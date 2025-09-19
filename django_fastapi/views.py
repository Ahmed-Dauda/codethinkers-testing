import httpx
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from asgiref.sync import sync_to_async

FASTAPI_URL = "https://fastapi-service-tk85.onrender.com/"


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


import httpx
from django.shortcuts import render

async def async_program_pages_list_view(request):
    pages = []
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            # response = await client.get("http://127.0.0.1:8010/api/program-pages")
            response = await client.get("https://fastapi-service-tk85.onrender.com/api/program-pages")
            if response.status_code == 200:
                pages = response.json()
            else:
                pages = [{"title": f"FastAPI error {response.status_code}", "description": "", "benefits": ""}]
    except httpx.RequestError as e:
        pages = [{"title": f"Error fetching FastAPI data: {e}", "description": "", "benefits": ""}]

    return render(request, "django_fastapi/program_pages_list.html", {"pages": pages})



# async def async_program_pages_list_view(request):
#     pages = []
#     try:
#         async with httpx.AsyncClient(timeout=5) as client:
#             response = await client.get("http://127.0.0.1:8001/api/program-pages")
#             # response = await client.get("https://fastapi-service-tk85.onrender.com/api/program-pages")
#             if response.status_code == 200:
#                 pages = response.json()
#     except Exception as e:
#         pages = [{"title": f"Error fetching FastAPI data: {e}", "subtitle": "", "description": "", "cta_text": "", "benefits": []}]

#     return render(request, "django_fastapi/program_pages_list.html", {"pages": pages})
