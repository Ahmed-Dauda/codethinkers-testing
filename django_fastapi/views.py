from django.shortcuts import render

def frontend(request):
    return render(request, "django_fastapi/frontend.html")

import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

FASTAPI_URL = "http://127.0.0.1:8001/api/test-ai"  # your FastAPI app

@csrf_exempt
def proxy_fastapi_test(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)

        response = requests.post(
            FASTAPI_URL,
            json=data,
            headers={"Content-Type": "application/json"}
        )

        return JsonResponse(response.json(), safe=False, status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.shortcuts import render


import httpx
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # for testing
async def test_fastapi_async(request):
    message = {"html": "", "css": "", "js": ""}

    if request.method == "POST":
        prompt = request.POST.get("prompt", "Welcome to Codethinkers Academy 🚀")
        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(
                    "https://codethinkers.org/ai/generate",
                    # "http://127.0.0.1:8001/ai/generate",
                    json={"prompt": prompt}
                )
                message = r.json()
            except Exception as e:
                message = {"html": f"Error: {e}", "css": "", "js": ""}


    return render(request, "django_fastapi/test_fastapi.html", {"message": message})
