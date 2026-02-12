from django.shortcuts import render, redirect
from institutions.models import school
from setup.models import academicyr, currentacademicyr
from authenticate.decorators import allowed_users
from .models import fee_automate_report, AutomateFunc
from django.contrib import messages
from datetime import timedelta
from .forms import AutomateFuncForm
from django_q.models import Schedule
from datetime import datetime, date
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time

NODE_SERVER_URL = "http://localhost:3000/send-message"  # Change if running on AWS like http://mac.in/send-message


# Create your views here.

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def fee_automate_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = fee_automate_report.objects.filter(report_school=sdata)
    return render(request, 'automate/fee_automate_list.html', context={'skool': sdata, 'year': year, 'data': data})


def automate_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = AutomateFunc.objects.filter(school=sdata)
    return render(request, 'automate/automate_list.html', context={'skool': sdata, 'year': year, 'data': data})


def add_automate_task(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    usr = request.user
    initial_data = {
        'school': sdata,
        'created_by': usr,

    }
    if request.method == 'POST':
        form = AutomateFuncForm(request.POST)
        if form.is_valid():
            auto_task = form.save(commit=False)
            auto_task.save()
            time_str = request.POST.get('schedule_time')  # '16:00'
            today = date.today()
            run_time = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M")
            temp = request.POST.get('schedule_type')
            if temp == "DAILY":
                sch = Schedule.DAILY
            elif temp == "WEEKLY":
                sch = Schedule.WEEKLY
                # Schedule for next Saturday
                weekday = today.weekday()  # Monday = 0, Saturday = 5
                days_until_saturday = (5 - weekday) % 7
                run_date = today + timedelta(days=days_until_saturday or 7)
            else:
                sch = Schedule.MONTHLY
                if today.month == 12:
                    run_date = date(today.year + 1, 1, 1)
                else:
                    run_date = date(today.year, today.month + 1, 1)
            func = "automate.tasks." + auto_task.task

            Schedule.objects.create(
                func=func,
                schedule_type=sch,
                next_run=run_time,
                repeats=-1,
                args=[auto_task.id]
            )

            return redirect('automate_list')  # redirect to the list view or a success page

    form = AutomateFuncForm(initial=initial_data)
    return render(request, 'automate/add_task.html', {'form': form, 'skool': sdata, 'year': year})


def send_whatsapp_message(request):
    # Hardcoded test numbers and message
    numbers = ["919047621499", "918012998375"]
    message = "Hello! This is a test message from Django URL"
    delay_seconds = 5

    results = []

    for phone in numbers:
        payload = {"phone": phone, "message": message}
        try:
            response = requests.post(NODE_SERVER_URL, json=payload, timeout=10)

            # Check if response is valid JSON
            try:
                result_json = response.json()
            except:
                result_json = {"status": "error", "error": "Node server returned invalid response"}

            results.append({phone: result_json})
        except Exception as e:
            results.append({phone: f"Failed to send - {str(e)}"})

        print(f"Waiting {delay_seconds} seconds before next message...")
        time.sleep(delay_seconds)

    return JsonResponse({"status": "done", "results": results})

def delete_automate_task(request, task_id):
    auto_task = AutomateFunc.objects.get(id=task_id)

    # delete related schedule
    Schedule.objects.filter(args=[auto_task.id]).delete()

    # delete task
    auto_task.delete()
    messages.success(request,"Automation Deleted Successfully")
    return redirect('automate_list')
