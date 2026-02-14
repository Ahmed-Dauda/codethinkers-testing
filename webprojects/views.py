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


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json

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
from sms.models import Courses, Topics


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


import os
from openai import OpenAI

#Initialize OpenAI client
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# @login_required
# def create_project(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             name = data.get('name', '').strip()
#             if not name:
#                 return JsonResponse({'status': 'error', 'message': 'Project name is required'})

#             # Get or create default topic
#             default_topic, _ = Topics.objects.get_or_create(title="General")

#             # Check if project already exists for this user
#             existing_project = Project.objects.filter(user=request.user, name=name).first()
#             if existing_project:
#                 first_file = existing_project.files.first()
#                 return JsonResponse({
#                     'status': 'success',
#                     'project_id': existing_project.id,
#                     'file_id': first_file.id if first_file else None
#                 })

#             # Auto-detect file extension
#             lower_name = name.lower()
#             if "python" in lower_name:
#                 ext = ".py"
#                 default_content = "# Start your Python code here"
#             elif "html" in lower_name:
#                 ext = ".html"
#                 default_content = "<!-- Start writing HTML here -->"
#             elif "css" in lower_name:
#                 ext = ".css"
#                 default_content = "/* Write your CSS here */"
#             elif "js" in lower_name or "javascript" in lower_name:
#                 ext = ".js"
#                 default_content = "// JavaScript starts here"
#             else:
#                 ext = ".py"
#                 default_content = "# General notes"

#             # Create project with default topic
#             project = Project.objects.create(
#                 user=request.user,
#                 name=name,
#                 topic=default_topic  # ✅ assign topic here
#             )

#             # Optionally, create a default folder with topic
#             folder = Folder.objects.create(
#                 project=project,
#                 name="Main",
#                 topic=default_topic  # ✅ assign topic here
#             )

#             # Create the first file inside that folder with topic
#             file = File.objects.create(
#                 name='main' + ext,
#                 project=project,
#                 folder=folder,
#                 content=default_content,
#                 topic=default_topic  # ✅ assign topic here
#             )

#             return JsonResponse({
#                 'status': 'success',
#                 'project_id': project.id,
#                 'file_id': file.id
#             })

#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})

#     else:
#         user_projects = Project.objects.filter(user=request.user).order_by('-created')
#         return render(request, 'webprojects/create_project.html', {
#             'projects': user_projects
#         })

@login_required
def create_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            course_id = data.get('course_id')  # 👈 IMPORTANT

            if not name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Project name is required'
                })

            # ---------------- COURSE RESOLUTION ----------------
            course = None
            if course_id:
                course = Courses.objects.filter(id=course_id).first()

            print("CREATE PROJECT COURSE:", course)
            # ---------------------------------------------------

            # Get or create DEFAULT topic FOR THIS COURSE
            default_topic, _ = Topics.objects.get_or_create(
                title="General",
                courses=course
            )

            # Prevent duplicate projects per user
            existing_project = Project.objects.filter(
                user=request.user,
                name=name
            ).first()

            if existing_project:
                first_file = existing_project.files.first()
                return JsonResponse({
                    'status': 'success',
                    'project_id': existing_project.id,
                    'file_id': first_file.id if first_file else None
                })

            # ---------------- FILE TYPE AUTO-DETECT ----------------
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
                ext = ".py"
                default_content = "# General notes"
            # ------------------------------------------------------

            # ---------------- CREATE PROJECT ----------------
            project = Project.objects.create(
                user=request.user,
                name=name,
                course=course,          # ✅ FIXED
                topic=default_topic     # ✅ course-aware topic
            )

            folder = Folder.objects.create(
                project=project,
                name="Main",
                topic=default_topic
            )

            file = File.objects.create(
                name='main' + ext,
                project=project,
                folder=folder,
                content=default_content,
                topic=default_topic
            )
            # ------------------------------------------------

            return JsonResponse({
                'status': 'success',
                'project_id': project.id,
                'file_id': file.id
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    # ---------------- GET REQUEST ----------------
    user_projects = Project.objects.filter(
        user=request.user
    ).select_related('course', 'topic').order_by('-created')

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
   


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
import os, json, traceback, io, base64, contextlib
import pandas as pd
import matplotlib.pyplot as plt
from .models import Project, File, Folder
from django.conf import settings



from django.db import transaction
from django.views.decorators.http import require_http_methods


import re

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

@csrf_protect
@require_http_methods(["POST"])
def file_chat(request, project_id, file_id):
    """
    AI-powered file editor endpoint (ASK / APPLY)
    GUARANTEED JSON RESPONSES ONLY
    """

    # ================= SAFE JSON PARSING =================
    try:
        if request.content_type != "application/json":
            return JsonResponse({
                "status": "error",
                "message": "Content-Type must be application/json"
            }, status=400)

        data = json.loads(request.body.decode("utf-8"))
        prompt = data.get("prompt", "").strip()
        apply_changes = bool(data.get("apply", False))

    except json.JSONDecodeError:
        return JsonResponse({
            "status": "error",
            "message": "Invalid JSON payload"
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": "Failed to parse request",
            "detail": str(e)
        }, status=400)

    # ================= VALIDATION =================
    if not prompt:
        return JsonResponse({
            "status": "error",
            "message": "Prompt cannot be empty"
        }, status=400)

    if len(prompt) > 5000:
        return JsonResponse({
            "status": "error",
            "message": "Prompt too long (max 5000 chars)"
        }, status=400)

    # ================= LOAD FILE =================
    try:
        file = get_object_or_404(File, id=file_id, project_id=project_id)
        file_ext = file.extension()

    except Exception:
        return JsonResponse({
            "status": "error",
            "message": "File not found"
        }, status=404)

    LANGUAGE_MAP = {
        '.html': 'HTML',
        '.css': 'CSS',
        '.js': 'JavaScript',
        '.py': 'Python',
        '.json': 'JSON',
        '.md': 'Markdown',
        '.txt': 'Text',
    }

    language = LANGUAGE_MAP.get(
        file_ext.lower(),
        file_ext.upper().replace('.', '') + " file"
    )

    # ================= BUILD PROMPTS =================
    if apply_changes:
        system_prompt = f"""
You are an expert {language} code editor.

RULES:
- Return ONLY the complete updated file content
- NO markdown
- NO explanations
- NO code fences
- Output MUST start with code
"""

        user_prompt = f"""
CURRENT FILE:
{file.content or f"// Empty {language} file"}

USER REQUEST:
{prompt}
"""

    else:
        system_prompt = f"""
You are an expert {language} code reviewer.

Explain what would change.
Do NOT return code.
"""

        user_prompt = f"""
FILE:
{file.content or f"// Empty {language} file"}

REQUEST:
{prompt}
"""

    # ================= OPENAI CALL =================
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=4000,
        )

        ai_output = response.choices[0].message.content.strip()

        if not ai_output:
            raise ValueError("Empty AI response")

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": "AI service failed",
            "detail": str(e)
        }, status=500)

    # ================= APPLY MODE =================
    if apply_changes:
        try:
            cleaned = ai_output.strip()

            # Strip accidental markdown
            if cleaned.startswith("```"):
                cleaned = "\n".join(
                    line for line in cleaned.splitlines()
                    if not line.strip().startswith("```")
                ).strip()

            if not cleaned:
                return JsonResponse({
                    "status": "error",
                    "message": "AI returned empty code"
                }, status=500)

            file.content = cleaned
            file.save(update_fields=["content"])

            return JsonResponse({
                "status": "success",
                "saved": True,
                "code": cleaned,
                "file_id": file.id,
                "file_name": file.name,
                "language": language
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": "Failed to save file",
                "detail": str(e)
            }, status=500)

    # ================= ASK MODE =================
    return JsonResponse({
        "status": "success",
        "saved": False,
        "explanation": ai_output,
        "file_name": file.name,
        "language": language
    })

#worked
# @csrf_protect
# @require_http_methods(["POST"])
# def file_chat(request, project_id, file_id):
#     """
#     VS Code–style AI file chat
#     - Ask: explanation only (no save)
#     - Apply: updates ONLY the current file and saves to DB
#     """
    
#     # -----------------------------
#     # Parse request body
#     # -----------------------------
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         prompt = data.get("prompt", "").strip()
#         apply_changes = bool(data.get("apply", False))
#     except json.JSONDecodeError as e:
#         return JsonResponse({"status": "error", "message": f"Invalid JSON: {e}"}, status=400)

#     if not prompt:
#         return JsonResponse({"status": "error", "message": "Prompt is required"}, status=400)

#     # Limit prompt length to prevent abuse
#     if len(prompt) > 5000:
#         return JsonResponse({"status": "error", "message": "Prompt too long (max 5000 chars)"}, status=400)

#     # -----------------------------
#     # Load file (scoped to project)
#     # -----------------------------
#     file = get_object_or_404(File, id=file_id, project_id=project_id)
#     file_ext = file.extension()

#     # -----------------------------
#     # SYSTEM PROMPT
#     # -----------------------------
#     if apply_changes:
#         system_prompt = f"""You are an AI code editor like VS Code.

# RULES:
# - Edit ONLY this file: {file.name}
# - Return the FULL updated file content
# - Do NOT add explanations or comments about what you changed
# - Do NOT wrap in markdown code fences (no ```{file_ext})
# - Output MUST be valid {file_ext} code that can be directly saved
# - Start your response with the actual code immediately
# """
#     else:
#         system_prompt = """You are an AI assistant helping explain code changes.

# RULES:
# - DO NOT modify the file
# - DO NOT return code
# - ONLY explain what changes would be made and why
# - Be concise and specific
# """

#     user_prompt = f"""CURRENT FILE CONTENT:
# ```{file_ext}
# {file.content}
# ```

# USER REQUEST:
# {prompt}
# """

#     # -----------------------------
#     # Call OpenAI
#     # -----------------------------
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4-turbo-preview",  # Use correct model name
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt},
#             ],
#             temperature=0,
#             max_tokens=4000,
#         )

#         ai_output = response.choices[0].message.content.strip()
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": f"AI error: {str(e)}"}, status=500)

#     if not ai_output:
#         return JsonResponse({"status": "error", "message": "AI returned empty response"}, status=500)

#     # -----------------------------
#     # APPLY MODE → SAVE FILE
#     # -----------------------------
#     if apply_changes:
#         # Clean up any markdown code fences that might have slipped through
#         cleaned_code = ai_output
#         if cleaned_code.startswith("```"):
#             lines = cleaned_code.split("\n")
#             # Remove first line if it's a code fence
#             if lines[0].startswith("```"):
#                 lines = lines[1:]
#             # Remove last line if it's a closing fence
#             if lines and lines[-1].strip() == "```":
#                 lines = lines[:-1]
#             cleaned_code = "\n".join(lines)
        
#         print(f"[APPLY] Updating {file.name} (ID: {file.id})")
#         print(f"[APPLY] Preview: {cleaned_code[:200]}...")
        
#         file.content = cleaned_code
#         file.save(update_fields=["content"])
        
#         return JsonResponse({
#             "status": "success",
#             "message": "File updated successfully",
#             "code": cleaned_code
#         })

#     # -----------------------------
#     # ASK MODE → EXPLANATION ONLY
#     # -----------------------------
#     return JsonResponse({
#         "status": "success",
#         "explanation": ai_output
#     })

# At the very top of views.py, after all imports
from django.conf import settings
from openai import OpenAI
from .sandbox_runner import run_code

# ================= OPENAI CLIENT INITIALIZATION =================
# Initialize once when the module loads, not on every request


@login_required
@require_http_methods(["GET", "POST"])
def file_detail(request, project_id, file_id):
    # ================= PROJECT & FILE =================
    project = get_object_or_404(
        Project.objects.prefetch_related("files"),
        id=project_id,
        user=request.user
    )
    file = get_object_or_404(File, id=file_id, project=project)

    files = project.files.all()
    folders = Folder.objects.filter(project=project)

    # Fetch the course object by project name
    try:
        course = Courses.objects.get(title=file.project.name)
    except Courses.DoesNotExist:
        course = None

    # Fetch topics using the course object
    topics = Topics.objects.filter(courses=course).select_related("courses", "categories") if course else Topics.objects.none()

    print("PROJECT COURSE:", file.project.name)
    print("COURSE:", course)
    print("TOPICS COUNT:", topics.count())
    print("TOPICS RAW:", list(topics.values("id", "title", "courses_id")))

    # ================= SIDEBAR EXTENSIONS =================
    exts = sorted({
        os.path.splitext(f.name)[1].lstrip(".").lower()
        for f in files if "." in f.name
    })

    IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif")
    is_image = file.name.lower().endswith(IMAGE_EXTS)

    # ================= FILE TYPE =================
    ext = file.name.rsplit(".", 1)[-1].lower()
    is_python = ext == "py"

    # ================= POST =================
    if request.method == "POST":
        # ---------- Safe JSON parsing ----------
        try:
            data = json.loads(request.body.decode()) if request.body else {}
        except json.JSONDecodeError:
            data = {}

        new_content = data.get("content", "")
        run_plot = data.get("run_plot", False)
        run_table = data.get("run_table", False)
        prompt = data.get("prompt", "")

        # ================= AI PROMPT =================
        if prompt:
            # Check if OpenAI client is available
            if client is None:
                return JsonResponse({
                    "status": "error",
                    "message": "🔑 OpenAI API is not configured. Please set your API key.",
                    "error_detail": "OPENAI_API_KEY is missing or invalid."
                }, status=500)

            try:
                with transaction.atomic():
                    # Get or create the three core files
                    html_file, html_created = File.objects.get_or_create(
                        project=project, 
                        name="index.html",
                        defaults={"content": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Project</title>\n    <link rel='stylesheet' href='style.css'>\n</head>\n<body>\n    <script src='script.js'></script>\n</body>\n</html>"}
                    )
                    css_file, css_created = File.objects.get_or_create(
                        project=project, 
                        name="style.css",
                        defaults={"content": "/* Your styles here */\n"}
                    )
                    js_file, js_created = File.objects.get_or_create(
                        project=project, 
                        name="script.js",
                        defaults={"content": "// Your JavaScript here\n"}
                    )

                    # ================= ENHANCED AI SYSTEM PROMPT =================
                    system_message = """You are a senior full-stack web developer with expertise in modern web technologies.

**Your Role:**
- Generate clean, production-ready HTML, CSS, and JavaScript
- Follow modern best practices and web standards
- Create responsive, accessible, and performant code
- Write semantic HTML with proper structure
- Use modern CSS (Flexbox, Grid, custom properties)
- Write vanilla JavaScript with ES6+ features

**Code Quality Standards:**
- Use meaningful class names and IDs
- Include helpful comments for complex logic
- Ensure cross-browser compatibility
- Follow consistent indentation (2 spaces)
- Write DRY (Don't Repeat Yourself) code

**Response Format:**
Return ONLY valid JSON with these exact keys: "html", "css", "js"
Each value should be the complete file content as a string.
Do NOT include any markdown code fences, explanations, or extra text.

**Example Response Structure:**
{
  "html": "<!DOCTYPE html>...",
  "css": "body { ... }",
  "js": "document.addEventListener..."
}

**Important Rules:**
1. Preserve existing functionality unless explicitly asked to change it
2. Only modify what the user requests
3. Keep the code clean and maintainable
4. Ensure all three files work together cohesively
5. Always include proper DOCTYPE and meta tags in HTML
6. Link CSS and JS files correctly in HTML"""

                    # ================= ENHANCED USER PROMPT =================
                    user_message = f"""**Current Project State:**

**HTML File (index.html):**
```html
{html_file.content if html_file.content.strip() else "<!-- Empty file -->"}
```

**CSS File (style.css):**
```css
{css_file.content if css_file.content.strip() else "/* Empty file */"}
```

**JavaScript File (script.js):**
```javascript
{js_file.content if js_file.content.strip() else "// Empty file"}
```

---

**User Request:**
{prompt}

---

**Instructions:**
1. Analyze the current code state
2. Implement the requested changes
3. Ensure all files work together
4. Maintain consistency with existing code style
5. Return complete, updated files in JSON format

Remember: Return ONLY the JSON object with keys "html", "css", "js". No extra text or markdown."""

                    # ================= API CALL WITH BETTER ERROR HANDLING =================
                    print(f"🤖 AI Request: {prompt[:100]}...")
                    print(f"📊 Request size: System={len(system_message)} chars, User={len(user_message)} chars")
                    
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4-turbo-preview",
                            messages=[
                                {"role": "system", "content": system_message},
                                {"role": "user", "content": user_message},
                            ],
                            max_tokens=4000,
                            temperature=0.3,
                            response_format={"type": "json_object"}
                        )
                        
                        ai_text = response.choices[0].message.content.strip()
                        print(f"✅ AI Response received: {len(ai_text)} chars")
                        
                    except Exception as api_error:
                        error_msg = str(api_error)
                        print(f"❌ OpenAI API Error: {error_msg}")
                        print(f"❌ Full traceback: {traceback.format_exc()}")
                        
                        # Check for common API errors
                        if "rate_limit" in error_msg.lower():
                            return JsonResponse({
                                "status": "error",
                                "message": "⏳ Rate limit reached. Please wait a moment and try again.",
                                "error_detail": error_msg
                            }, status=429)
                        elif "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                            return JsonResponse({
                                "status": "error",
                                "message": "🔑 API authentication failed. Please check your API key configuration.",
                                "error_detail": error_msg
                            }, status=500)
                        elif "timeout" in error_msg.lower():
                            return JsonResponse({
                                "status": "error",
                                "message": "⏱️ Request timed out. Please try again.",
                                "error_detail": error_msg
                            }, status=504)
                        elif "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
                            return JsonResponse({
                                "status": "error",
                                "message": "💳 API quota exceeded. Please check your OpenAI account.",
                                "error_detail": error_msg
                            }, status=402)
                        else:
                            return JsonResponse({
                                "status": "error",
                                "message": f"🚫 AI service failed: {error_msg}",
                                "error_detail": error_msg
                            }, status=500)

                    # ================= PARSE AI RESPONSE =================
                    try:
                        ai_generated = json.loads(ai_text)
                    except json.JSONDecodeError as json_error:
                        print(f"⚠️ JSON Parse Error: {json_error}")
                        print(f"⚠️ Raw AI response: {ai_text[:500]}...")
                        
                        # Try to extract JSON from markdown code blocks
                        print("⚠️ Attempting to extract JSON from malformed response")
                        start = ai_text.find("{")
                        end = ai_text.rfind("}") + 1
                        if start != -1 and end > start:
                            ai_text_cleaned = ai_text[start:end]
                            try:
                                ai_generated = json.loads(ai_text_cleaned)
                                print("✅ Successfully extracted JSON from response")
                            except json.JSONDecodeError:
                                return JsonResponse({
                                    "status": "error",
                                    "message": "Failed to parse AI response as JSON. The AI may have returned an invalid format.",
                                    "error_detail": f"Could not parse: {ai_text[:200]}..."
                                }, status=500)
                        else:
                            return JsonResponse({
                                "status": "error",
                                "message": "AI response does not contain valid JSON.",
                                "error_detail": f"Response preview: {ai_text[:200]}..."
                            }, status=500)

                    # ================= VALIDATE RESPONSE =================
                    if not isinstance(ai_generated, dict):
                        return JsonResponse({
                            "status": "error",
                            "message": "AI response is not a valid JSON object.",
                            "error_detail": f"Type: {type(ai_generated)}"
                        }, status=500)
                    
                    # Check if at least one file key exists
                    if not any(key in ai_generated for key in ["html", "css", "js"]):
                        return JsonResponse({
                            "status": "error",
                            "message": "AI response missing required keys (html, css, or js).",
                            "error_detail": f"Keys found: {list(ai_generated.keys())}"
                        }, status=500)
                    
                    updates_made = []

                    # ================= UPDATE FILES =================
                    if "html" in ai_generated and ai_generated["html"].strip():
                        html_content = ai_generated["html"].strip()
                        if not html_content.startswith("<!DOCTYPE"):
                            html_content = f"<!DOCTYPE html>\n{html_content}"
                        html_file.content = html_content
                        html_file.save(update_fields=["content"])
                        updates_made.append("HTML")
                        print(f"✅ Updated index.html ({len(html_content)} chars)")

                    if "css" in ai_generated and ai_generated["css"].strip():
                        css_file.content = ai_generated["css"].strip()
                        css_file.save(update_fields=["content"])
                        updates_made.append("CSS")
                        print(f"✅ Updated style.css ({len(css_file.content)} chars)")

                    if "js" in ai_generated and ai_generated["js"].strip():
                        js_file.content = ai_generated["js"].strip()
                        js_file.save(update_fields=["content"])
                        updates_made.append("JavaScript")
                        print(f"✅ Updated script.js ({len(js_file.content)} chars)")

                    if not updates_made:
                        return JsonResponse({
                            "status": "warning",
                            "message": "No files were updated. AI may not have understood the request.",
                            "ai_response": ai_generated
                        }, status=200)

                    # ================= SUCCESS RESPONSE =================
                    return JsonResponse({
                        "status": "success",
                        "ai_content": ai_generated,
                        "message": f"✨ Successfully updated: {', '.join(updates_made)}",
                        "files_updated": updates_made,
                        "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt
                    })

            except Exception as e:
                print(f"❌ Unexpected Error in AI Processing: {traceback.format_exc()}")
                return JsonResponse({
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                    "error_detail": traceback.format_exc()
                }, status=500)

        # ================= FILE SAVE =================
        if new_content and new_content != file.content:
            file.content = new_content
            file.save(update_fields=["content"])
            print(f"💾 Saved {file.name} ({len(new_content)} chars)")

        response_table = ""

        # ================= CSV / EXCEL PREVIEW =================
        if ext in {"csv", "xls", "xlsx"} and file.file:
            try:
                if ext == "csv":
                    df = pd.read_csv(file.file.path)
                else:
                    df = pd.read_excel(file.file.path)

                if run_table:
                    response_table = df.head(20).to_html(
                        classes="table table-bordered table-sm",
                        index=False
                    )
            except Exception as e:
                return JsonResponse({
                    "status": "error",
                    "message": f"Failed to read file: {str(e)}"
                }, status=400)

        # ================= SAFE PYTHON RUNNER =================
        if is_python and (run_plot or new_content.strip()):
            result = run_code(new_content)
            
            # Add table data if available
            result["table"] = response_table
            
            # Return error response if execution failed
            if result["status"] == "error":
                return JsonResponse(result, status=500)
            
            return JsonResponse(result)

        return JsonResponse({
            "status": "saved",
            "message": "✓ File saved successfully"
        })

    # ================= GET =================
    return render(request, "webprojects/file_detail.html", {
        "file": file,
        "files": files,
        "folders": folders,
        "exts": exts,
        "project": project,
        "is_image": is_image,
        "topics": topics,
    })

#worked
# @login_required
# @require_http_methods(["GET", "POST"])
# def file_detail(request, project_id, file_id):
#     # ================= PROJECT & FILE =================
#     project = get_object_or_404(
#         Project.objects.prefetch_related("files"),
#         id=project_id,
#         user=request.user
#     )
#     file = get_object_or_404(File, id=file_id, project=project)

#     files = project.files.all()
#     folders = Folder.objects.filter(project=project)

#     # ================= SIDEBAR EXTENSIONS =================
#     exts = sorted({
#         os.path.splitext(f.name)[1].lstrip(".").lower()
#         for f in files if "." in f.name
#     })

#     IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif")
#     is_image = file.name.lower().endswith(IMAGE_EXTS)

#     # ================= FILE TYPE =================
#     ext = file.name.rsplit(".", 1)[-1].lower()
#     is_python = ext == "py"

#     # ================= POST =================
#     if request.method == "POST":

#         # ---------- Safe JSON parsing ----------
#         try:
#             data = json.loads(request.body.decode()) if request.body else {}
#         except json.JSONDecodeError:
#             data = {}

#         new_content = data.get("content", "")
#         run_plot = data.get("run_plot", False)
#         run_table = data.get("run_table", False)
#         prompt = data.get("prompt", "")

#         # ================= AI PROMPT =================
#         if prompt:
#             try:
#                 with transaction.atomic():
#                     html_file, _ = File.objects.get_or_create(
#                         project=project, name="index.html",
#                         defaults={"content": ""}
#                     )
#                     css_file, _ = File.objects.get_or_create(
#                         project=project, name="style.css",
#                         defaults={"content": ""}
#                     )
#                     js_file, _ = File.objects.get_or_create(
#                         project=project, name="script.js",
#                         defaults={"content": ""}
#                     )

#                     system_message = (
#                         "You are an expert web developer. "
#                         "Update the HTML, CSS, and JS based on the user's request. "
#                         "Only modify what is necessary. "
#                         "Return VALID JSON with keys: html, css, js."
#                     )

#                     user_message = f"""
# HTML:
# {html_file.content}

# CSS:
# {css_file.content}

# JS:
# {js_file.content}

# User request:
# {prompt}
# """

#                     response = client.chat.completions.create(
#                         model="gpt-4.1",
#                         messages=[
#                             {"role": "system", "content": system_message},
#                             {"role": "user", "content": user_message},
#                         ],
#                         max_completion_tokens=4000,
#                         temperature=0,
#                     )

#                     ai_text = response.choices[0].message.content.strip()
#                     start, end = ai_text.find("{"), ai_text.rfind("}")
#                     if start != -1 and end != -1:
#                         ai_text = ai_text[start:end + 1]

#                     ai_generated = json.loads(ai_text)

#                     if ai_generated.get("html"):
#                         html_file.content = ai_generated["html"]
#                         html_file.save(update_fields=["content"])

#                     if ai_generated.get("css"):
#                         css_file.content = ai_generated["css"]
#                         css_file.save(update_fields=["content"])

#                     if ai_generated.get("js"):
#                         js_file.content = ai_generated["js"]
#                         js_file.save(update_fields=["content"])

#                 return JsonResponse({
#                     "status": "success",
#                     "ai_content": ai_generated,
#                     "message": "AI project updated successfully"
#                 })

#             except Exception:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": traceback.format_exc()
#                 }, status=500)

#         # ================= FILE SAVE =================
#         if new_content and new_content != file.content:
#             file.content = new_content
#             file.save(update_fields=["content"])

#         response_table = ""
#         images = []

#         # ================= CSV / EXCEL PREVIEW =================
#         if ext in {"csv", "xls", "xlsx"} and file.file:
#             try:
#                 if ext == "csv":
#                     df = pd.read_csv(file.file.path)
#                 else:
#                     df = pd.read_excel(file.file.path)

#                 if run_table:
#                     response_table = df.head(20).to_html(
#                         classes="table table-bordered table-sm",
#                         index=False
#                     )
#             except Exception as e:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": str(e)
#                 }, status=400)

#         # ================= SAFE PYTHON RUNNER =================
#         if is_python and (run_plot or new_content.strip()):
#             buffer_out = io.StringIO()
#             buffer_err = io.StringIO()

#             plt.clf()
#             plt.close("all")

#             SAFE_BUILTINS = {
#                 "print": print,
#                 "len": len,
#                 "range": range,
#                 "min": min,
#                 "max": max,
#                 "sum": sum,
#                 "abs": abs,
#             }

#             safe_globals = {
#                 "__builtins__": SAFE_BUILTINS,
#                 "pd": pd,
#                 "plt": plt,
#             }

#             def fake_show(*args, **kwargs):
#                 buf = io.BytesIO()
#                 plt.savefig(buf, format="png", bbox_inches="tight")
#                 buf.seek(0)
#                 images.append(
#                     f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"
#                 )
#                 plt.close()

#             plt.show = fake_show

#             try:
#                 with contextlib.redirect_stdout(buffer_out), \
#                      contextlib.redirect_stderr(buffer_err):
#                     exec(new_content, safe_globals, {})

#                 if buffer_err.getvalue():
#                     return JsonResponse({
#                         "status": "error",
#                         "message": buffer_err.getvalue()
#                     }, status=500)

#                 return JsonResponse({
#                     "status": "success",
#                     "output": buffer_out.getvalue() or "[No output]",
#                     "table": response_table,
#                     "images": images,
#                 })

#             except Exception:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": traceback.format_exc()
#                 }, status=500)

#         return JsonResponse({
#             "status": "saved",
#             "message": "File saved successfully"
#         })

#     # ================= GET =================
#     return render(request, "webprojects/file_detail.html", {
#         "file": file,
#         "files": files,
#         "folders": folders,
#         "exts": exts,
#         "project": project,
#         "is_image": is_image,
#     })

#real view 2
# @login_required
# def file_detail(request, project_id, file_id):
#     # Ensure the project belongs to the logged-in user
#     project = get_object_or_404(Project, id=project_id, user=request.user)
#     file = get_object_or_404(File, id=file_id, project=project)
    
#     files = project.files.all()
#     folders = Folder.objects.filter(project=project)

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
#             prompt = data.get("prompt", "")

#             # ===== AI Prompt Handling =====
#             # ===== AI Prompt Handling =====
#             if prompt:
#                 try:
#                     # Only fetch or create files for this verified project
#                     html_file, _ = File.objects.get_or_create(project=project, name="index.html")
#                     css_file, _ = File.objects.get_or_create(project=project, name="style.css")
#                     js_file, _ = File.objects.get_or_create(project=project, name="script.js")

#                     system_message = (
#                         "You are an expert web developer. Update the given HTML, CSS, and JS project "
#                         "based on the user's request. Only modify what is necessary. "
#                         "Always return a VALID JSON object with keys: html, css, js. "
#                         "Do NOT include explanations, markdown, or extra text."
#                     )

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
#                         max_completion_tokens=4000,
#                         temperature=0
#                     )

#                     ai_text = response.choices[0].message.content.strip()

#                     # Extract only JSON portion
#                     start = ai_text.find("{")
#                     end = ai_text.rfind("}")
#                     if start != -1 and end != -1:
#                         ai_text = ai_text[start:end+1]

#                     try:
#                         ai_generated = json.loads(ai_text)
#                     except json.JSONDecodeError:
#                         cleaned = ai_text.replace("\n", " ").replace("\r", " ").strip()
#                         try:
#                             ai_generated = json.loads(cleaned)
#                         except Exception:
#                             ai_generated = {"html": ai_text, "css": "", "js": ""}

#                     # ✅ Save AI updates only for files belonging to this project
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
#                     df = pd.read_csv(file_path) if ext == "csv" else pd.read_excel(file_path)
#                     if run_table:
#                         response_table = df.head(20).to_html(classes="table table-bordered table-sm", index=False)
#                 except Exception as e:
#                     return JsonResponse({"status": "error", "message": str(e)}, status=500)

#             # Python execution (mini Jupyter)
#             if run_plot or new_content.strip():
#                 buffer_out = io.StringIO()
#                 buffer_err = io.StringIO()
#                 plt.clf()
#                 plt.close('all')

#                 # Patch pandas read methods to use MEDIA_ROOT/uploads
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

#                 # Capture plots as base64
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


#real
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
#                         max_completion_tokens=4000,
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
                max_tokens=2000,
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
                max_tokens=2000,
                temperature=0
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
            max_tokens=2000,
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