import openai
from django.http import JsonResponse

from django.conf import settings
from django.shortcuts import render,HttpResponse
from institutions.models import school
from setup.models import currentacademicyr,academicyr

# Initialize OpenAI client
client = openai.Client(api_key=settings.OPENAI_API_KEY)

def chatbot_response(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":
                 "You are SERA, a friendly and intelligent AI assistant. "
                 "You are like a smart, caring young woman who helps users in a warm and engaging way. "
                 "Your responses should feel friendly, a bit playful, but also professional and helpful. "
                 "Always respond in a natural and conversational tone."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def chatbot_view(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_reply = chatbot_response(user_message)

        return JsonResponse({"response": bot_reply}, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    
    return render(request,"chatbot/chat.html",context={'skool':sdata,'year':year})
