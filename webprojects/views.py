from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project, File
import json
from django.shortcuts import get_object_or_404, render
from .models import Folder, File
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import File, Project

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
from sms.models import Topics

import os
import pandas as pd
from django.conf import settings


import os
import io
import json
import base64
import traceback
import contextlib
import pandas as pd
import matplotlib.pyplot as plt

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.conf import settings
from .models import File, Project, Folder
client = OpenAI(api_key=settings.OPENAI_API_KEY) 

@login_required
def create_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()

            if not name:
                return JsonResponse({'status': 'error', 'message': 'Project name is required'})

            # Check for existing project by name (per user)
            existing_project = Project.objects.filter(user=request.user, name=name).first()
            if existing_project:
                first_file = existing_project.files.first()
                return JsonResponse({
                    'status': 'success',
                    'project_id': existing_project.id,
                    'file_id': first_file.id if first_file else None
                })

            # Auto-detect file extension
            lower_name = name.lower()
            if "python" in lower_name:
                ext = ".py"
                default_content = "# Start your Python code here"
            elif "html" in lower_name:
                ext = ".html"
                default_content = "<!-- Start writing HTML here -->"
            elif "css" in lower_name:
                ext = ".css"
                default_content = "/* Write your CSS here */"
            elif "js" in lower_name or "javascript" in lower_name:
                ext = ".js"
                default_content = "// JavaScript starts here"
            else:
                ext = ".txt"
                default_content = "// General notes"

            project = Project.objects.create(user=request.user, name=name)

            file = File.objects.create(
                name='main' + ext,
                project=project,
                content=default_content
            )

            return JsonResponse({
                'status': 'success',
                'project_id': project.id,
                'file_id': file.id
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
@csrf_exempt
def upload_file_ajax(request, project_id):
    if request.method == 'POST' and request.FILES.get('file'):
        upload = request.FILES['file']
        file_name = request.POST.get('name', upload.name)
        ext = os.path.splitext(file_name)[1].lower().replace('.', '')

        project = get_object_or_404(Project, id=project_id)

        # Decide where to save: CloudinaryField (image) or FileField (other)
        if ext in ["jpg", "jpeg", "png", "gif", "svg", "webp"]:
            file = File.objects.create(
                project=project,
                name=file_name,
                image=upload  # goes to Cloudinary
            )
        else:
            file = File.objects.create(
                project=project,
                name=file_name,
                file=upload  # goes to local FileField
            )

        return JsonResponse({
            'success': True,
            'file_id': file.id,
            'file_url': file.file_url(),
            'ext': ext,
        })

    return JsonResponse({'success': False, 'error': 'No file uploaded'})


# @csrf_exempt
# def upload_image_ajax(request, project_id):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES['image']
#         image_name = request.POST.get('name', image_file.name)

#         project = get_object_or_404(Project, id=project_id)

#         # Create a file record with the uploaded image
#         file = File.objects.create(
#             project=project,
#             name=image_name,
#             image=image_file,
#         )

#         # Optionally store image URL in content
#         if hasattr(file.image, 'url'):
#             file.content = file.image.url
#             file.save()

#         return JsonResponse({
#             'success': True,
#             'file_id': file.id,
#             'image_url': file.image.url
#         })

#     return JsonResponse({'success': False, 'error': 'No image uploaded'})




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




def file_preview(request, project_id, file_id):
    file = get_object_or_404(File, id=file_id, project_id=project_id)

    if not file.is_excel():
        return render(request, "webprojects/preview_error.html", {"message": "File type not supported for preview."})

    # Full path
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))

    # Read the file
    try:
        if file.extension() == "csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        return render(request, "webprojects/preview_error.html", {"message": str(e)})

    # Limit rows for preview
    preview_df = df.head(20)

    return render(request, "webprojects/file_preview.html", {
        "file": file,
        "df_html": preview_df.to_html(classes="table table-bordered table-sm", index=False)
    })


def file_delete(request, project_id, file_id):
    if request.method == "POST":
        file = get_object_or_404(File, id=file_id, project_id=project_id)
        file.delete()  # This triggers post_delete and removes the file physically
        return JsonResponse({"status": "success", "message": "File deleted."})
    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)


def project_files_json(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    html_file = project.files.filter(name="index.html").first()
    css_file = project.files.filter(name="style.css").first()
    js_file = project.files.filter(name="script.js").first()

    return JsonResponse({
        "html": html_file.content if html_file else "",
        "css": css_file.content if css_file else "",
        "js": js_file.content if js_file else "",
    })
   


def file_detail(request, project_id, file_id):
    file = get_object_or_404(File, id=file_id, project_id=project_id)
    files = file.project.files.all()
    project = get_object_or_404(Project, id=project_id)
    folders = Folder.objects.filter(project=file.project)

    # Sidebar file extensions
    exts = sorted({os.path.splitext(f.name)[1].lstrip('.').lower() for f in files if '.' in f.name})

    # Detect if file is an image
    is_image = file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

    # Full path to the file
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))

    if request.method == 'POST':
        try:
            data = json.loads(request.body or "{}")
            new_content = data.get("content", "")
            run_plot = data.get("run_plot", False)
            run_table = data.get("run_table", False)
            prompt = data.get("prompt", "")  # Safe access
            # ===== AI Prompt Handling =====
            if prompt:
                try:
                    # ✅ Fetch existing files (create empty ones if missing)
                    html_file, _ = File.objects.get_or_create(project=project, name="index.html")
                    css_file, _ = File.objects.get_or_create(project=project, name="style.css")
                    js_file, _ = File.objects.get_or_create(project=project, name="script.js")

                    # ✅ System instruction (force JSON output only)
                    system_message = (
                        "You are an expert web developer. Update the given HTML, CSS, and JS project "
                        "based on the user's request. Only modify what is necessary. "
                        "Always return a VALID JSON object with keys: html, css, js. "
                        "Do NOT include explanations, markdown, or extra text. "
                        "Example: {\"html\": \"<h1>Hello</h1>\", \"css\": \"body {color:red;}\", \"js\": \"console.log('hi');\"}"
                    )

                    # ✅ Include current project state
                    user_message = f"""
                    Current project:
                    HTML:
                    {html_file.content}

                    CSS:
                    {css_file.content}

                    JS:
                    {js_file.content}

                    User request:
                    {prompt}
                    """

                    response = client.chat.completions.create(
                        model="gpt-4.1",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=4000,
                        temperature=0
                    )

                    ai_text = response.choices[0].message.content.strip()

                    # 🛡️ Extract only JSON portion
                    start = ai_text.find("{")
                    end = ai_text.rfind("}")
                    if start != -1 and end != -1:
                        ai_text = ai_text[start:end+1]

                    # 🛡️ Try parsing JSON safely
                    try:
                        ai_generated = json.loads(ai_text)
                    except json.JSONDecodeError:
                        cleaned = ai_text.replace("\n", " ").replace("\r", " ").strip()
                        try:
                            ai_generated = json.loads(cleaned)
                        except Exception:
                            ai_generated = {"html": ai_text, "css": "", "js": ""}

                    # ✅ Update only if AI returned something new
                    if ai_generated.get("html"):
                        html_file.content = ai_generated["html"]
                        html_file.save()

                    if ai_generated.get("css"):
                        css_file.content = ai_generated["css"]
                        css_file.save()

                    if ai_generated.get("js"):
                        js_file.content = ai_generated["js"]
                        js_file.save()

                    return JsonResponse({
                        "status": "success",
                        "ai_content": ai_generated,
                        "message": "AI project updated and saved into index.html, style.css, script.js"
                    })

                except Exception as e:
                    return JsonResponse({
                        "status": "error",
                        "message": str(e),
                        "trace": traceback.format_exc()
                    }, status=500)
            # ===== End AI Prompt =====

            # Prevent mismatched file updates
            if data.get("file_id") and data.get("file_id") != file.id:
                return JsonResponse({"error": "Mismatched file ID"}, status=400)

            # Save new content
            if new_content:
                file.content = new_content
                file.save()

            ext = file.name.lower().split(".")[-1]
            response_table = ""
            images = []

            # CSV/Excel handling
            df = None
            if ext in ["csv", "xls", "xlsx"]:
                try:
                    if ext == "csv":
                        df = pd.read_csv(file_path)
                    else:
                        df = pd.read_excel(file_path)
                    if run_table:
                        response_table = df.head(20).to_html(
                            classes="table table-bordered table-sm",
                            index=False
                        )
                except Exception as e:
                    return JsonResponse({"status": "error", "message": str(e)}, status=500)

            # Python execution (mini Jupyter)
            if run_plot or new_content.strip():
                buffer_out = io.StringIO()
                buffer_err = io.StringIO()
                plt.clf()
                plt.close('all')

                if not hasattr(pd, "_original_read_csv"):
                    pd._original_read_csv = pd.read_csv
                if not hasattr(pd, "_original_read_excel"):
                    pd._original_read_excel = pd.read_excel

                def patched_read_csv(name, *args, **kwargs):
                    path = os.path.join(settings.MEDIA_ROOT, 'uploads', name)
                    return pd._original_read_csv(path, *args, **kwargs)

                def patched_read_excel(name, *args, **kwargs):
                    path = os.path.join(settings.MEDIA_ROOT, 'uploads', name)
                    return pd._original_read_excel(path, *args, **kwargs)

                pd.read_csv = patched_read_csv
                pd.read_excel = patched_read_excel

                def fake_show(*args, **kwargs):
                    buf = io.BytesIO()
                    plt.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)
                    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
                    images.append(f"data:image/png;base64,{img_base64}")
                    plt.close()

                plt.show = fake_show

                try:
                    with contextlib.redirect_stdout(buffer_out), contextlib.redirect_stderr(buffer_err):
                        exec(new_content, {"pd": pd})

                    printed_output = buffer_out.getvalue()
                    error_output = buffer_err.getvalue()
                    if error_output:
                        return JsonResponse({"status": "error", "message": error_output}, status=500)

                    for i in plt.get_fignums():
                        fig = plt.figure(i)
                        buf = io.BytesIO()
                        fig.savefig(buf, format="png", bbox_inches="tight")
                        buf.seek(0)
                        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
                        images.append(f"data:image/png;base64,{img_base64}")
                        plt.close(fig)

                    return JsonResponse({
                        "status": "success",
                        "output": printed_output or "[No output]",
                        "table": response_table,
                        "images": images
                    })
                except Exception:
                    return JsonResponse({"status": "error", "message": traceback.format_exc()}, status=500)

            # Default save response
            return JsonResponse({"status": "saved", "message": "File saved successfully."})

        except Exception:
            return JsonResponse({"status": "error", "message": traceback.format_exc()}, status=500)

    # GET request
    return render(request, 'webprojects/file_detail.html', {
        'file': file,
        'files': files,
        'folders': folders,
        'exts': exts,
        'project': project,
        'is_image': is_image,
    })



#working code

# def file_detail(request, project_id, file_id):
#     file = get_object_or_404(File, id=file_id, project_id=project_id)
#     files = file.project.files.all()
#     project = get_object_or_404(Project, id=project_id)
#     folders = Folder.objects.filter(project=file.project)

#     # Sidebar file extensions
#     exts = sorted({os.path.splitext(f.name)[1].lstrip('.').lower() for f in files if '.' in f.name})

#     # Detect if file is an image
#     is_image = file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

#     # Full path to the file
#     file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body or "{}")
#             new_content = data.get("content", "")
#             run_plot = data.get("run_plot", False)
#             run_table = data.get("run_table", False)
#             prompt = data.get("prompt", "")  # Safe access
#             # ===== AI Prompt Handling =====
#             if prompt:
#                 try:
#                     # ✅ Fetch existing files (create empty ones if missing)
#                     html_file, _ = File.objects.get_or_create(project=project, name="index.html")
#                     css_file, _ = File.objects.get_or_create(project=project, name="style.css")
#                     js_file, _ = File.objects.get_or_create(project=project, name="script.js")

#                     # ✅ System instruction (force JSON output only)
#                     system_message = (
#                         "You are an expert web developer. Update the given HTML, CSS, and JS project "
#                         "based on the user's request. Only modify what is necessary. "
#                         "Always return a VALID JSON object with keys: html, css, js. "
#                         "Do NOT include explanations, markdown, or extra text. "
#                         "Example: {\"html\": \"<h1>Hello</h1>\", \"css\": \"body {color:red;}\", \"js\": \"console.log('hi');\"}"
#                     )

#                     # ✅ Include current project state
#                     user_message = f"""
#                     Current project:
#                     HTML:
#                     {html_file.content}

#                     CSS:
#                     {css_file.content}

#                     JS:
#                     {js_file.content}

#                     User request:
#                     {prompt}
#                     """

#                     response = client.chat.completions.create(
#                         model="gpt-4.1",
#                         messages=[
#                             {"role": "system", "content": system_message},
#                             {"role": "user", "content": user_message}
#                         ],
#                         max_tokens=4000,
#                         temperature=0
#                     )

#                     ai_text = response.choices[0].message.content.strip()

#                     # 🛡️ Extract only JSON portion
#                     start = ai_text.find("{")
#                     end = ai_text.rfind("}")
#                     if start != -1 and end != -1:
#                         ai_text = ai_text[start:end+1]

#                     # 🛡️ Try parsing JSON safely
#                     try:
#                         ai_generated = json.loads(ai_text)
#                     except json.JSONDecodeError:
#                         cleaned = ai_text.replace("\n", " ").replace("\r", " ").strip()
#                         try:
#                             ai_generated = json.loads(cleaned)
#                         except Exception:
#                             ai_generated = {"html": ai_text, "css": "", "js": ""}

#                     # ✅ Update only if AI returned something new
#                     if ai_generated.get("html"):
#                         html_file.content = ai_generated["html"]
#                         html_file.save()

#                     if ai_generated.get("css"):
#                         css_file.content = ai_generated["css"]
#                         css_file.save()

#                     if ai_generated.get("js"):
#                         js_file.content = ai_generated["js"]
#                         js_file.save()

#                     return JsonResponse({
#                         "status": "success",
#                         "ai_content": ai_generated,
#                         "message": "AI project updated and saved into index.html, style.css, script.js"
#                     })

#                 except Exception as e:
#                     return JsonResponse({
#                         "status": "error",
#                         "message": str(e),
#                         "trace": traceback.format_exc()
#                     }, status=500)
#             # ===== End AI Prompt =====

#             # Prevent mismatched file updates
#             if data.get("file_id") and data.get("file_id") != file.id:
#                 return JsonResponse({"error": "Mismatched file ID"}, status=400)

#             # Save new content
#             if new_content:
#                 file.content = new_content
#                 file.save()

#             ext = file.name.lower().split(".")[-1]
#             response_table = ""
#             images = []

#             # CSV/Excel handling
#             df = None
#             if ext in ["csv", "xls", "xlsx"]:
#                 try:
#                     if ext == "csv":
#                         df = pd.read_csv(file_path)
#                     else:
#                         df = pd.read_excel(file_path)
#                     if run_table:
#                         response_table = df.head(20).to_html(
#                             classes="table table-bordered table-sm",
#                             index=False
#                         )
#                 except Exception as e:
#                     return JsonResponse({"status": "error", "message": str(e)}, status=500)

#             # Python execution (mini Jupyter)
#             if run_plot or new_content.strip():
#                 buffer_out = io.StringIO()
#                 buffer_err = io.StringIO()
#                 plt.clf()
#                 plt.close('all')

#                 if not hasattr(pd, "_original_read_csv"):
#                     pd._original_read_csv = pd.read_csv
#                 if not hasattr(pd, "_original_read_excel"):
#                     pd._original_read_excel = pd.read_excel

#                 def patched_read_csv(name, *args, **kwargs):
#                     path = os.path.join(settings.MEDIA_ROOT, 'uploads', name)
#                     return pd._original_read_csv(path, *args, **kwargs)

#                 def patched_read_excel(name, *args, **kwargs):
#                     path = os.path.join(settings.MEDIA_ROOT, 'uploads', name)
#                     return pd._original_read_excel(path, *args, **kwargs)

#                 pd.read_csv = patched_read_csv
#                 pd.read_excel = patched_read_excel

#                 def fake_show(*args, **kwargs):
#                     buf = io.BytesIO()
#                     plt.savefig(buf, format="png", bbox_inches="tight")
#                     buf.seek(0)
#                     img_base64 = base64.b64encode(buf.read()).decode("utf-8")
#                     images.append(f"data:image/png;base64,{img_base64}")
#                     plt.close()

#                 plt.show = fake_show

#                 try:
#                     with contextlib.redirect_stdout(buffer_out), contextlib.redirect_stderr(buffer_err):
#                         exec(new_content, {"pd": pd})

#                     printed_output = buffer_out.getvalue()
#                     error_output = buffer_err.getvalue()
#                     if error_output:
#                         return JsonResponse({"status": "error", "message": error_output}, status=500)

#                     for i in plt.get_fignums():
#                         fig = plt.figure(i)
#                         buf = io.BytesIO()
#                         fig.savefig(buf, format="png", bbox_inches="tight")
#                         buf.seek(0)
#                         img_base64 = base64.b64encode(buf.read()).decode("utf-8")
#                         images.append(f"data:image/png;base64,{img_base64}")
#                         plt.close(fig)

#                     return JsonResponse({
#                         "status": "success",
#                         "output": printed_output or "[No output]",
#                         "table": response_table,
#                         "images": images
#                     })
#                 except Exception:
#                     return JsonResponse({"status": "error", "message": traceback.format_exc()}, status=500)

#             # Default save response
#             return JsonResponse({"status": "saved", "message": "File saved successfully."})

#         except Exception:
#             return JsonResponse({"status": "error", "message": traceback.format_exc()}, status=500)

#     # GET request
#     return render(request, 'webprojects/file_detail.html', {
#         'file': file,
#         'files': files,
#         'folders': folders,
#         'exts': exts,
#         'project': project,
#         'is_image': is_image,
#     })


# views.py
def load_project_files(request, project_id):
    try:
        project = Project.objects.get(id=project_id)

        html_file = File.objects.filter(project=project, name="index.html").first()
        css_file = File.objects.filter(project=project, name="style.css").first()
        js_file = File.objects.filter(project=project, name="script.js").first()

        return JsonResponse({
            "status": "success",
            "html": html_file.content if html_file else "",
            "css": css_file.content if css_file else "",
            "js": js_file.content if js_file else ""
        })
    except Project.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Project not found"}, status=404)


# working before adding ai prompt    
# def file_detail(request, project_id, file_id):
#     file = get_object_or_404(File, id=file_id, project_id=project_id)
#     files = file.project.files.all()
#     project = get_object_or_404(Project, id=project_id)
#     folders = Folder.objects.filter(project=file.project)

#     # Sidebar file extensions
#     exts = sorted({
#         os.path.splitext(f.name)[1].lstrip('.').lower()
#         for f in files if '.' in f.name
#     })

#     # Detect if file is an image
#     is_image = file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

#     # Full path to the file
#     file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))

#     # ai prompts
#     # end ai prompt

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body or "{}")
#             new_content = data.get("content", "")
#             run_plot = data.get("run_plot", False)
#             run_table = data.get("run_table", False)

#             # Prevent mismatched file updates
#             if data.get("file_id") and data.get("file_id") != file.id:
#                 return JsonResponse({"error": "Mismatched file ID"}, status=400)

#             # Save content for text-based files
#             if new_content:
#                 file.content = new_content
#                 file.save()

#             ext = file.name.lower().split(".")[-1]
#             response_table = ""
#             images = []

#             # Automatically load CSV/Excel as df
#             df = None
#             if ext in ["csv", "xls", "xlsx"]:
#                 try:
#                     if ext == "csv":
#                         df = pd.read_csv(file_path)
#                     else:
#                         df = pd.read_excel(file_path)
#                     if run_table:
#                         response_table = df.head(20).to_html(
#                             classes="table table-bordered table-sm",
#                             index=False
#                         )
#                 except Exception as e:
#                     return JsonResponse({"status": "error", "message": str(e)}, status=500)

#             # Execute Python code (mini Jupyter)
#             if run_plot or new_content.strip():
#                 buffer_out = io.StringIO()
#                 buffer_err = io.StringIO()
#                 plt.clf()
#                 plt.close('all')

#                 # Save original pandas functions
#                 # Save the original functions once
#                 if not hasattr(pd, "_original_read_csv"):
#                     pd._original_read_csv = pd.read_csv
#                 if not hasattr(pd, "_original_read_excel"):
#                     pd._original_read_excel = pd.read_excel

#                 # Patch read_csv and read_excel
#                 def patched_read_csv(name, *args, **kwargs):
#                     path = os.path.join(settings.MEDIA_ROOT, 'uploads', name)
#                     return pd._original_read_csv(path, *args, **kwargs)

#                 def patched_read_excel(name, *args, **kwargs):
#                     path = os.path.join(settings.MEDIA_ROOT, 'uploads', name)
#                     return pd._original_read_excel(path, *args, **kwargs)

#                 # Use patched versions inside exec
#                 local_vars = {"pd": pd}
#                 pd.read_csv = patched_read_csv
#                 pd.read_excel = patched_read_excel

#                 # Monkeypatch plt.show to save plots
#                 def fake_show(*args, **kwargs):
#                     buf = io.BytesIO()
#                     plt.savefig(buf, format="png", bbox_inches="tight")
#                     buf.seek(0)
#                     img_base64 = base64.b64encode(buf.read()).decode("utf-8")
#                     images.append(f"data:image/png;base64,{img_base64}")
#                     plt.close()

#                 plt.show = fake_show

#                 try:
#                     with contextlib.redirect_stdout(buffer_out), contextlib.redirect_stderr(buffer_err):
#                         exec(new_content, local_vars)

#                     printed_output = buffer_out.getvalue()
#                     error_output = buffer_err.getvalue()

#                     if error_output:
#                         return JsonResponse({
#                             "status": "error",
#                             "message": error_output
#                         }, status=500)

#                     # Capture open matplotlib figures
#                     for i in plt.get_fignums():
#                         fig = plt.figure(i)
#                         buf = io.BytesIO()
#                         fig.savefig(buf, format="png", bbox_inches="tight")
#                         buf.seek(0)
#                         img_base64 = base64.b64encode(buf.read()).decode("utf-8")
#                         images.append(f"data:image/png;base64,{img_base64}")
#                         plt.close(fig)

#                     return JsonResponse({
#                         "status": "success",
#                         "output": printed_output or "[No output]",
#                         "table": response_table,
#                         "images": images
#                     })

#                 except Exception:
#                     return JsonResponse({
#                         "status": "error",
#                         "message": traceback.format_exc()
#                     }, status=500)

#             # Default response
#             return JsonResponse({"status": "saved", "message": "File saved successfully."})

#         except Exception:
#             return JsonResponse({"status": "error", "message": traceback.format_exc()}, status=500)

#     # GET request
#     return render(request, 'webprojects/file_detail.html', {
#         'file': file,
#         'files': files,
#         'folders': folders,
#         'exts': exts,
#         'project': project,
#         'is_image': is_image,
#     })


# def file_detail(request, project_id, file_id):
#     file = get_object_or_404(File, id=file_id, project_id=project_id)
#     files = file.project.files.all()
#     project = get_object_or_404(Project, id=project_id)
#     folders = Folder.objects.filter(project=file.project)

#     # Group file extensions for sidebar
#     exts = sorted({
#         os.path.splitext(f.name)[1].lstrip('.').lower()
#         for f in files if '.' in f.name
#     })

#     # ✅ Detect if file is an image
#     is_image = file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             if data.get("file_id") and data.get("file_id") != file.id:
#                 return JsonResponse({"error": "Mismatched file ID"}, status=400)

#             new_content = data.get("content", "")
#             updated_timestamp = data.get("timestamp")
#             run_plot = data.get("run_plot", False)

#             if updated_timestamp:
#                 from django.utils.dateparse import parse_datetime
#                 new_time = parse_datetime(updated_timestamp)
#                 if new_time and new_time < file.updated:
#                     return JsonResponse({
#                         "status": "skipped",
#                         "message": "Stale update ignored."
#                     })

#             file.content = new_content
#             file.save()

#             # ✅ Execute Python if requested
#             if run_plot and file.name.lower().endswith(".py"):
#                 buffer_out = io.StringIO()
#                 buffer_err = io.StringIO()
#                 plt.clf()
#                 plt.close('all')

#                 local_vars = {}

#                 try:
#                     with contextlib.redirect_stdout(buffer_out), contextlib.redirect_stderr(buffer_err):
#                         exec(new_content, {}, local_vars)

#                     printed_output = buffer_out.getvalue()
#                     error_output = buffer_err.getvalue()

#                     # Return error if there was stderr
#                     if error_output:
#                         return JsonResponse({
#                             "status": "error",
#                             "message": error_output
#                         }, status=500)

#                     # Capture DataFrame (if any)
#                     table_html = ""
#                     for var in local_vars.values():
#                         if isinstance(var, pd.DataFrame):
#                             table_html = var.to_html(classes="table table-bordered", index=False)
#                             break

#                     # Capture matplotlib plots
#                     images = []
#                     for i in plt.get_fignums():
#                         fig = plt.figure(i)
#                         buffer = io.BytesIO()
#                         fig.savefig(buffer, format='png', bbox_inches='tight')
#                         plt.close(fig)
#                         buffer.seek(0)
#                         img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
#                         images.append(f"data:image/png;base64,{img_base64}")

#                     return JsonResponse({
#                         "status": "plot_generated",
#                         "images": images,
#                         "output": printed_output or "[No output]",
#                         "table": table_html
#                     })

#                 except Exception:
#                     # Catch and return full traceback
#                     traceback_output = traceback.format_exc()
#                     return JsonResponse({
#                         "status": "error",
#                         "message": traceback_output
#                     }, status=500)

#             return JsonResponse({"status": "saved", "message": "File saved successfully."})

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=400)

#     return render(request, 'webprojects/file_detail.html', {
#         'file': file,
#         'files': files,
#         'folders': folders,
#         'exts': exts,
#         'project': project,
#         'is_image': is_image,
#     })



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

# client = OpenAI(api_key="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")
 # Use your settings variable
#client = OpenAI(api_key=settings.OPENAI_API_KEY) 

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
            print("OpenAI error:", e)
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
            f"List 100 Python keywords, functions, or methods that typically start with '{prefix}'. "
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