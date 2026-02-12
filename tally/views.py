from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import decorator_from_middleware
from django.http import JsonResponse
import xml.etree.ElementTree as ET

@csrf_exempt
@login_required
def receive_tally_data(request):
    if request.method == "POST":
        xml_data = request.POST.get("xml") or request.body.decode("utf-8")
        try:
            root = ET.fromstring(xml_data)
            # parse and store in database here
            return JsonResponse({"message": "Tally data received"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)