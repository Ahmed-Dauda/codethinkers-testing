import httpx
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
FASTAPI_URL = "https://fastapi-service-tk85.onrender.com/"




import httpx
from django.shortcuts import render
from asgiref.sync import sync_to_async

async def test_fastapi(request):
    message = "Error: could not connect to FastAPI"
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://fastapi-service-tk85.onrender.com/welcome")
            data = r.json()
            message = data.get("message", message)
    except Exception as e:
        message = f"Error: {e}"

    return render(request, "django_fastapi/test_fastapi.html", {"message": message})


import httpx
import asyncio
from django.http import JsonResponse

async def test_async_speed(request):
    urls = [
        "https://fastapi-service-tk85.onrender.com/slow",
        "https://fastapi-service-tk85.onrender.com/slow",
        "https://fastapi-service-tk85.onrender.com/slow",
    ]

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)

    data = [r.json() for r in responses]
    return JsonResponse({"results": data})
