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
import logging

logger = logging.getLogger(__name__)
from django.template.loader import render_to_string
from .utils import render_to_pdf
import csv
import datetime
from django.http import JsonResponse


def fee_collection(auto_task_id):
    try:
        if isinstance(auto_task_id, (list, tuple)):
            auto_task_id = auto_task_id[0]

        data = AutomateFunc.objects.get(id=auto_task_id)

        print("✅ DATA FOUND:", data.id,data.send_to)
        data = AutomateFunc.objects.get(id=auto_task_id)
        sch = data.school
        tdy = datetime.date.today()

        print("schedule type:-", data.schedule_type)

        # === DAILY ===
        if data.task == "fee_collection" and data.schedule_type == "DAILY" and data.automate_type == "email":
            tdy_fee = fee_reciept.objects.filter(
                reciept_date=tdy,
                reciept_inv__fee_cat__fees_school=sch
            )

            total_revenue_Cash = tdy_fee.filter(payment_type='Cash').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_revenue_Cheque = tdy_fee.filter(payment_type='Cheque').aggregate(Sum('paid_amt'))[
                                       'paid_amt__sum'] or 0
            total_netbnk = tdy_fee.filter(payment_type='Net-Banking').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_BT = tdy_fee.filter(payment_type='Bank-Transfer').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_DD = tdy_fee.filter(payment_type='Demand-Draft').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_UPI = tdy_fee.filter(payment_type='UPI').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0

            tot_coll = sum(coll.paid_amt for coll in tdy_fee)

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
                subject = f"Daily Fee Collection Summary - {tdy.strftime('%d-%m-%Y')}"
                body = "Please find the attached daily fee collection summary PDF."
                from_email = "noreply@mithran.co.in"
               cd

                email = EmailMessage(subject, body, from_email, to_email)
                email.attach(f"fee_summary_{tdy.strftime('%d%m%Y')}.pdf", pdf.getvalue(), 'application/pdf')
                email.send()
                ogger.info("Email TO: %s", to_email)
                return "Email with PDF sent successfully."
            else:
                return "Error generating PDF"

        # === WEEKLY ===
        elif data.task == "fee_collection" and data.schedule_type == "WEEKLY" and data.automate_type == "email":
            start_of_week = tdy - datetime.timedelta(days=tdy.weekday())  # Monday
            end_of_week = tdy  # Usually set to Saturday

            weekly_fees = fee_reciept.objects.filter(
                reciept_date__range=[start_of_week, end_of_week],
                reciept_inv__fee_cat__fees_school=sch
            )

            total_revenue_Cash = weekly_fees.filter(payment_type='Cash').aggregate(Sum('paid_amt'))[
                                     'paid_amt__sum'] or 0
            total_revenue_Cheque = weekly_fees.filter(payment_type='Cheque').aggregate(Sum('paid_amt'))[
                                       'paid_amt__sum'] or 0
            total_netbnk = weekly_fees.filter(payment_type='Net-Banking').aggregate(Sum('paid_amt'))[
                               'paid_amt__sum'] or 0
            total_BT = weekly_fees.filter(payment_type='Bank-Transfer').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_DD = weekly_fees.filter(payment_type='Demand-Draft').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_UPI = weekly_fees.filter(payment_type='UPI').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0

            tot_coll = sum(item.paid_amt for item in weekly_fees)

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
                subject = f"Weekly Fee Report ({start_of_week.strftime('%d-%b')} to {end_of_week.strftime('%d-%b')})"
                body = "Attached is the weekly fee collection summary."
                from_email = "noreply@mithran.co.in"
                to_email = [data.created_by.email]

                email = EmailMessage(subject, body, from_email, to_email)
                email.attach(
                    f"weekly_fee_report_{start_of_week.strftime('%d%m')}_{end_of_week.strftime('%d%m')}.pdf",
                    pdf.getvalue(), 'application/pdf')
                email.send()

                return "Weekly report sent successfully."
            else:
                return "PDF generation failed."

        # === MONTHLY ===
        else:
            start_of_month = tdy.replace(day=1)
            end_of_month = tdy

            monthly_fees = fee_reciept.objects.filter(
                reciept_date__range=[start_of_month, end_of_month],
                reciept_inv__fee_cat__fees_school=sch
            )

            total_revenue_Cash = monthly_fees.filter(payment_type='Cash').aggregate(Sum('paid_amt'))[
                                     'paid_amt__sum'] or 0
            total_revenue_Cheque = monthly_fees.filter(payment_type='Cheque').aggregate(Sum('paid_amt'))[
                                       'paid_amt__sum'] or 0
            total_netbnk = monthly_fees.filter(payment_type='Net-Banking').aggregate(Sum('paid_amt'))[
                               'paid_amt__sum'] or 0
            total_BT = monthly_fees.filter(payment_type='Bank-Transfer').aggregate(Sum('paid_amt'))[
                           'paid_amt__sum'] or 0
            total_DD = monthly_fees.filter(payment_type='Demand-Draft').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
            total_UPI = monthly_fees.filter(payment_type='UPI').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0

            tot_coll = sum(item.paid_amt for item in monthly_fees)

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
                subject = f"Monthly Fee Report ({start_of_month.strftime('%b %Y')})"
                body = "Attached is the monthly fee collection summary."
                from_email = "noreply@mithran.co.in"
                to_email = [data.created_by.email]

                email = EmailMessage(subject, body, from_email, to_email)
                email.attach(
                    f"monthly_fee_report_{start_of_month.strftime('%b%Y')}.pdf",
                    pdf.getvalue(), 'application/pdf')
                email.send()

                return "Monthly report sent successfully."
            else:
                return "Monthly PDF generation failed."

        return "Conditions not met for daily/weekly/monthly email."

    except Exception as e:
        return str(e)


def petty_cash(auto_task_id):
    logger.info("Entering petty cash")
    try:
        auto_task_id = auto_task_id[0]  # if it's a list
        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()
        print("schedule type:-", data_obj.schedule_type)
        # tdy = datetime.date(2024, 6, 26)
        # === DAILY EMAIL TASK ===
        if data_obj.task == "pettycash" and data_obj.schedule_type == "DAILY" and data_obj.automate_type == "email":
            expenses = PettyCashExpense.objects.filter(date_spent=tdy, petty_school=sch)

            if not expenses.exists():
                return HttpResponse("No petty cash records for today.", status=204)

            # Generate CSV
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Balance'])

            for obj in expenses:
                writer.writerow([
                    obj.date_spent.strftime("%Y-%m-%d"),
                    obj.description,
                    obj.category,
                    obj.amount,
                    obj.balance
                ])

            # Prepare and send email
            email = EmailMessage(
                subject=f"Petty Cash Report - {tdy.strftime('%d-%m-%Y')}",
                body="Please find the attached petty cash report.",
                from_email="noreply@mithran.co.in",
                to=[data_obj.created_by.email],  # ensure this field exists or modify as needed
            )
            email.attach(f"pettycash_{tdy.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
            email.send()

            return HttpResponse("Email sent successfully.")
        elif data_obj.task == "pettycash" and data_obj.schedule_type == "WEEKLY" and data_obj.automate_type == "email":

            # Get current week's Monday to Saturday
            start_date = tdy - timedelta(days=tdy.weekday())  # Monday
            end_date = start_date + timedelta(days=5)  # Saturday

            expenses = PettyCashExpense.objects.filter(
                date_spent__range=(start_date, end_date),
                petty_school=sch
            )

            # if not expenses.exists():
            #     return HttpResponse("No petty cash records for this week (Mon-Sat).", status=204)

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Balance'])

            for obj in expenses:
                writer.writerow([
                    obj.date_spent.strftime("%Y-%m-%d"),
                    obj.description,
                    obj.category,
                    obj.amount,
                    obj.balance
                ])

            to_emails = [email.strip() for email in
                         data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [
                data_obj.created_by.email]

            email = EmailMessage(
                subject=f"Petty Cash Report - {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}",
                body="Please find the attached petty cash report (Monday to Saturday).",
                from_email="noreply@mithran.co.in",
                to=to_emails,
            )
            email.attach(f"pettycash_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                         csv_buffer.getvalue(), 'text/csv')
            email.send()

            return HttpResponse("Weekly petty cash email sent successfully.")

        else:

            # Get first and last day of previous month
            first_day_this_month = tdy.replace(day=1)
            last_day_prev_month = first_day_this_month - timedelta(days=1)
            first_day_prev_month = last_day_prev_month.replace(day=1)

            expenses = PettyCashExpense.objects.filter(
                date_spent__range=(first_day_prev_month, last_day_prev_month),
                petty_school=sch
            )

            # if not expenses.exists():
            #     return HttpResponse("No petty cash records for previous month.", status=204)

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Balance'])

            for obj in expenses:
                writer.writerow([
                    obj.date_spent.strftime("%Y-%m-%d"),
                    obj.description,
                    obj.category,
                    obj.amount,
                    obj.balance
                ])

            to_emails = [email.strip() for email in
                         data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [
                data_obj.created_by.email]

            email = EmailMessage(
                subject=f"Petty Cash Report - {first_day_prev_month.strftime('%B %Y')}",
                body=f"Attached is the petty cash report from {first_day_prev_month.strftime('%d-%m-%Y')} to {last_day_prev_month.strftime('%d-%m-%Y')}.",
                from_email="noreply@mithran.co.in",
                to=to_emails,
            )
            email.attach(
                f"pettycash_{first_day_prev_month.strftime('%Y%m%d')}_{last_day_prev_month.strftime('%Y%m%d')}.csv",
                csv_buffer.getvalue(),
                'text/csv'
            )
            email.send()

            return HttpResponse("Monthly petty cash email sent successfully.")
    except Exception as e:
        print(str(e))
        return HttpResponse(f"Error: {str(e)}", status=500)


def stocks(auto_task_id):
    logger.info("Entering Stock")
    try:
        auto_task_id = auto_task_id[0]  # if it's a list
        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()
        print("schedule type:-", data_obj.schedule_type)
        # tdy = datetime.date(2024, 6, 26)
        # === DAILY EMAIL TASK ===
        if data_obj.task == "stock" and data_obj.schedule_type == "DAILY" and data_obj.automate_type == "email":
            expenses = stock.objects.filter(Prod_school=sch)

            if not expenses.exists():
                return HttpResponse("No stock records for today.", status=204)

            # Generate CSV
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Name', 'Description', 'Category', 'Balance'])

            for obj in expenses:
                writer.writerow([
                    obj.name,
                    obj.description,
                    obj.category,
                    obj.quantity

                ])

            # Prepare and send email
            email = EmailMessage(
                subject=f"Stock Report - {tdy.strftime('%d-%m-%Y')}",
                body="Please find the attached Stock report.",
                from_email="noreply@mithran.co.in",
                to=[data_obj.created_by.email],  # ensure this field exists or modify as needed
            )
            email.attach(f"stock_{tdy.strftime('%Y%m%d')}.csv", csv_buffer.getvalue(), 'text/csv')
            email.send()

            return HttpResponse("Email sent successfully.")
        elif data_obj.task == "stock" and data_obj.schedule_type == "WEEKLY" and data_obj.automate_type == "email":

            # Get current week's Monday to Saturday
            start_date = tdy - timedelta(days=tdy.weekday())  # Monday
            end_date = start_date + timedelta(days=5)  # Saturday

            expenses = stock.objects.filter(

                Prod_school=sch
            )

            # if not expenses.exists():
            #     return HttpResponse("No petty cash records for this week (Mon-Sat).", status=204)

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Name', 'Description', 'Category', 'Balance'])

            for obj in expenses:
                writer.writerow([
                    obj.name,
                    obj.description,
                    obj.category,
                    obj.quantity

                ])

            to_emails = [email.strip() for email in
                         data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [
                data_obj.created_by.email]

            email = EmailMessage(
                subject=f"Stock Report - {tdy.strftime('%d-%m-%Y')}",
                body="Please find the attached Stock report.",
                from_email="noreply@mithran.co.in",
                to=[data_obj.created_by.email],  # ensure this field exists or modify as needed
            )
            email.attach(f"stock_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                         csv_buffer.getvalue(), 'text/csv')
            email.send()

            return HttpResponse("Weekly stock email sent successfully.")

        else:

            # Get first and last day of previous month
            first_day_this_month = tdy.replace(day=1)
            last_day_prev_month = first_day_this_month - timedelta(days=1)
            first_day_prev_month = last_day_prev_month.replace(day=1)

            expenses = stock.objects.filter(

                Prod_school=sch
            )

            # if not expenses.exists():
            #     return HttpResponse("No petty cash records for previous month.", status=204)

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Name', 'Description', 'Category', 'Balance'])

            for obj in expenses:
                writer.writerow([
                    obj.name,
                    obj.description,
                    obj.category,
                    obj.quantity

                ])

            to_emails = [email.strip() for email in
                         data_obj.created_by.email.split(',')] if ',' in data_obj.created_by.email else [
                data_obj.created_by.email]

            email = EmailMessage(
                subject=f"Stock Report - {tdy.strftime('%d-%m-%Y')}",
                body="Please find the attached Stock report.",
                from_email="noreply@mithran.co.in",
                to=[data_obj.created_by.email],  # ensure this field exists or modify as needed
            )
            email.attach(
                f"stock{first_day_prev_month.strftime('%Y%m%d')}_{last_day_prev_month.strftime('%Y%m%d')}.csv",
                csv_buffer.getvalue(),
                'text/csv'
            )
            email.send()

            return HttpResponse("Monthly stock email sent successfully.")
    except Exception as e:
        print(str(e))
        return HttpResponse(f"Error: {str(e)}", status=500)


def Grievance_Report(auto_task_id):
    logger.info("Entering Grievance Automation")

    try:
        auto_task_id = auto_task_id[0]  # if passed as list
        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()

        # =============== DAILY REPORT ===============
        if data_obj.task == "grievance" and data_obj.schedule_type == "DAILY" and data_obj.automate_type == "email":

            complaints = Grievance.objects.filter(gschool=sch)

            if not complaints.exists():
                return HttpResponse("No grievance records for today.", status=204)

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Student', 'Class', 'Sec', 'Mobile', 'Area', 'Detail', 'Status', 'Complaint Date'])

            for obj in complaints:
                writer.writerow([
                    str(obj.stud_name),
                    obj.gclass,
                    obj.gsec,
                    obj.mobile,
                    obj.area_of_complaint,
                    obj.detail,
                    obj.complaint_status,
                    obj.complaint_date.strftime('%d-%m-%Y')
                ])

            email = EmailMessage(
                subject=f"Daily Grievance Report - {tdy.strftime('%d-%m-%Y')}",
                body="Please find the attached Grievance report.",
                from_email="noreply@mithran.co.in",
                to=[data_obj.created_by.email],
            )

            email.attach(f"grievance_{tdy.strftime('%Y%m%d')}.csv",
                         csv_buffer.getvalue(),
                         'text/csv')
            email.send()

            return HttpResponse("Daily Grievance email sent successfully.")

        # =============== WEEKLY REPORT ===============
        elif data_obj.task == "grievance" and data_obj.schedule_type == "WEEKLY" and data_obj.automate_type == "email":

            start_date = tdy - timedelta(days=tdy.weekday())  # Monday
            end_date = start_date + timedelta(days=5)  # Saturday

            complaints = Grievance.objects.filter(gschool=sch)

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Student', 'Class', 'Sec', 'Mobile', 'Area', 'Detail', 'Status', 'Complaint Date'])

            for obj in complaints:
                writer.writerow([
                    str(obj.stud_name),
                    obj.gclass,
                    obj.gsec,
                    obj.mobile,
                    obj.area_of_complaint,
                    obj.detail,
                    obj.complaint_status,
                    obj.complaint_date.strftime('%d-%m-%Y')
                ])

            email = EmailMessage(
                subject=f"Weekly Grievance Report - {tdy.strftime('%d-%m-%Y')}",
                body="Please find the attached weekly Grievance report.",
                from_email="noreply@mithran.co.in",
                to=[data_obj.created_by.email],
            )

            email.attach(
                f"grievance_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                csv_buffer.getvalue(),
                'text/csv'
            )
            email.send()

            return HttpResponse("Weekly Grievance email sent successfully.")

        # =============== MONTHLY REPORT ===============
        else:
            first_day_this_month = tdy.replace(day=1)
            last_day_prev_month = first_day_this_month - timedelta(days=1)
            first_day_prev_month = last_day_prev_month.replace(day=1)

            complaints = Grievance.objects.filter(gschool=sch)

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([f"School: {sch}"])
            writer.writerow(['Student', 'Class', 'Sec', 'Mobile', 'Area', 'Detail', 'Status', 'Complaint Date'])

            for obj in complaints:
                writer.writerow([
                    str(obj.stud_name),
                    obj.gclass,
                    obj.gsec,
                    obj.mobile,
                    obj.area_of_complaint,
                    obj.detail,
                    obj.complaint_status,
                    obj.complaint_date.strftime('%d-%m-%Y')
                ])

            email = EmailMessage(
                subject=f"Monthly Grievance Report - {tdy.strftime('%d-%m-%Y')}",
                body="Please find the attached monthly Grievance report.",
                from_email="noreply@mithran.co.in",
                to=[data_obj.created_by.email],
            )

            email.attach(
                f"grievance_{first_day_prev_month.strftime('%Y%m%d')}_{last_day_prev_month.strftime('%Y%m%d')}.csv",
                csv_buffer.getvalue(),
                'text/csv'
            )
            email.send()

            return HttpResponse("Monthly Grievance email sent successfully.")

    except Exception as e:
        print(str(e))
        return HttpResponse(f"Error: {str(e)}", status=500)


def Grievance_over_Due(auto_task_id):
    logger.info("Entering Overdue Grievance Report")

    try:
        auto_task_id = auto_task_id[0]  # if list
        data_obj = AutomateFunc.objects.get(id=auto_task_id)
        sch = data_obj.school
        tdy = datetime.date.today()

        # -----------------------------------
        #   FETCH ALL GRIEVANCES BY SCHOOL
        # -----------------------------------
        qs = Grievance.objects.filter(gschool=sch)
        now = datetime.datetime.now()

        # -----------------------------------
        #      OVERDUE RULES
        # -----------------------------------
        open_overdue = qs.filter(
            complaint_status="Open",
            complaint_date__lte=now - timedelta(days=2)
        )

        pending_overdue = qs.filter(
            complaint_status="Pending",
            complaint_date__lte=now - timedelta(days=3)
        )

        inprogress_overdue = qs.filter(
            complaint_status="In-progress",
            action_date__lte=now - timedelta(days=3)
        )

        # FINAL OVERDUE LIST
        overdue_list = (open_overdue | pending_overdue | inprogress_overdue).distinct()

        if not overdue_list.exists():
            return HttpResponse("No overdue grievances.", status=204)

        # -----------------------------------
        #   GENERATE CSV REPORT
        # -----------------------------------
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        writer.writerow([f"School: {sch}"])
        writer.writerow(['Student', 'Class', 'Sec', 'Mobile', 'Area',
                         'Detail', 'Status', 'Complaint Date', 'Action Date'])

        for obj in overdue_list:
            writer.writerow([
                str(obj.stud_name),
                str(obj.gclass),
                str(obj.gsec),
                obj.mobile,
                obj.area_of_complaint,
                obj.detail,
                obj.complaint_status,
                obj.complaint_date.strftime('%d-%m-%Y'),
                obj.action_date.strftime('%d-%m-%Y') if obj.action_date else ""
            ])

        # -----------------------------------
        #    SEND EMAIL
        # -----------------------------------
        email = EmailMessage(
            subject=f"Overdue Grievance Report - {tdy.strftime('%d-%m-%Y')}",
            body="Please find the attached Overdue Grievance Report.",
            from_email="noreply@mithran.co.in",
            to=[data_obj.created_by.email],
        )

        email.attach(
            f"overdue_grievance_{tdy.strftime('%Y%m%d')}.csv",
            csv_buffer.getvalue(),
            'text/csv'
        )

        email.send()

        return HttpResponse("Overdue grievance report sent successfully.")

    except Exception as e:
        print(str(e))
        return HttpResponse(f"Error: {str(e)}", status=500)


