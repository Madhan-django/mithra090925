from django.shortcuts import HttpResponse
from .models import AutomateFunc
from django.core.mail import EmailMessage
from fees.models import fee_reciept
from pettycash.models import PettyCashExpense
from inventory.models import stock
from grievance.models import Grievance
from django.db.models import Sum
from datetime import timedelta
from io import StringIO
from django.template.loader import render_to_string
from .utils import render_to_pdf
from django.db import connection
from django.utils import timezone
from collections import defaultdict
from staff.models import staff
from digiattend.models import BioDevices
import logging
import requests
import csv
import datetime

logger = logging.getLogger(__name__)

WHATSAPP_API_URL = "http://139.167.56.10:3000/send"
WHATSAPP_API_KEY = "MITHRAN_ERP_2026_x8K9mP2Q7L"


# ─────────────────────────────────────────────
#  WHATSAPP HELPER
# ─────────────────────────────────────────────

def send_whatsapp_message(number, message):
    clean_number = str(number).strip().replace("+", "").replace(" ", "")
    if len(clean_number) == 10:
        clean_number = "91" + clean_number
    headers = {"x-api-key": WHATSAPP_API_KEY}
    payload = {"number": clean_number, "message": message}
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            logger.info("WhatsApp sent to %s: %s", clean_number, response.text)
            return True
        else:
            logger.error("WhatsApp send failed (%s): %s", response.status_code, response.text)
            return False
    except requests.RequestException:
        logger.exception("WhatsApp send raised an exception for %s", clean_number)
        return False


# ─────────────────────────────────────────────
#  FEE COLLECTION
# ─────────────────────────────────────────────

def fee_collection(auto_task_id):
    try:
        if isinstance(auto_task_id, (list, tuple)):
            auto_task_id = auto_task_id[0]

        data = AutomateFunc.objects.get(id=auto_task_id)
        print("✅ DATA FOUND:", data.id, data.send_to)
        sch = data.school
        tdy = datetime.date.today()
        print("schedule type:-", data.schedule_type)

        # === DAILY ===
        if data.task == "fee_collection" and data.schedule_type == "DAILY":
            tdy_fee = fee_reciept.objects.filter(
                reciept_date=tdy,
                reciept_inv__fee_cat__fees_school=sch
            )
            total_revenue_Cash   = tdy_fee.filter(payment_type='Cash').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_revenue_Cheque = tdy_fee.filter(payment_type='Cheque').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_netbnk         = tdy_fee.filter(payment_type='Net-Banking').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_BT             = tdy_fee.filter(payment_type='Bank-Transfer').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_DD             = tdy_fee.filter(payment_type='Demand-Draft').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_UPI            = tdy_fee.filter(payment_type='UPI').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            tot_coll             = sum(coll.paid_amt for coll in tdy_fee)

            if data.automate_type == "email":
                context = {
                    'tdy_fee': tdy_fee,
                    'total_revenue_Cash': total_revenue_Cash,
                    'total_revenue_Cheque': total_revenue_Cheque,
                    'total_netbnk': total_netbnk,
                    'total_BT': total_BT,
                    'total_DD': total_DD,
                    'total_UPI': total_UPI,
                    'tot_coll': tot_coll,
                    'skool': sch,
                }
                pdf = render_to_pdf('fee/collect_summary.html', context)
                if pdf:
                    email = EmailMessage(
                        f"Daily Fee Collection Summary - {tdy.strftime('%d-%m-%Y')}",
                        "Please find the attached daily fee collection summary PDF.",
                        "noreply@mithran.co.in",
                        [data.created_by.email]
                    )
                    email.attach(f"fee_summary_{tdy.strftime('%d%m%Y')}.pdf", pdf.getvalue(), 'application/pdf')
                    email.send()
                    logger.info("Email TO: %s", [data.created_by.email])
                    return "Email with PDF sent successfully."
                return "Error generating PDF"

            elif data.automate_type == "whatsapp":
                message = (
                    f"📊 *Daily Fee Collection Summary*\n"
                    f"{tdy.strftime('%d-%m-%Y')}\n\n"
                    f"School: {sch}\n\n"
                    f"Cash: ₹{total_revenue_Cash}\n"
                    f"Cheque: ₹{total_revenue_Cheque}\n"
                    f"Net Banking: ₹{total_netbnk}\n"
                    f"Bank Transfer: ₹{total_BT}\n"
                    f"Demand Draft: ₹{total_DD}\n"
                    f"UPI: ₹{total_UPI}\n\n"
                    f"*Total Collection: ₹{tot_coll}*"
                )
                if send_whatsapp_message(data.send_to, message):
                    return "WhatsApp message sent successfully."
                return "WhatsApp send failed."

        # === WEEKLY ===
        elif data.task == "fee_collection" and data.schedule_type == "WEEKLY":
            start_of_week = tdy - datetime.timedelta(days=tdy.weekday())
            end_of_week   = tdy
            weekly_fees   = fee_reciept.objects.filter(
                reciept_date__range=[start_of_week, end_of_week],
                reciept_inv__fee_cat__fees_school=sch
            )
            total_revenue_Cash   = weekly_fees.filter(payment_type='Cash').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_revenue_Cheque = weekly_fees.filter(payment_type='Cheque').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_netbnk         = weekly_fees.filter(payment_type='Net-Banking').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_BT             = weekly_fees.filter(payment_type='Bank-Transfer').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_DD             = weekly_fees.filter(payment_type='Demand-Draft').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_UPI            = weekly_fees.filter(payment_type='UPI').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            tot_coll             = sum(item.paid_amt for item in weekly_fees)

            if data.automate_type == "email":
                context = {
                    'tdy_fee': weekly_fees,
                    'total_revenue_Cash': total_revenue_Cash,
                    'total_revenue_Cheque': total_revenue_Cheque,
                    'total_netbnk': total_netbnk,
                    'total_BT': total_BT,
                    'total_DD': total_DD,
                    'total_UPI': total_UPI,
                    'tot_coll': tot_coll,
                    'skool': sch,
                    'start_date': start_of_week,
                    'end_date': end_of_week,
                }
                pdf = render_to_pdf('fee/collect_summary.html', context)
                if pdf:
                    email = EmailMessage(
                        f"Weekly Fee Report ({start_of_week.strftime('%d-%b')} to {end_of_week.strftime('%d-%b')})",
                        "Attached is the weekly fee collection summary.",
                        "noreply@mithran.co.in",
                        [data.created_by.email]
                    )
                    email.attach(
                        f"weekly_fee_report_{start_of_week.strftime('%d%m')}_{end_of_week.strftime('%d%m')}.pdf",
                        pdf.getvalue(), 'application/pdf'
                    )
                    email.send()
                    logger.info("Email TO: %s", [data.created_by.email])
                    return "Weekly report sent successfully."
                return "PDF generation failed."

            elif data.automate_type == "whatsapp":
                message = (
                    f"📊 *Weekly Fee Collection Summary*\n"
                    f"{start_of_week.strftime('%d-%b')} to {end_of_week.strftime('%d-%b')}\n\n"
                    f"School: {sch}\n\n"
                    f"Cash: ₹{total_revenue_Cash}\n"
                    f"Cheque: ₹{total_revenue_Cheque}\n"
                    f"Net Banking: ₹{total_netbnk}\n"
                    f"Bank Transfer: ₹{total_BT}\n"
                    f"Demand Draft: ₹{total_DD}\n"
                    f"UPI: ₹{total_UPI}\n\n"
                    f"*Total Collection: ₹{tot_coll}*"
                )
                if send_whatsapp_message(data.send_to, message):
                    return "WhatsApp message sent successfully."
                return "WhatsApp send failed."

        # === MONTHLY ===
        elif data.task == "fee_collection" and data.schedule_type == "MONTHLY":
            start_of_month = tdy.replace(day=1)
            end_of_month   = tdy
            monthly_fees   = fee_reciept.objects.filter(
                reciept_date__range=[start_of_month, end_of_month],
                reciept_inv__fee_cat__fees_school=sch
            )
            total_revenue_Cash   = monthly_fees.filter(payment_type='Cash').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_revenue_Cheque = monthly_fees.filter(payment_type='Cheque').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_netbnk         = monthly_fees.filter(payment_type='Net-Banking').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_BT             = monthly_fees.filter(payment_type='Bank-Transfer').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_DD             = monthly_fees.filter(payment_type='Demand-Draft').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_UPI            = monthly_fees.filter(payment_type='UPI').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            tot_coll             = sum(item.paid_amt for item in monthly_fees)

            if data.automate_type == "email":
                context = {
                    'tdy_fee': monthly_fees,
                    'total_revenue_Cash': total_revenue_Cash,
                    'total_revenue_Cheque': total_revenue_Cheque,
                    'total_netbnk': total_netbnk,
                    'total_BT': total_BT,
                    'total_DD': total_DD,
                    'total_UPI': total_UPI,
                    'tot_coll': tot_coll,
                    'skool': sch,
                    'start_date': start_of_month,
                    'end_date': end_of_month,
                }
                pdf = render_to_pdf('fee/collect_summary.html', context)
                if pdf:
                    email = EmailMessage(
                        f"Monthly Fee Report ({start_of_month.strftime('%b %Y')})",
                        "Attached is the monthly fee collection summary.",
                        "noreply@mithran.co.in",
                        [data.created_by.email]
                    )
                    email.attach(
                        f"monthly_fee_report_{start_of_month.strftime('%b%Y')}.pdf",
                        pdf.getvalue(), 'application/pdf'
                    )
                    email.send()
                    logger.info("Email TO: %s", [data.created_by.email])
                    return "Monthly report sent successfully."
                return "Monthly PDF generation failed."

            elif data.automate_type == "whatsapp":
                message = (
                    f"📊 *Monthly Fee Collection Summary*\n"
                    f"{start_of_month.strftime('%b %Y')}\n\n"
                    f"School: {sch}\n\n"
                    f"Cash: ₹{total_revenue_Cash}\n"
                    f"Cheque: ₹{total_revenue_Cheque}\n"
                    f"Net Banking: ₹{total_netbnk}\n"
                    f"Bank Transfer: ₹{total_BT}\n"
                    f"Demand Draft: ₹{total_DD}\n"
                    f"UPI: ₹{total_UPI}\n\n"
                    f"*Total Collection: ₹{tot_coll}*"
                )
                if send_whatsapp_message(data.send_to, message):
                    return "WhatsApp message sent successfully."
                return "WhatsApp send failed."

        return "Conditions not met for daily/weekly/monthly automation."

    except Exception as e:
        logger.exception("fee_collection task failed for auto_task_id=%s", auto_task_id)
        return str(e)


# ─────────────────────────────────────────────
#  PETTY CASH
# ─────────────────────────────────────────────

def petty_cash(auto_task_id):
    logger.info("Entering petty cash")
    try:
        if isinstance(auto_task_id, (list, tuple)):
            auto_task_id = auto_task_id[0]

        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()
        print("schedule type:-", data_obj.schedule_type)

        # === DAILY ===
        if data_obj.task == "petty_cash" and data_obj.schedule_type == "DAILY":
            expenses = PettyCashExpense.objects.filter(date_spent=tdy, petty_school=sch)

            if data_obj.automate_type == "email":
                if not expenses.exists():
                    return "No petty cash records for today."
                csv_buffer = StringIO()
                writer = csv.writer(csv_buffer)
                writer.writerow([f"School: {sch}"])
                writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Balance'])
                for obj in expenses:
                    writer.writerow([obj.date_spent.strftime("%Y-%m-%d"), obj.description, obj.category, obj.amount, obj.balance])
                email = EmailMessage(
                    f"Petty Cash Report - {tdy.strftime('%d-%m-%Y')}",
                    "Please find the attached petty cash report.",
                    "noreply@mithran.co.in",
                    [data_obj.created_by.email],
                )
                email.attach(f"pettycash_{tdy.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Daily petty cash email sent successfully."

            elif data_obj.automate_type == "whatsapp":
                if not expenses.exists():
                    return "No petty cash records for today."
                total = sum(obj.amount for obj in expenses)
                lines = "\n".join(f"• {obj.description} ({obj.category}): ₹{obj.amount}" for obj in expenses)
                message = (
                    f"💰 *Daily Petty Cash Report*\n"
                    f"{tdy.strftime('%d-%m-%Y')}\n\n"
                    f"School: {sch}\n\n"
                    f"{lines}\n\n"
                    f"*Total Spent: ₹{total}*"
                )
                if send_whatsapp_message(data_obj.send_to, message):
                    return "Daily petty cash WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === WEEKLY ===
        elif data_obj.task == "petty_cash" and data_obj.schedule_type == "WEEKLY":
            start_date = tdy - timedelta(days=tdy.weekday())
            end_date   = start_date + timedelta(days=5)
            expenses   = PettyCashExpense.objects.filter(date_spent__range=(start_date, end_date), petty_school=sch)

            if data_obj.automate_type == "email":
                csv_buffer = StringIO()
                writer = csv.writer(csv_buffer)
                writer.writerow([f"School: {sch}"])
                writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Balance'])
                for obj in expenses:
                    writer.writerow([obj.date_spent.strftime("%Y-%m-%d"), obj.description, obj.category, obj.amount, obj.balance])
                to_emails = [e.strip() for e in data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [data_obj.created_by.email]
                email = EmailMessage(
                    f"Petty Cash Report - {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}",
                    "Please find the attached petty cash report (Monday to Saturday).",
                    "noreply@mithran.co.in",
                    to_emails,
                )
                email.attach(f"pettycash_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Weekly petty cash email sent successfully."

            elif data_obj.automate_type == "whatsapp":
                total = sum(obj.amount for obj in expenses)
                lines = "\n".join(f"• {obj.date_spent.strftime('%d-%m')} {obj.description} ({obj.category}): ₹{obj.amount}" for obj in expenses) or "No expenses this week."
                message = (
                    f"💰 *Weekly Petty Cash Report*\n"
                    f"{start_date.strftime('%d-%b')} to {end_date.strftime('%d-%b')}\n\n"
                    f"School: {sch}\n\n"
                    f"{lines}\n\n"
                    f"*Total Spent: ₹{total}*"
                )
                if send_whatsapp_message(data_obj.send_to, message):
                    return "Weekly petty cash WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === MONTHLY ===
        elif data_obj.task == "petty_cash" and data_obj.schedule_type == "MONTHLY":
            first_day_this_month = tdy.replace(day=1)
            last_day_prev_month  = first_day_this_month - timedelta(days=1)
            first_day_prev_month = last_day_prev_month.replace(day=1)
            expenses = PettyCashExpense.objects.filter(date_spent__range=(first_day_prev_month, last_day_prev_month), petty_school=sch)

            if data_obj.automate_type == "email":
                csv_buffer = StringIO()
                writer = csv.writer(csv_buffer)
                writer.writerow([f"School: {sch}"])
                writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Balance'])
                for obj in expenses:
                    writer.writerow([obj.date_spent.strftime("%Y-%m-%d"), obj.description, obj.category, obj.amount, obj.balance])
                to_emails = [e.strip() for e in data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [data_obj.created_by.email]
                email = EmailMessage(
                    f"Petty Cash Report - {first_day_prev_month.strftime('%B %Y')}",
                    f"Attached is the petty cash report from {first_day_prev_month.strftime('%d-%m-%Y')} to {last_day_prev_month.strftime('%d-%m-%Y')}.",
                    "noreply@mithran.co.in",
                    to_emails,
                )
                email.attach(f"pettycash_{first_day_prev_month.strftime('%Y%m%d')}_{last_day_prev_month.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Monthly petty cash email sent successfully."

            elif data_obj.automate_type == "whatsapp":
                total = sum(obj.amount for obj in expenses)
                lines = "\n".join(f"• {obj.date_spent.strftime('%d-%m')} {obj.description} ({obj.category}): ₹{obj.amount}" for obj in expenses) or "No expenses this month."
                message = (
                    f"💰 *Monthly Petty Cash Report*\n"
                    f"{first_day_prev_month.strftime('%B %Y')}\n\n"
                    f"School: {sch}\n\n"
                    f"{lines}\n\n"
                    f"*Total Spent: ₹{total}*"
                )
                if send_whatsapp_message(data_obj.send_to, message):
                    return "Monthly petty cash WhatsApp sent successfully."
                return "WhatsApp send failed."

        return "Conditions not met for daily/weekly/monthly automation."

    except Exception as e:
        logger.exception("petty_cash task failed for auto_task_id=%s", auto_task_id)
        return str(e)


# ─────────────────────────────────────────────
#  STOCKS
# ─────────────────────────────────────────────

def stocks(auto_task_id):
    logger.info("Entering Stock")
    try:
        if isinstance(auto_task_id, (list, tuple)):
            auto_task_id = auto_task_id[0]

        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()
        print("schedule type:-", data_obj.schedule_type)

        stock_items = stock.objects.filter(Prod_school=sch)

        def build_stock_csv():
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Name', 'Description', 'Category', 'Quantity'])
            for obj in stock_items:
                writer.writerow([obj.name, obj.description, obj.category, obj.quantity])
            return csv_buffer

        def build_stock_whatsapp_message(period_label):
            lines = "\n".join(f"• {obj.name} ({obj.category}): {obj.quantity}" for obj in stock_items) or "No stock records found."
            return (
                f"📦 *Stock Report — {period_label}*\n"
                f"{tdy.strftime('%d-%m-%Y')}\n\n"
                f"School: {sch}\n\n"
                f"{lines}"
            )

        # === DAILY ===
        if data_obj.task == "stocks" and data_obj.schedule_type == "DAILY":
            if not stock_items.exists():
                return "No stock records found."
            if data_obj.automate_type == "email":
                csv_buffer = build_stock_csv()
                email = EmailMessage(f"Stock Report - {tdy.strftime('%d-%m-%Y')}", "Please find the attached daily stock report.", "noreply@mithran.co.in", [data_obj.created_by.email])
                email.attach(f"stock_{tdy.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Daily stock email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                if send_whatsapp_message(data_obj.send_to, build_stock_whatsapp_message("Daily")):
                    return "Daily stock WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === WEEKLY ===
        elif data_obj.task == "stocks" and data_obj.schedule_type == "WEEKLY":
            start_date = tdy - timedelta(days=tdy.weekday())
            end_date   = start_date + timedelta(days=5)
            if not stock_items.exists():
                return "No stock records found."
            if data_obj.automate_type == "email":
                to_emails = [e.strip() for e in data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [data_obj.created_by.email]
                csv_buffer = build_stock_csv()
                email = EmailMessage(f"Stock Report - {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}", "Please find the attached weekly stock report.", "noreply@mithran.co.in", to_emails)
                email.attach(f"stock_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Weekly stock email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                period = f"{start_date.strftime('%d-%b')} to {end_date.strftime('%d-%b')}"
                if send_whatsapp_message(data_obj.send_to, build_stock_whatsapp_message(period)):
                    return "Weekly stock WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === MONTHLY ===
        elif data_obj.task == "stocks" and data_obj.schedule_type == "MONTHLY":
            first_day_this_month = tdy.replace(day=1)
            last_day_prev_month  = first_day_this_month - timedelta(days=1)
            first_day_prev_month = last_day_prev_month.replace(day=1)
            if not stock_items.exists():
                return "No stock records found."
            if data_obj.automate_type == "email":
                to_emails = [e.strip() for e in data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [data_obj.created_by.email]
                csv_buffer = build_stock_csv()
                email = EmailMessage(f"Stock Report - {first_day_prev_month.strftime('%B %Y')}", f"Attached is the stock report for {first_day_prev_month.strftime('%B %Y')}.", "noreply@mithran.co.in", to_emails)
                email.attach(f"stock_{first_day_prev_month.strftime('%Y%m%d')}_{last_day_prev_month.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Monthly stock email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                if send_whatsapp_message(data_obj.send_to, build_stock_whatsapp_message(first_day_prev_month.strftime('%B %Y'))):
                    return "Monthly stock WhatsApp sent successfully."
                return "WhatsApp send failed."

        return "Conditions not met for daily/weekly/monthly automation."

    except Exception as e:
        logger.exception("stocks task failed for auto_task_id=%s", auto_task_id)
        return str(e)


# ─────────────────────────────────────────────
#  GRIEVANCE REPORT
# ─────────────────────────────────────────────

def Grievance_Report(auto_task_id):
    logger.info("Entering Grievance Automation")
    try:
        if isinstance(auto_task_id, (list, tuple)):
            auto_task_id = auto_task_id[0]

        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()

        def build_grievance_csv(complaints):
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Student', 'Class', 'Sec', 'Mobile', 'Area', 'Detail', 'Status', 'Complaint Date'])
            for obj in complaints:
                writer.writerow([str(obj.stud_name), obj.gclass, obj.gsec, obj.mobile, obj.area_of_complaint, obj.detail, obj.complaint_status, obj.complaint_date.strftime('%d-%m-%Y')])
            return csv_buffer

        def build_grievance_whatsapp(complaints, period_label):
            lines = "\n".join(
                f"• {obj.stud_name} | {obj.gclass}-{obj.gsec} | {obj.area_of_complaint} | {obj.complaint_status}"
                for obj in complaints
            ) or "No grievances found."
            return (
                f"📋 *Grievance Report — {period_label}*\n"
                f"School: {sch}\n\n"
                f"{lines}\n\n"
                f"*Total: {complaints.count()}*"
            )

        # === DAILY ===
        if data_obj.task == "Grievance_Report" and data_obj.schedule_type == "DAILY":
            complaints = Grievance.objects.filter(gschool=sch, complaint_date=tdy)
            if data_obj.automate_type == "email":
                if not complaints.exists():
                    return "No grievance records for today."
                csv_buffer = build_grievance_csv(complaints)
                email = EmailMessage(f"Daily Grievance Report - {tdy.strftime('%d-%m-%Y')}", "Please find the attached daily grievance report.", "noreply@mithran.co.in", [data_obj.created_by.email])
                email.attach(f"grievance_{tdy.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Daily grievance email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                if not complaints.exists():
                    return "No grievance records for today."
                if send_whatsapp_message(data_obj.send_to, build_grievance_whatsapp(complaints, tdy.strftime('%d-%m-%Y'))):
                    return "Daily grievance WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === WEEKLY ===
        elif data_obj.task == "Grievance_Report" and data_obj.schedule_type == "WEEKLY":
            start_date = tdy - timedelta(days=tdy.weekday())
            end_date   = start_date + timedelta(days=5)
            complaints = Grievance.objects.filter(gschool=sch, complaint_date__range=(start_date, end_date))
            if data_obj.automate_type == "email":
                csv_buffer = build_grievance_csv(complaints)
                email = EmailMessage(f"Weekly Grievance Report - {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}", "Please find the attached weekly grievance report.", "noreply@mithran.co.in", [data_obj.created_by.email])
                email.attach(f"grievance_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Weekly grievance email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                period = f"{start_date.strftime('%d-%b')} to {end_date.strftime('%d-%b')}"
                if send_whatsapp_message(data_obj.send_to, build_grievance_whatsapp(complaints, period)):
                    return "Weekly grievance WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === MONTHLY ===
        elif data_obj.task == "Grievance_Report" and data_obj.schedule_type == "MONTHLY":
            first_day_this_month = tdy.replace(day=1)
            last_day_prev_month  = first_day_this_month - timedelta(days=1)
            first_day_prev_month = last_day_prev_month.replace(day=1)
            complaints = Grievance.objects.filter(gschool=sch, complaint_date__range=(first_day_prev_month, last_day_prev_month))
            if data_obj.automate_type == "email":
                csv_buffer = build_grievance_csv(complaints)
                email = EmailMessage(f"Monthly Grievance Report - {first_day_prev_month.strftime('%B %Y')}", f"Attached is the grievance report for {first_day_prev_month.strftime('%B %Y')}.", "noreply@mithran.co.in", [data_obj.created_by.email])
                email.attach(f"grievance_{first_day_prev_month.strftime('%Y%m%d')}_{last_day_prev_month.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Monthly grievance email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                if send_whatsapp_message(data_obj.send_to, build_grievance_whatsapp(complaints, first_day_prev_month.strftime('%B %Y'))):
                    return "Monthly grievance WhatsApp sent successfully."
                return "WhatsApp send failed."

        return "Conditions not met for daily/weekly/monthly automation."

    except Exception as e:
        logger.exception("Grievance_Report task failed for auto_task_id=%s", auto_task_id)
        return str(e)


# ─────────────────────────────────────────────
#  GRIEVANCE OVERDUE
# ─────────────────────────────────────────────

def Grievance_over_Due(auto_task_id):
    logger.info("Entering Overdue Grievance Report")
    try:
        if isinstance(auto_task_id, (list, tuple)):
            auto_task_id = auto_task_id[0]

        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()

        if data_obj.task != "Grievance_over_Due":
            return "Conditions not met for Grievance_over_Due automation."

        qs = Grievance.objects.filter(gschool=sch)
        open_overdue       = qs.filter(complaint_status="Open",        complaint_date__lte=tdy - timedelta(days=2))
        pending_overdue    = qs.filter(complaint_status="Pending",     complaint_date__lte=tdy - timedelta(days=3))
        inprogress_overdue = qs.filter(complaint_status="In-progress", action_date__lte=tdy - timedelta(days=3))
        overdue_list       = (open_overdue | pending_overdue | inprogress_overdue).distinct()

        if not overdue_list.exists():
            return "No overdue grievances found."

        if data_obj.automate_type == "email":
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Student', 'Class', 'Sec', 'Mobile', 'Area', 'Detail', 'Status', 'Complaint Date', 'Action Date'])
            for obj in overdue_list:
                writer.writerow([
                    str(obj.stud_name), str(obj.gclass), str(obj.gsec),
                    obj.mobile, obj.area_of_complaint, obj.detail,
                    obj.complaint_status,
                    obj.complaint_date.strftime('%d-%m-%Y'),
                    obj.action_date.strftime('%d-%m-%Y') if obj.action_date else ""
                ])
            email = EmailMessage(
                f"Overdue Grievance Report - {tdy.strftime('%d-%m-%Y')}",
                "Please find the attached overdue grievance report.",
                "noreply@mithran.co.in",
                [data_obj.created_by.email],
            )
            email.attach(f"overdue_grievance_{tdy.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
            email.send()
            return "Overdue grievance email sent successfully."

        elif data_obj.automate_type == "whatsapp":
            lines = "\n".join(
                f"• {obj.stud_name} | {obj.gclass}-{obj.gsec} | {obj.area_of_complaint} | {obj.complaint_status} | Since: {obj.complaint_date.strftime('%d-%m-%Y')}"
                for obj in overdue_list
            )
            message = (
                f"⚠️ *Overdue Grievance Report*\n"
                f"{tdy.strftime('%d-%m-%Y')}\n\n"
                f"School: {sch}\n\n"
                f"{lines}\n\n"
                f"*Total Overdue: {overdue_list.count()}*"
            )
            if send_whatsapp_message(data_obj.send_to, message):
                return "Overdue grievance WhatsApp sent successfully."
            return "WhatsApp send failed."

        return "Conditions not met for Grievance_over_Due automation."

    except Exception as e:
        logger.exception("Grievance_over_Due task failed for auto_task_id=%s", auto_task_id)
        return str(e)


# ─────────────────────────────────────────────
#  MORNING ATTENDANCE ALERT
# ─────────────────────────────────────────────

def Morning_Attendance_Alert(auto_task_id):
    logger.info("Entering Morning Attendance Alert")
    try:
        if isinstance(auto_task_id, (list, tuple)):
            auto_task_id = auto_task_id[0]

        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()

        if data_obj.task != "Morning_Attendance_Alert":
            return "Conditions not met for Morning_Attendance_Alert automation."

        def get_attendance_for_date(date_obj):
            table_name = f"DeviceLogs_{date_obj.month}_{date_obj.year}"
            device_ids = list(BioDevices.objects.filter(BioSchool=sch).values_list('BioDeviceId', flat=True))
            if not device_ids:
                return []
            placeholders = ', '.join(['%s'] * len(device_ids))
            query = f"""
                SELECT
                    UserId,
                    MIN(CONVERT_TZ(LogDate, '+00:00', '+05:30')) AS in_time,
                    MAX(CONVERT_TZ(LogDate, '+00:00', '+05:30')) AS out_time,
                    COUNT(*) as punch_count
                FROM {table_name}
                WHERE DATE(CONVERT_TZ(LogDate, '+00:00', '+05:30')) = %s
                  AND DeviceId IN ({placeholders})
                GROUP BY UserId
            """
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, [date_obj, *device_ids])
                    rows = cursor.fetchall()
            except Exception:
                rows = []

            rows_map   = {row[0]: row for row in rows}
            staff_list = list(
                staff.objects.select_related('shift', 'department')
                .filter(staff_school=sch)
                .order_by('shift__name', 'department')
            )

            result = []
            for stf in staff_list:
                user_id    = stf.BioCode
                row        = rows_map.get(user_id)
                shift_name = stf.shift.name if stf.shift else "No Shift"

                if row:
                    _, in_time, out_time, punch_count = row
                    if in_time:
                        in_time = timezone.make_aware(in_time, timezone.get_current_timezone())
                    if out_time:
                        out_time = timezone.make_aware(out_time, timezone.get_current_timezone())

                    work_hours = ""
                    if in_time and out_time:
                        total_seconds = int((out_time - in_time).total_seconds())
                        h = total_seconds // 3600
                        m = (total_seconds % 3600) // 60
                        s = total_seconds % 60
                        work_hours = f"{h:02}:{m:02}:{s:02}"

                    # Mis-punch
                    if punch_count == 1:
                        result.append({
                            "date": date_obj,
                            "name": f"{stf.first_name} {stf.last_name}",
                            "designation": stf.desg or "",
                            "department": stf.department.name if stf.department else "",
                            "shift": shift_name,
                            "in_time": in_time.strftime('%H:%M') if in_time else "",
                            "out_time": out_time.strftime('%H:%M') if out_time else "",
                            "work_hours": work_hours,
                            "status": "MIS_PUNCH",
                        })
                        continue

                    # Late — no grace, purely shift start
                    is_late = False
                    if stf.shift and stf.shift.start_time and in_time:
                        shift_start_dt = timezone.make_aware(
                            datetime.datetime.combine(date_obj, stf.shift.start_time),
                            timezone.get_current_timezone()
                        )
                        if in_time > shift_start_dt:
                            is_late = True

                    if is_late:
                        result.append({
                            "date": date_obj,
                            "name": f"{stf.first_name} {stf.last_name}",
                            "designation": stf.desg or "",
                            "department": stf.department.name if stf.department else "",
                            "shift": shift_name,
                            "in_time": in_time.strftime('%H:%M') if in_time else "",
                            "out_time": out_time.strftime('%H:%M') if out_time else "",
                            "work_hours": work_hours,
                            "status": "LATE",
                        })
                else:
                    result.append({
                        "date": date_obj,
                        "name": f"{stf.first_name} {stf.last_name}",
                        "designation": stf.desg or "",
                        "department": stf.department.name if stf.department else "",
                        "shift": shift_name,
                        "in_time": "",
                        "out_time": "",
                        "work_hours": "",
                        "status": "ABSENT",
                    })
            return result

        def build_attendance_csv(records, period_label):
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow([f"Period: {period_label}"])
            writer.writerow(['Date', 'Name', 'Designation', 'Department', 'Shift', 'In Time', 'Out Time', 'Work Hours', 'Status'])
            for r in records:
                writer.writerow([
                    r['date'].strftime('%d-%m-%Y'), r['name'], r['designation'],
                    r['department'], r['shift'], r['in_time'], r['out_time'],
                    r['work_hours'], r['status'],
                ])
            return csv_buffer

        def build_attendance_whatsapp(records, period_label):
            by_shift = defaultdict(lambda: {'absent': [], 'late': [], 'mispunch': []})
            for r in records:
                if r['status'] == 'ABSENT':
                    by_shift[r['shift']]['absent'].append(r)
                elif r['status'] == 'LATE':
                    by_shift[r['shift']]['late'].append(r)
                elif r['status'] == 'MIS_PUNCH':
                    by_shift[r['shift']]['mispunch'].append(r)

            lines = []
            for shift_name in sorted(by_shift.keys()):
                group = by_shift[shift_name]
                lines.append(f"\n🕐 *{shift_name}*")
                if group['absent']:
                    lines.append("  🔴 *Absent:*")
                    lines += [f"    • {r['name']} ({r['department']})" for r in group['absent']]
                if group['late']:
                    lines.append("  🟡 *Late:*")
                    lines += [f"    • {r['name']} | In: {r['in_time']} ({r['department']})" for r in group['late']]
                if group['mispunch']:
                    lines.append("  🟠 *Mis-Punch:*")
                    lines += [f"    • {r['name']} ({r['department']})" for r in group['mispunch']]

            total_absent   = sum(len(g['absent'])   for g in by_shift.values())
            total_late     = sum(len(g['late'])      for g in by_shift.values())
            total_mispunch = sum(len(g['mispunch'])  for g in by_shift.values())

            body = "\n".join(lines) or "All staff present on time."
            return (
                f"📅 *Attendance Report — {period_label}*\n"
                f"School: {sch}\n"
                f"{body}\n\n"
                f"Absent: {total_absent} | Late: {total_late} | Mis-Punch: {total_mispunch}"
            )

        # === DAILY ===
        if data_obj.task == "Morning_Attendance_Alert" and data_obj.schedule_type == "DAILY":
            records = get_attendance_for_date(tdy)
            period_label = tdy.strftime('%d-%m-%Y')
            if not records:
                return "No late/absent/mispunch staff for today."
            if data_obj.automate_type == "email":
                csv_buffer = build_attendance_csv(records, period_label)
                email = EmailMessage(
                    f"Daily Attendance Report - {period_label}",
                    "Please find the attached daily attendance report (Late/Absent/Mis-Punch only).",
                    "noreply@mithran.co.in",
                    [data_obj.created_by.email],
                )
                email.attach(f"attendance_{tdy.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Daily attendance email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                message = build_attendance_whatsapp(records, period_label)
                if send_whatsapp_message(data_obj.send_to, message):
                    return "Daily attendance WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === WEEKLY ===
        elif data_obj.task == "Morning_Attendance_Alert" and data_obj.schedule_type == "WEEKLY":
            start_date  = tdy - timedelta(days=tdy.weekday())
            end_date    = start_date + timedelta(days=5)
            all_records = []
            current     = start_date
            while current <= end_date:
                all_records.extend(get_attendance_for_date(current))
                current += timedelta(days=1)
            period_label = f"{start_date.strftime('%d-%b')} to {end_date.strftime('%d-%b')}"
            if not all_records:
                return "No late/absent/mispunch staff for this week."
            if data_obj.automate_type == "email":
                csv_buffer = build_attendance_csv(all_records, period_label)
                email = EmailMessage(
                    f"Weekly Attendance Report - {period_label}",
                    "Please find the attached weekly attendance report (Late/Absent/Mis-Punch only).",
                    "noreply@mithran.co.in",
                    [data_obj.created_by.email],
                )
                email.attach(f"attendance_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Weekly attendance email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                message = build_attendance_whatsapp(all_records, period_label)
                if send_whatsapp_message(data_obj.send_to, message):
                    return "Weekly attendance WhatsApp sent successfully."
                return "WhatsApp send failed."

        # === MONTHLY ===
        elif data_obj.task == "Morning_Attendance_Alert" and data_obj.schedule_type == "MONTHLY":
            first_day_this_month = tdy.replace(day=1)
            last_day_prev_month  = first_day_this_month - timedelta(days=1)
            first_day_prev_month = last_day_prev_month.replace(day=1)
            all_records = []
            current     = first_day_prev_month
            while current <= last_day_prev_month:
                all_records.extend(get_attendance_for_date(current))
                current += timedelta(days=1)
            period_label = first_day_prev_month.strftime('%B %Y')
            if not all_records:
                return "No late/absent/mispunch staff for last month."
            if data_obj.automate_type == "email":
                csv_buffer = build_attendance_csv(all_records, period_label)
                email = EmailMessage(
                    f"Monthly Attendance Report - {period_label}",
                    f"Attached is the attendance report for {period_label} (Late/Absent/Mis-Punch only).",
                    "noreply@mithran.co.in",
                    [data_obj.created_by.email],
                )
                email.attach(f"attendance_{first_day_prev_month.strftime('%Y%m%d')}_{last_day_prev_month.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
                email.send()
                return "Monthly attendance email sent successfully."
            elif data_obj.automate_type == "whatsapp":
                message = build_attendance_whatsapp(all_records, period_label)
                if send_whatsapp_message(data_obj.send_to, message):
                    return "Monthly attendance WhatsApp sent successfully."
                return "WhatsApp send failed."

        return "Conditions not met for daily/weekly/monthly automation."

    except Exception as e:
        logger.exception("Morning_Attendance_Alert task failed for auto_task_id=%s", auto_task_id)
        return str(e)