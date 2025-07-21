from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project, File
import json
from django.shortcuts import get_object_or_404, render
from .models import Folder, File

from django.http import HttpResponse
from django.utils.safestring import mark_safe

import openai
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import openai
import openai
from openai import OpenAI
import io
import contextlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Folder
import builtins
import traceback
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import File  # adjust path as needed

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import File
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from django.views.decorators.http import require_POST 
from django.contrib.auth.decorators import login_required

# views.py
from django.http import JsonResponse
from collections import defaultdict


@login_required
def create_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()

            if not name:
                return JsonResponse({'status': 'error', 'message': 'Project title is required'})

            project = Project.objects.create(user=request.user, name=name)

            index_file = File.objects.create(
                name='index.html',
                project=project,
                content="<!-- Welcome to your new project -->"
            )

            return JsonResponse({
                'status': 'success',
                'project_id': project.id,
                'file_id': index_file.id
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        user_projects = Project.objects.filter(user=request.user).order_by('-created')
        return render(request, 'webprojects/create_project.html', {
            'projects': user_projects
        })

# editor/views.py
# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import File, Project

@csrf_exempt
def upload_image_ajax(request, project_id):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image_name = request.POST.get('name', image_file.name)

        project = get_object_or_404(Project, id=project_id)

        # Create a file record with the uploaded image
        file = File.objects.create(
            project=project,
            name=image_name,
            image=image_file,
        )

        # Optionally store image URL in content
        if hasattr(file.image, 'url'):
            file.content = file.image.url
            file.save()

        return JsonResponse({
            'success': True,
            'file_id': file.id,
            'image_url': file.image.url
        })

    return JsonResponse({'success': False, 'error': 'No image uploaded'})

 
# views.py
from bs4 import BeautifulSoup

def share_preview_view(request, project_id, file_id):
    project = get_object_or_404(Project, id=project_id)
    file = get_object_or_404(File, id=file_id, project=project)

    other_files = project.files.exclude(id=file.id)

    # Separate files
    css_snippets = [f'<style>{f.content}</style>' for f in other_files if f.is_css()]
    js_snippets = [f'<script>{f.content}</script>' for f in other_files if f.is_js()]
    image_files = [f for f in other_files if f.is_image() and f.image]

    # HTML base
    html = file.content or ""

    # Inject CSS
    if '</head>' in html:
        html = html.replace('</head>', ''.join(css_snippets) + '</head>')
    else:
        html = ''.join(css_snippets) + html

    # Inject JS
    if '</body>' in html:
        html = html.replace('</body>', ''.join(js_snippets) + '</body>')
    else:
        html = html + ''.join(js_snippets)

    # Handle <img src="filename"> by replacing them with Cloudinary URLs
    soup = BeautifulSoup(html, 'html.parser')
    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src:
            # Try to find a matching image file by name
            matched_image = next((img for img in image_files if img.name == src or img.name.endswith("/" + src)), None)
            if matched_image:
                img_tag['src'] = matched_image.image.url  # Replace with Cloudinary URL

    html = str(soup)

    return render(request, 'webprojects/live_preview.html', {
        'project': project,
        'file': file,
        'rendered_html': html,
    })


# def share_preview_view(request, project_id, file_id):
#     file = get_object_or_404(File, id=file_id, project_id=project_id)
#     ext = os.path.splitext(file.name)[1].lstrip('.').lower()

#     rendered_html = ""
#     if ext == "html":
#         rendered_html = f"""
#         <!DOCTYPE html>
#         <html>
#         <head><meta charset="UTF-8"></head>
#         <body style='background:white; padding:1rem'>
#         {file.content}
#         </body>
#         </html>
#         """
#     return render(request, 'webprojects/live_preview.html', {
#         'rendered_html': rendered_html,
#         'file': file,
#         'project': file.project,
#     })


def build_folder_tree(folders):
    tree = defaultdict(list)
    for folder in folders:
        tree[folder.parent_id].append(folder)
    return tree

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    files = project.files.filter(folder__isnull=True)
    folders = project.folders.filter(parent__isnull=True)
    return render(request, 'webprojects/project_detail.html', {
        'project': project,
        'files': files,
        'folders': folders
    })



@csrf_exempt
def auto_save_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_id = data.get("file_id")
            content = data.get("content")
            file = File.objects.get(id=file_id)
            file.content = content
            file.save()
            return JsonResponse({"status": "success"})
        except File.DoesNotExist:
            return JsonResponse({"status": "error", "message": "File not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

def file_detail(request, project_id, file_id):
    file = get_object_or_404(File, id=file_id, project_id=project_id)
    files = file.project.files.all()
    project = get_object_or_404(Project, id=project_id)
    folders = Folder.objects.filter(project=file.project)

    # Group file extensions for sidebar
    exts = sorted({
        os.path.splitext(f.name)[1].lstrip('.').lower()
        for f in files if '.' in f.name
    })

    # ✅ Detect if file is an image
    is_image = file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if data.get("file_id") and data.get("file_id") != file.id:
                return JsonResponse({"error": "Mismatched file ID"}, status=400)

            new_content = data.get("content", "")
            updated_timestamp = data.get("timestamp")
            run_plot = data.get("run_plot", False)

            if updated_timestamp:
                from django.utils.dateparse import parse_datetime
                new_time = parse_datetime(updated_timestamp)
                if new_time and new_time < file.updated:
                    return JsonResponse({
                        "status": "skipped",
                        "message": "Stale update ignored."
                    })

            file.content = new_content
            file.save()

            # ✅ Python execution block
            if run_plot and file.name.lower().endswith(".py"):
                import contextlib
                import sys

                buffer_out = io.StringIO()
                plt.clf()
                plt.close('all')

                local_vars = {}

                try:
                    with contextlib.redirect_stdout(buffer_out):
                        exec(new_content, {}, local_vars)

                    printed_output = buffer_out.getvalue()

                    # Capture DataFrame (if any)
                    table_html = ""
                    for var in local_vars.values():
                        if isinstance(var, pd.DataFrame):
                            table_html = var.to_html(classes="table table-bordered", index=False)
                            break

                    # Capture matplotlib plots
                    images = []
                    for i in plt.get_fignums():
                        fig = plt.figure(i)
                        buffer = io.BytesIO()
                        fig.savefig(buffer, format='png', bbox_inches='tight')
                        plt.close(fig)
                        buffer.seek(0)
                        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
                        images.append(f"data:image/png;base64,{img_base64}")

                    return JsonResponse({
                        "status": "plot_generated",
                        "images": images,
                        "output": printed_output or "[No output]",
                        "table": table_html
                    })

                except Exception as e:
                    return JsonResponse({"status": "error", "message": str(e)}, status=500)

            return JsonResponse({"status": "saved", "message": "File saved successfully."})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return render(request, 'webprojects/file_detail.html', {
        'file': file,
        'files': files,
        'folders': folders,
        'exts': exts,
        'project': project,
        'is_image': is_image,  # ✅ Pass to template
    })


def view_rendered_file(request, file_id):
    file = get_object_or_404(File, id=file_id)

    if file.name.endswith('.html'):
        return HttpResponse(file.content)
    elif file.name.endswith('.js'):
        return HttpResponse(file.content, content_type="application/javascript")
    elif file.name.endswith('.css'):
        return HttpResponse(file.content, content_type="text/css")
    else:
        return HttpResponse("Preview not supported for this file type.")


def public_folder_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    files = folder.files.all()  # This will work only if File has a ForeignKey to Folder
    return render(request, 'webprojects/public_folder_view.html', {
        'folder': folder,
        'files': files
    })

 

@csrf_exempt  # Use only if you haven't handled CSRF with JS token yet
def create_file(request, project_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            folder_id = data.get("folder_id")

            project = Project.objects.get(id=project_id)
            folder = Folder.objects.get(id=folder_id) if folder_id else None

            new_file = File.objects.create(
                name=name,
                project=project,
                folder=folder
            )

            return JsonResponse({
                "status": "success",
                "file_id": new_file.id,
                "file_name": new_file.name
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)
    

@require_POST
@login_required
def create_folder(request, project_id):
    try:
        data = json.loads(request.body)
        name = data.get("name")
        parent_id = data.get("parent_id")  # NEW!
        project = get_object_or_404(Project, id=project_id)

        if not name:
            return JsonResponse({"status": "error", "message": "Folder name is required"})

        parent_folder = None
        if parent_id:
            parent_folder = Folder.objects.get(id=parent_id)

        folder = Folder.objects.create(
            name=name,
            project=project,
            parent=parent_folder  # SET NESTING HERE
        )

 
        return JsonResponse({"status": "success", "folder_id": folder.id, "folder_name": folder.name})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# Use your actual OpenAI API key here
# openai.api_key = "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"

client = OpenAI(api_key="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")

@csrf_exempt
def ai_suggest_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "").strip()
            if not prompt:
                return JsonResponse({"error": "Prompt is empty"}, status=400)

            # Inside ai_suggest_code view:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert programmer. When the user gives code, you complete it directly without explanation or questions. Do not ask the user what to do — just complete the code."
                    },
                    {
                        "role": "user",
                        "content": f"Complete this code:\n{prompt}"
                    }
                ],
                max_tokens=150,
                temperature=0.3
            )

            suggestion = response.choices[0].message.content.strip()
            return JsonResponse({"suggestion": suggestion})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def explain_code_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "").strip()
            if not code:
                return JsonResponse({"error": "Code is empty"}, status=400)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert coding teacher. Explain code clearly."},
                    {"role": "user", "content": f"Explain this code:\n{code}"}
                ],
                max_tokens=250,
                temperature=0.4
            )
            explanation = response.choices[0].message.content.strip()
            return JsonResponse({"explanation": explanation})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=405)



@csrf_exempt
def ai_python_completion(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        data = json.loads(request.body)
        prefix = data.get("prefix", "").strip()

        if not prefix or not prefix.isidentifier():
            return JsonResponse({"error": "Invalid prefix"}, status=400)

        prompt = (
            f"List 30 Python keywords, functions, or methods that typically start with '{prefix}'. "
            f"Just return one per line without explanation."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        completions = [line.strip() for line in content.splitlines() if line.strip()]

        return JsonResponse({"completions": completions})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
       

@csrf_exempt
def run_python_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')

            # Set up in-memory output capture
            stdout = io.StringIO()
            stderr = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                with contextlib.redirect_stderr(stderr):
                    try:
                        exec(code, {})
                    except Exception:
                        traceback.print_exc(file=stderr)

            output = stdout.getvalue()
            error = stderr.getvalue()

            return JsonResponse({'output': output, 'error': error})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)    
