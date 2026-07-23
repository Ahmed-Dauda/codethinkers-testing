import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Project, File, StudentProgress, StudentXP
import json
import glob
import json
import sqlite3
import re
import secrets
import shutil
import socket
import subprocess
import sys
import time
import traceback as tb_module
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods



import time
import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction, OperationalError

from bs4 import BeautifulSoup
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
import os
import json
import traceback
import pandas as pd
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.conf import settings
from .models import Project, File, Folder, StudentProgress
from sms.models import Courses, Topics
from quiz.models import Course as ExamCourse
import hashlib
from django.core.cache import cache
from django.db.models import Count, Q
from django.db.models import Count
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
from sms.models import CompletedTopics, Courses, Topics


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
import secrets
#Initialize OpenAI client
from openai import OpenAI
import os

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt  
def voice_chat_tutor(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    
    try:
        data = json.loads(request.body)
        messages = data.get('messages', [])
        system_prompt = data.get('system_prompt', '')


        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'system', 'content': system_prompt}] + messages,
            max_tokens=300,
        )
        
        reply = response.choices[0].message.content
        return JsonResponse({'reply': reply})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@login_required
def create_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            course_id = data.get('course_id')

            if not name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Project name is required'
                })

            # ---------------- COURSE RESOLUTION ----------------
            course = None
            if course_id:
                course = Courses.objects.filter(pk=course_id).first()
            if not course:
                course = Courses.objects.filter(title=name).first()
            print("CREATE PROJECT COURSE:", course)
            # ---------------------------------------------------

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
                course=course,
                topic=None
            )

            folder = Folder.objects.create(
                project=project,
                name="Main",
                topic=None
            )

            file = File.objects.create(
                name='main' + ext,
                project=project,
                folder=folder,
                created_by=request.user,
                content=default_content,
                topic=None
            )

            print("Created project:", project.name, "| file:", file.name)
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
@require_http_methods(["POST"])
def file_autosave(request):
    # ── Parse JSON body ──────────────────────────────────────────────────
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({
            "status": "error",
            "message": "Invalid JSON data",
            "detail": str(e)
        }, status=400)

    file_id = data.get("file_id")

    if not file_id:
        return JsonResponse({
            "status": "error",
            "message": "file_id is required"
        }, status=400)

    if "content" not in data:
        return JsonResponse({
            "status": "error",
            "message": "content is required"
        }, status=400)

    content = data["content"]

    # ── Save with retry (handles SQLite "database is locked") ────────────
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            with transaction.atomic():
                file_obj = (
                    File.objects
                    .select_for_update(nowait=False)
                    .get(id=file_id)
                )
                file_obj.content = content
                file_obj.save(update_fields=["content"])

                # ── Sync straight to disk if a server is live, instead of
                # ── triggering a full rebuild. Django's own autoreloader
                # ── (now enabled in start_dev_server) picks up .py changes
                # ── on its own — cheaply, without us killing/respawning
                # ── anything. Templates/static are read fresh per-request
                # ── anyway, so a plain write is enough for those too.
                export_dir = (
                    Path(settings.BASE_DIR)
                    / "generated_projects"
                    / str(file_obj.project.id)
                )
                sync_note = None

                if get_live_server_info(export_dir):
                    target_path = export_dir / file_obj.name
                    if target_path.exists():
                        # Only sync files that already exist on disk from a
                        # previous full export — a brand new file needs a
                        # real rebuild (new INSTALLED_APPS entries, etc.)
                        # and isn't something autosave should handle.
                        target_path.write_text(content, encoding="utf-8")

                        if file_obj.name.endswith("models.py"):
                            sync_note = _run_migrations_for_live_project(
                                export_dir, file_obj.project
                            )
                        else:
                            sync_note = "synced to disk; autoreload will pick it up"
                    else:
                        sync_note = "new file — not synced; use Run/rebuild to include it"

            response = {
                "status": "success",
                "message": "File saved",
                "file_id": file_id,
                "content_length": len(content),
            }
            if sync_note:
                response["sync"] = sync_note
            return JsonResponse(response)

        except OperationalError as e:
            if "locked" in str(e).lower() and attempt < max_attempts - 1:
                wait = 0.3 * (attempt + 1)
                print(f"⚠️ DB locked (attempt {attempt + 1}), retrying in {wait}s...")
                time.sleep(wait)
                continue
            print(f"❌ DB OperationalError after {attempt + 1} attempts: {e}")
            return JsonResponse({
                "status": "error",
                "message": "Database is busy. Please try again in a moment.",
                "detail": str(e)
            }, status=503)

        except File.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": f"File with ID {file_id} not found"
            }, status=404)

        except Exception as e:
            print(f"❌ Autosave error: {e}")
            print(traceback.format_exc())
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)



def _run_migrations_for_live_project(export_dir, project):
    """
    Only called when models.py was edited. Runs makemigrations + migrate
    against the live project's export dir. Clears old migration records
    so new models are always detected, even on existing databases.
    """
    settings_file = next(
        (f.name for f in File.objects.filter(project=project) if f.name.endswith("/settings.py")),
        None
    )
    if not settings_file:
        return "models.py changed but no settings.py found — skipped migrate"

    project_name = settings_file.split("/")[0]
    env = build_subprocess_env(export_dir, project_name)

    # Clear old migration files and records so new models are detected
    for app_name in _get_app_names_from_project(export_dir, project):
        migrations_dir = Path(export_dir) / app_name / "migrations"
        if migrations_dir.exists():
            for f in migrations_dir.glob("*.py"):
                if f.name != "__init__.py":
                    f.unlink()
                    print(f"🗑️ Deleted old migration: {f.name}")
        
        # Clear django_migrations table record
        subprocess.run(
            [sys.executable, "manage.py", "shell", "-c",
             f"from django.db import connection; cursor = connection.cursor(); "
             f"cursor.execute(\"DELETE FROM django_migrations WHERE app='{app_name}'\"); "
             f"print(f'Cleared {{cursor.rowcount}} records for {app_name}')"],
            cwd=export_dir, capture_output=True, text=True, env=env,
        )

    makemigrations = subprocess.run(
        [sys.executable, "manage.py", "makemigrations"],
        cwd=export_dir, capture_output=True, text=True, env=env,
    )
    if makemigrations.returncode != 0:
        return f"models.py changed but makemigrations failed: {makemigrations.stderr[:300]}"

   
    # First migrate all apps (system tables)
    migrate = subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        cwd=export_dir, capture_output=True, text=True, env=env,
    )
    # Then fake-initial for apps with cleared records (tables already exist)
    for app_name in _get_app_names_from_project(export_dir, project):
        subprocess.run(
            [sys.executable, "manage.py", "migrate", app_name, "--fake-initial"],
            cwd=export_dir, capture_output=True, text=True, env=env,
        )

    if migrate.returncode != 0:
        return f"models.py changed but migrate failed: {migrate.stderr[:300]}"

    return "models.py changed — migrations applied"


def _get_app_names_from_project(export_dir, project):
    """Get list of app names from the project's settings INSTALLED_APPS or models.py files."""
    app_names = set()
    for f in File.objects.filter(project=project):
        if f.name.endswith("models.py") and f.content:
            parts = f.name.split("/")
            if len(parts) >= 1:
                app_names.add(parts[0])
    return app_names



@require_http_methods(["GET"])
def get_file_content(request, project_id, file_id):
    """Fetch file content without full page load"""
    try:
        file = File.objects.get(id=file_id, project_id=project_id)
        
        return JsonResponse({
            "status": "success",
            "file": {
                "id": file.id,
                "name": file.name,
                "content": file.content,
                "language": get_language_from_extension(file.name)
            }
        })
    except File.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "File not found"
        }, status=404)

def get_language_from_extension(filename):
    """Helper to determine language"""
    ext = filename.split('.')[-1].lower()
    lang_map = {
        'py': 'python',
        'js': 'javascript',
        'html': 'html',
        'css': 'css',
        'json': 'json',
        'md': 'markdown',
        'txt': 'plaintext'
    }
    return lang_map.get(ext, 'plaintext')



# @csrf_exempt
# def auto_save_view(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             file_id = data.get("file_id")
#             content = data.get("content")
#             file = File.objects.get(id=file_id)
#             file.content = content
#             file.save()
#             return JsonResponse({"status": "success"})
#         except File.DoesNotExist:
#             return JsonResponse({"status": "error", "message": "File not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=500)
#     return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)




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
   


def restart_server_only(project):
    """Restart the dev server process using files already on disk —
    no rmtree, no re-export from DB. Use this after a direct disk edit
    (like the AI file editor) that's already in sync with the DB, so
    .py changes actually take effect without risking a full-rebuild
    override of anything else."""
    export_dir = Path(settings.BASE_DIR) / "generated_projects" / str(project.id)

    if not export_dir.exists():
        return {"status": "error", "message": "Project not yet built — run it first."}

        kill_previous_server(export_dir, project.id)
    time.sleep(1)  # Wait for OS to release the port

    settings_file = next(export_dir.glob("*/settings.py"), None)
    
    if not settings_file:
        return {"status": "error", "message": "No settings.py found on disk."}
    project_name = settings_file.parent.name

    env = build_subprocess_env(export_dir, project_name, project.id)

    try:
        proc, PORT = start_dev_server(export_dir, env, project)
    except RuntimeError as e:
        return {"status": "error", "step": "runserver", "message": str(e)}

    _running_servers[project.id] = proc
    get_pidfile_path(export_dir).write_text(str(proc.pid))

    # Preserve the existing admin password rather than generating a new one
    admin_password = None
    info_path = get_info_path(export_dir)
    if info_path.exists():
        try:
            admin_password = json.loads(info_path.read_text()).get("admin_password")
        except (json.JSONDecodeError, KeyError):
            pass

    info_path.write_text(json.dumps({
        "pid": proc.pid,
        "port": PORT,
        "admin_password": admin_password,
    }))

    return {
        "status": "success",

      "preview_url": f"https://{getattr(project, 'subdomain', None) or f'project-{project.id}'}.codethinkers.org/" if os.environ.get('PRODUCTION') else f"http://127.0.0.1:{port}/",
        "admin_url": f"http://127.0.0.1:{PORT}/admin/",
        "port": PORT,
    }


@csrf_protect
@require_http_methods(["POST"])
def file_chat(request, project_id, file_id):
    """
    AI-powered file editor endpoint (ASK / APPLY)
    """
    print(f"🔵 file_chat called: project_id={project_id}, file_id={file_id}")

    # Parse JSON
    try:
        if request.content_type != "application/json":
            return JsonResponse({
                "status": "error",
                "message": "Content-Type must be application/json"
            }, status=400)

        data = json.loads(request.body.decode("utf-8"))
        prompt = data.get("prompt", "").strip()
        apply_changes = bool(data.get("apply", False))

    except json.JSONDecodeError as e:
        return JsonResponse({
            "status": "error",
            "message": "Invalid JSON payload",
            "detail": str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": "Failed to parse request",
            "detail": str(e)
        }, status=400)

    print(f"📝 Prompt: {prompt[:100]}... (apply={apply_changes})")

    # Validate
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

    # Load file
    try:
        file = get_object_or_404(File, id=file_id, project_id=project_id)
        file_ext = file.extension()
        print(f"📄 File: {file.name}, current content length: {len(file.content)}")
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": "File not found",
            "detail": str(e)
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

    # Give the AI awareness of what else exists in this project, so an
    # edit to one file (e.g. adding a model) doesn't collide with names
    # already used elsewhere in the project.
    project_context = get_existing_project_context(file.project)
    context_note = f"""
OTHER THINGS ALREADY IN THIS PROJECT (avoid collisions with these):
- Existing app names: {project_context["existing_apps"] or "none"}
- Existing model names: {project_context["existing_models"] or "none"}
- Existing URL namespaces: {project_context["existing_url_namespaces"] or "none"}
- Existing template filenames: {project_context["existing_templates"] or "none"}
If your change introduces a new name (model, URL name, template file),
make sure it doesn't collide with any of the above."""

    # Build prompts
    if apply_changes:
        system_prompt = f"""
You are an expert {language} code editor.
{context_note}

RULES:
- Return ONLY the complete updated file content
- NO markdown
- NO explanations
- NO code fences
- Output MUST start with code
- CRITICAL: Preserve ALL existing code that is not directly related to the user's request
- Only modify what the user explicitly asked for
- Keep the same indentation and formatting style
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
{context_note}

Explain what would change.
Do NOT return code.
"""

        user_prompt = f"""
FILE:
{file.content or f"// Empty {language} file"}

REQUEST:
{prompt}
"""

    # OpenAI call
    try:
        print("🤖 Calling OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
        
        print(f"✅ AI response received: {len(ai_output)} chars")

    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return JsonResponse({
            "status": "error",
            "message": "AI service failed",
            "detail": str(e)
        }, status=500)

    # ===== APPLY MODE - SAVE TO DATABASE =====
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

            # ===== CRITICAL: Save to database =====
            file.content = cleaned
            file.save(update_fields=["content"])
            
            # Verify the save worked
            file.refresh_from_db()
            print(f"✅ File {file.id} saved successfully. New content length: {len(file.content)}")
            
            # ===== Export to disk for the running server =====
            export_dir = Path(settings.BASE_DIR) / "generated_projects" / str(file.project.id)
            disk_path = export_dir / file.name
            disk_path.parent.mkdir(parents=True, exist_ok=True)
            disk_path.write_text(cleaned, encoding="utf-8")
            print(f"✅ Exported to disk: {disk_path}")

            # Restart the process (not a full rebuild) so .py changes
            # actually take effect — templates update live, but code
            # changes need the process reloaded since it's --noreload.
            if get_live_server_info(export_dir):
                print("🔄 Restarting server process to pick up the change...")
                restart_result = restart_server_only(file.project)
                if restart_result.get("status") != "success":
                    print(f"⚠️ Restart failed: {restart_result}")
                touch_project(file.project_id)

            return JsonResponse({
                "status": "success",
                "saved": True,
                "code": cleaned,
                "file_id": file.id,
                "file_name": file.name,
                "language": language,
                "content_length": len(cleaned),
                "message": "✅ Changes applied and saved to database!"
            })

        except Exception as e:
            print(f"❌ Failed to save file: {e}")
            print(traceback.format_exc())
            return JsonResponse({
                "status": "error",
                "message": "Failed to save file",
                "detail": str(e)
            }, status=500)

    # ===== ASK MODE - return explanation only =====
    return JsonResponse({
        "status": "success",
        "saved": False,
        "explanation": ai_output,
        "file_name": file.name,
        "language": language
    })



# views.py

import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# ─────────────────────────────────────────────────────────────────
# NEW: Progress API endpoint — called by the editor on load + after
#      each topic completion to refresh the sidebar progress bar.
# ─────────────────────────────────────────────────────────────────


@login_required
def get_student_progress(request):
    try:
        from sms.models import Topics

        course_id = request.GET.get('course_id')

        if course_id:
            all_topics = list(Topics.objects.filter(courses_id=course_id).order_by('id'))
        else:
            all_topics = list(Topics.objects.all().order_by('id'))

        progress = StudentProgress.objects.filter(
            student=request.user,
            course_id=course_id if course_id else None
        ).prefetch_related('completed_topics').order_by('-last_updated').first()

        current_topic = progress.current_topic if progress else None
        completed_ids = set(
            progress.completed_topics.values_list('id', flat=True)
        ) if progress else set()

        sidebar_ids        = {t.id for t in all_topics}
        relevant_completed = completed_ids & sidebar_ids  # ← course-scoped

        total = len(all_topics)
        done  = len(relevant_completed)
        pct   = round((done / total) * 100) if total else 0

        topics_data = [
            {
                'id':         t.id,
                'title':      t.title,
                'completed':  t.id in relevant_completed,  # ← was completed_ids
                'is_current': bool(current_topic and t.id == current_topic.id),
            }
            for t in all_topics
        ]

        return JsonResponse({
            'status':               'success',
            'current_topic_id':     current_topic.id    if current_topic else None,
            'current_topic_title':  current_topic.title if current_topic else 'None selected',
            'completed_topic_ids':  list(relevant_completed),  # ← was completed_ids
            'completed_count':      done,
            'total_count':          total,
            'overall_pct':          pct,
            'topics':               topics_data,
        })

    except Exception as e:
        import traceback; traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        


@login_required
@require_http_methods(["POST"])
def mark_topic_complete(request):
    xp_data = award_xp(request.user, 100) if request.user.is_authenticated else {}
    try:
        data      = json.loads(request.body)
        topic_id  = data.get('topic_id')
        course_id = data.get('course_id')

        from sms.models import Topics, Courses
        topic = Topics.objects.get(id=topic_id)

        # ✅ Get the course object
        topic = get_object_or_404(Topics.objects.select_related('courses'), id=topic_id)
        course = topic.courses  # ✅ derived from the topic itself, not the client

        # ✅ Get or create progress PER USER PER COURSE
        progress, _ = StudentProgress.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'current_topic': topic}
        )

        # Mark topic as complete
        progress.completed_topics.add(topic)

        # Advance to next topic within same course
        course_topics = list(
            Topics.objects.filter(courses_id=course_id).order_by('id')
        ) if course_id else []

        next_topic = None
        ids = [t.id for t in course_topics]
        try:
            pos = ids.index(topic.id)
            if pos + 1 < len(course_topics):
                next_topic = course_topics[pos + 1]
                progress.current_topic = next_topic
        except ValueError:
            pass

        progress.save()

        # ✅ Counts scoped strictly to THIS course's topics
        completed_ids      = set(progress.completed_topics.values_list('id', flat=True))
        sidebar_ids        = set(ids)
        relevant_completed = completed_ids & sidebar_ids
        total              = len(course_topics)
        done               = len(relevant_completed)
        pct                = round((done / total) * 100) if total else 0

        return JsonResponse({
            'status':              'success',
            'topic_title':         topic.title,
            'next_topic_id':       next_topic.id    if next_topic else None,
            'next_topic_title':    next_topic.title if next_topic else None,
            'completed_topic_ids': list(completed_ids),
            'completed_count':     done,
            'total_count':         total,
            'xp':                  xp_data,
            'overall_pct':         pct,
        })

    except Topics.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Topic not found'}, status=404)
    except Exception as e:
        import traceback; traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

# views.py - Add this temporary debug view

@csrf_exempt
def debug_current_topic(request):
    """Debug endpoint to check what topic is stored"""
    from .models import StudentProgress
    
    if request.user.is_authenticated:
        progress = StudentProgress.objects.filter(student=request.user).first()
        
        return JsonResponse({
            "user": request.user.username,
            "progress_exists": bool(progress),
            "current_topic_id": progress.current_topic.id if progress and progress.current_topic else None,
            "current_topic_title": progress.current_topic.title if progress and progress.current_topic else None,
            "localStorage_should_have": "Check frontend console"
        })
    
    return JsonResponse({"error": "Not authenticated"})



@login_required
def debug_progress(request):
    from .models import StudentProgress
    from sms.models import Topics
    
    all_progress = StudentProgress.objects.filter(student=request.user)
    all_topics   = Topics.objects.all().order_by('id')
    
    data = []
    for p in all_progress:
        data.append({
            'id':              p.id,
            'course':          str(p.course),
            'current_topic':   str(p.current_topic),
            'completed_topics': list(p.completed_topics.values_list('id', 'title')),
        })
    
    return JsonResponse({
        'progress_records': data,
        'total_topics':     all_topics.count(),
        'topic_ids':        list(all_topics.values_list('id', 'title')),
    }, json_dumps_params={'indent': 2})    

# ─────────────────────────────────────────────────────────────────
# HELPER: Extract ordered code examples from topic description
# ─────────────────────────────────────────────────────────────────
import re
def extract_code_examples(topic_desc):
    """Return list of code strings from fenced python blocks in topic.desc."""
    if not topic_desc:
        return []
    matches = re.findall(r'```python\s*\n?(.*?)```', topic_desc, re.DOTALL)
    examples = [m.strip() for m in matches if m.strip()]

    # Fallback: plain indented / keyword lines if no fenced blocks
    if not examples:
        lines = []
        for line in topic_desc.split('\n'):
            s = line.strip()
            if s and (line.startswith('    ') or line.startswith('\t') or
                      re.match(r'^(print|input|def |class |if |for |while |import |\w+ ?=)', s)):
                lines.append(s)
        if lines:
            examples = ['\n'.join(lines)]

    return examples
# ─────────────────────────────────────────────────────────────────
# HELPER: Detect which example the student has completed
# ─────────────────────────────────────────────────────────────────
def detect_completed_example_index(student_code, examples):
    if not examples or not student_code.strip():
        return -1
    student_lower = student_code.lower()
    last_completed = -1
    for i, ex in enumerate(examples):
        if _example_present_in_code(ex, student_lower):
            last_completed = i
        else:
            break
    return last_completed

def _example_present_in_code(example, student_lower):
    tokens = re.findall(
        r'[a-zA-Z_]\w*|[+\-*/=<>!]+|"[^"]*"|\'[^\']*\'|\d+',
        example.lower()
    )
    meaningful = [t for t in tokens if len(t) > 1 and
                  t not in ('in', 'is', 'or', 'and', 'not', 'the', 'to')]
    return bool(meaningful) and all(t in student_lower for t in meaningful)

# ─────────────────────────────────────────────────────────────────
# HELPER: Keyword mastery fallback (when topic has no code blocks)
# ─────────────────────────────────────────────────────────────────

def detect_topic_mastery_keywords(code, topic):
    if not code.strip() or len(code.strip().split('\n')) < 3:
        return False

    title_lower = topic.title.lower()
    code_lower  = code.lower()

    checks_map = {
        ('variable', 'print', 'input', 'basic', 'introduction'):
            [code_lower.count('=') >= 1, 'print(' in code_lower],
        ('if', 'condition', 'else', 'elif', 'boolean'):
            ['if ' in code_lower, any(k in code_lower for k in ['else', 'elif'])],
        ('loop', 'for', 'while', 'iteration', 'repeat'):
            [any(k in code_lower for k in ['for ', 'while ']),
             any(k in code_lower for k in ['range(', 'in '])],
        ('function', 'def', 'return', 'parameter'):
            ['def ' in code_lower, 'return' in code_lower],
        ('list', 'array', 'append', 'collection'):
            ['[' in code and ']' in code,
             any(k in code_lower for k in ['append(', 'len('])],
        ('string', 'str', 'text', 'format'):
            [('"' in code or "'" in code),
             any(k in code_lower for k in ['.upper()', '.lower()', 'f"', "f'", '.format('])],
        ('dict', 'dictionary', 'key', 'value'):
            ['{' in code and '}' in code,
             any(k in code_lower for k in ['.keys()', '.values()', '.get('])],
        ('file', 'open', 'read', 'write'):
            ['open(' in code_lower,
             any(k in code_lower for k in ['.read()', '.write(', 'with open'])],
        ('class', 'object', 'oop', '__init__'):
            ['class ' in code_lower, '__init__' in code_lower],
    }

    for keywords, checks in checks_map.items():
        if any(w in title_lower for w in keywords):
            return all(checks)

    return len(code.strip().split('\n')) >= 5


# ─────────────────────────────────────────────────────────────────
# HELPER: Extract key hints/tips from topic description (non-code)
# ─────────────────────────────────────────────────────────────────
def extract_topic_hints(topic_desc, max_hints=8):
    """
    Pull bullet points, numbered items, and key sentences from topic.desc.
    These feed the AI as its ONLY permitted knowledge.
    """
    if not topic_desc:
        return []

    # Strip code blocks first
    clean = re.sub(r'```.*?```', '', topic_desc, flags=re.DOTALL)

    hints = []
    bullets  = re.findall(r'(?:^|\n)\s*[-*•]\s+(.+)', clean)
    numbered = re.findall(r'(?:^|\n)\s*\d+\.\s+(.+)', clean)
    hints.extend([b.strip() for b in bullets  if len(b.strip()) > 10])
    hints.extend([n.strip() for n in numbered if len(n.strip()) > 10])

    for sentence in re.split(r'(?<=[.!?])\s+', clean):
        s = sentence.strip()
        if len(s) > 20 and any(w in s.lower() for w in [
            'use', 'remember', 'note', 'important', 'means', 'allows',
            'creates', 'defines', 'returns', 'stores', 'prints', 'variable',
            'value', 'assign', 'syntax', 'keyword', 'statement', 'expression'
        ]):
            hints.append(s)

    seen, unique = set(), []
    for h in hints:
        if h not in seen:
            seen.add(h); unique.append(h)
    return unique[:max_hints]


# ─────────────────────────────────────────────────────────────────
# HELPER: Prompts
# ─────────────────────────────────────────────────────────────────

def build_system_message(current_topic, next_topic, mode):
    topic_name = current_topic.title if current_topic else 'Python basics'

    if mode == 'complete':
        next_line = f'Their next lesson is: "{next_topic.title}".' if next_topic else \
                    'They have completed all lessons.'
        return (
            f'You are an encouraging Python tutor. '
            f'The student just finished "{topic_name}". {next_line} '
            f'Write 1–2 sentences congratulating them on {topic_name}. '
            f'Do NOT explain the next topic.'
        )

    return (
        f'You are a patient Python tutor. '
        f'The student is ONLY studying: "{topic_name}". '
        f'STRICT RULES: '
        f'(1) Every hint MUST come directly from the lesson material provided. '
        f'(2) Do NOT mention concepts outside {topic_name}. '
        f'(3) Maximum 2 sentences. Be encouraging. Never give the full answer.'
    )


def build_step_prompt(code, current_example, example_index, total_examples,
                      next_example, topic, topic_hints, error):
    """
    Prompt that forces the AI to use only the topic's own content
    as the source of its hint.
    """
    parts = [f'📚 Lesson: {topic.title}\n']

    # Inject the topic's own explanatory hints as source material
    if topic_hints:
        parts.append('LESSON KEY POINTS (use ONLY these to form your hint):')
        for h in topic_hints:
            parts.append(f'  • {h}')
        parts.append('')

    parts.append(f'Step {example_index + 1} of {total_examples}.')
    parts.append(f'Target code for this step:\n```python\n{current_example}\n```\n')

    if code.strip():
        parts.append(f"Student's code:\n```python\n{code}\n```\n")
    else:
        parts.append("Student hasn't written anything yet.\n")

    if error:
        parts.append(
            f'⚠️ Error: {error}\n'
            f'Using only the lesson key points above, help fix this in 1 sentence.'
        )
    elif not code.strip():
        parts.append(
            f'Using only the lesson key points above, give a 1-sentence hint '
            f'to start step {example_index + 1}: `{current_example}`.'
        )
    else:
        parts.append(
            f'Using only the lesson key points above, guide the student in 1 sentence '
            f'to complete or correct step {example_index + 1}. Do not reveal the full answer.'
        )

    if next_example:
        parts.append(f'\n(Next step after this: `{next_example}`. Do NOT mention it yet.)')

    return '\n'.join(parts)


def build_completion_prompt(code, current_topic, next_topic):
    next_line = (f'Their next lesson: "{next_topic.title}".'
                 if next_topic else 'They finished all lessons.')
    return (
        f'Student completed all exercises for "{current_topic.title}".\n'
        f'Code:\n```python\n{code}\n```\n{next_line}\n'
        f'Write 1–2 sentences of congratulations. Do NOT explain the next topic.'
    )


def build_free_hint_prompt(code, topic_context, topic_hints, cursor_line, error, topic):
    parts = []
    if topic_hints:
        parts.append('LESSON KEY POINTS (use ONLY these):')
        for h in topic_hints:
            parts.append(f'  • {h}')
        parts.append('')
    elif topic_context:
        parts.append(f'📚 LESSON:\n{topic_context}\n')

    topic_name = topic.title if topic else 'this topic'
    parts.append(f"Student's code (cursor line {cursor_line}):\n```python\n{code}\n```\n")

    if error:
        parts.append(f'⚠️ Error: {error}\nFix in 1 sentence using lesson points above.')
    elif not code.strip():
        parts.append(f'Give the first step for {topic_name} in 1 sentence.')
    else:
        parts.append(f'Suggest the next step based ONLY on lesson points above, 1 sentence.')
    return '\n'.join(parts)

def determine_hint_type(code, error):
    if error:                         return 'error'
    if not code.strip():              return 'start'
    if len(code.split('\n')) < 10:    return 'next_step'
    return 'improvement'

# ─────────────────────────────────────────────────────────────────
# MAIN VIEW
# ─────────────────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def get_contextual_hint(request):
    """
    AI hints are 100% grounded in the selected topic's own text.

    Pipeline:
      1. Load topic from DB using current_topic_id
      2. Extract examples + tips from topic.desc
      3. Detect which example the student is on
      4. Build a prompt that quotes the topic text verbatim as the
         ONLY allowed knowledge source
      5. System prompt explicitly forbids AI from going outside it
    """
    try:
        print("=" * 60)
        print("🔍 get_contextual_hint (strict topic mode)")

        data             = json.loads(request.body)
        code             = data.get('code', '')
        file_id          = data.get('file_id')
        cursor_line      = data.get('cursor_line', 1)
        error            = data.get('error')
        current_topic_id = data.get('current_topic_id')
        course_id        = data.get('course_id')

        # ── Guard: must have a selected topic ──────────────────────
        if not current_topic_id:
            return JsonResponse({
                "status": "success",
                "hint":  "Please select a topic from the sidebar before asking for hints.",
                "type":  "start",
                "topic": None
            })

        from .models import File
        from sms.models import Topics

        File.objects.get(id=file_id)   # validate file exists
        current_topic = Topics.objects.get(id=current_topic_id)
        print(f"✅ Topic: {current_topic.title}")

        # ── Resolve next topic in course order ─────────────────────
        next_topic = None
        try:
            if course_id:
                all_topics = list(Topics.objects.filter(courses_id=course_id).order_by('id'))
            else:
                all_topics = list(Topics.objects.all().order_by('id'))

            ids = [t.id for t in all_topics]
            pos = ids.index(current_topic.id)
            if pos + 1 < len(all_topics):
                next_topic = all_topics[pos + 1]
        except (ValueError, Exception):
            pass

        # ── Extract lesson material from DB ────────────────────────
        topic_desc = current_topic.desc or ''
        examples   = extract_code_examples(topic_desc)
        tips       = extract_topic_hints(topic_desc)

        print(f"  Examples: {len(examples)}  Tips: {len(tips)}")

        # ── Detect which step the student is on ────────────────────
        topic_mastered  = False
        current_example = None
        next_example    = None
        example_index   = 0
        total_examples  = len(examples)

        if examples:
            completed = detect_completed_example_index(code, examples)
            if completed >= total_examples - 1 and code.strip():
                topic_mastered = True
            else:
                example_index   = max(completed + 1, 0)
                current_example = examples[example_index]
                next_example    = (examples[example_index + 1]
                                   if example_index + 1 < total_examples else None)

        # ── Build AI system prompt ─────────────────────────────────
        # The system prompt carries the FULL lesson text so the AI
        # has zero excuse to go outside it.

        system_prompt = f"""You are a Python tutor helping a student learn ONLY this lesson:

════════════════════════════════════════
LESSON: {current_topic.title}
════════════════════════════════════════
{topic_desc}
════════════════════════════════════════

ABSOLUTE RULES — violations are not allowed:
1. You may ONLY use concepts, syntax, and examples that appear in the lesson text above.
2. NEVER mention loops, functions, classes, lists, dictionaries, decorators, or ANY concept
   that is NOT explicitly written in the lesson text above.
3. NEVER invent new examples. If you show code, it MUST be copied verbatim from the
   lesson examples above — do not change variable names, numbers, or structure.
4. Keep your reply to 1–2 sentences maximum.
5. Be encouraging but never give away the full answer.
6. If the student's code uses a concept not in this lesson, gently redirect them
   back to the lesson topic without explaining the outside concept.
"""

        # ── Build user prompt ──────────────────────────────────────
        if topic_mastered:
            next_line = (f'Their next lesson will be "{next_topic.title}".'
                         if next_topic else 'They have completed all available lessons.')
            user_prompt = (
                f'The student has completed all exercises for "{current_topic.title}".\n'
                f'Student code:\n```python\n{code}\n```\n'
                f'{next_line}\n'
                f'Write 1–2 encouraging sentences about what they achieved in '
                f'"{current_topic.title}". Do NOT mention or explain the next topic.'
            )
            hint_type = 'topic_complete'

        elif current_example:
            # Guided step-by-step mode
            parts = [
                f'The student is on Step {example_index + 1} of {total_examples} '
                f'for the lesson "{current_topic.title}".\n',
                f'The target code for this step (from the lesson):\n'
                f'```python\n{current_example}\n```\n',
            ]

            if tips:
                parts.append('Key points from the lesson the student should know:')
                for tip in tips:
                    parts.append(f'  • {tip}')
                parts.append('')

            if code.strip():
                parts.append(f"Student's current code:\n```python\n{code}\n```\n")
            else:
                parts.append("The student hasn't written anything yet.\n")

            if error:
                parts.append(
                    f'There is an error: {error}\n'
                    f'Using ONLY the lesson text above, explain the fix in 1 sentence.'
                )
            elif not code.strip():
                parts.append(
                    f'Give a 1-sentence hint to start Step {example_index + 1}. '
                    f'Use ONLY the lesson text and examples above as your source.'
                )
            else:
                parts.append(
                    f'Guide the student to complete Step {example_index + 1} in 1 sentence. '
                    f'Use ONLY the lesson text above. Do not reveal the full answer.'
                )

            if next_example:
                parts.append(
                    f'\n(After this step the next example is: `{next_example}`. '
                    f'Do NOT mention it yet.)'
                )

            user_prompt = '\n'.join(parts)
            hint_type   = determine_hint_type(code, error)

        else:
            # No examples in topic — free hint grounded in tips only
            parts = []
            if tips:
                parts.append(f'Key points from the lesson "{current_topic.title}":')
                for tip in tips:
                    parts.append(f'  • {tip}')
                parts.append('')
            else:
                parts.append(f'Lesson text:\n{topic_desc[:600]}\n')

            parts.append(
                f"Student's code (cursor line {cursor_line}):\n"
                f"```python\n{code if code.strip() else '(empty)'}\n```\n"
            )

            if error:
                parts.append(
                    f'Error: {error}\n'
                    f'Fix it in 1 sentence using ONLY the lesson key points above.'
                )
            elif not code.strip():
                parts.append(
                    f'Give the very first step for "{current_topic.title}" '
                    f'in 1 sentence, using ONLY the lesson text above.'
                )
            else:
                parts.append(
                    f'Suggest the next step in 1 sentence, using ONLY the '
                    f'lesson key points above. Do not go outside the lesson.'
                )

            user_prompt = '\n'.join(parts)
            hint_type   = determine_hint_type(code, error)

        # ── Call OpenAI ────────────────────────────────────────────
        print("📡 Calling OpenAI (strict topic mode)…")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.2,   # low temperature = less hallucination
            max_tokens=200,
        )
        hint = response.choices[0].message.content.strip()
        print(f"✅ Hint: {hint}")

        # ── Auto-save completion to DB ─────────────────────────────
        if topic_mastered and request.user.is_authenticated:
            try:
                from .models import StudentProgress
                progress, _ = StudentProgress.objects.get_or_create(
                    student=request.user,
                    defaults={'current_topic': current_topic}
                )
                progress.completed_topics.add(current_topic)
                if next_topic:
                    progress.current_topic = next_topic
                progress.save()
                print(f"✅ DB: {current_topic.title} marked complete")
            except Exception as db_err:
                print(f"⚠️  DB save failed: {db_err}")

        return JsonResponse({
            "status":          "success",
            "hint":            hint,
            "type":            hint_type,
            "topic":           current_topic.title,
            "next_topic":      next_topic.title if next_topic else None,
            "next_topic_id":   next_topic.id    if next_topic else None,
            "step_index":      example_index,
            "total_steps":     total_examples,
            "current_example": current_example,
            "next_example":    next_example,
            "completed_topic_id": current_topic.id    if topic_mastered and current_topic else None,  # ← KEY
        })

    except Topics.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Topic not found"}, status=404)
    except Exception as e:
        import traceback; traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def build_database_bound_prompt(code, topic, code_analysis, error):
    """
    STRICT: AI must reuse only lesson examples
    """

    examples = extract_code_examples(topic.desc)

    examples_text = "\n\n".join(examples) if examples else "No code examples found."

    prompt = f"""
YOU MUST FOLLOW THESE RULES STRICTLY:

1. You are ONLY allowed to use the exact syntax patterns shown in the lesson examples.
2. You are NOT allowed to change numbers, variable names, or structure.
3. If suggesting improvement, reuse the exact pattern from examples.
4. DO NOT invent new numbers.
5. DO NOT create new examples.

LESSON TITLE:
{topic.title}

AUTHORIZED CODE EXAMPLES (ONLY THESE ARE ALLOWED):
{examples_text}

STUDENT CODE:
{code if code.strip() else "(empty)"}

Progress Level: {code_analysis['progress_level']}
"""

    if error:
        prompt += "\nFix the error using ONLY the authorized examples above."
    else:
        prompt += "\nGive the next step by reusing the exact example pattern above."

    return prompt

import re

def get_primary_example(topic):
    """
    Extract first python code block from lesson.
    This becomes the authoritative example.
    """
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, topic.desc, re.DOTALL)

    if matches:
        return matches[0].strip()
    
    return None

def compare_with_example(student_code, example_code):
    student = student_code.strip()
    example = example_code.strip()

    if not student:
        return "empty", "Start by typing the example shown in this lesson."

    if student == example:
        return "correct", "Excellent! 🎉 Your syntax is exactly correct. Keep learning!"

    # Check if structure same but small numeric difference
    student_structure = re.sub(r"\d+", "N", student)
    example_structure = re.sub(r"\d+", "N", example)

    if student_structure == example_structure:
        return (
            "minor_error",
            f"Great structure! 👍 Check the numbers carefully.\n\nCorrect example:\n{example}"
        )

    return (
        "incorrect",
        f"Follow the exact syntax shown in this lesson:\n\n{example}"
    )



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def set_current_topic(request, project_id, topic_id):
    """Set the current topic for a student in this project"""
    try:
        from .models import Project, StudentProgress
        from sms.models import Topics
        
        project = Project.objects.get(id=project_id)
        topic = Topics.objects.get(id=topic_id)
        
        # Get or create student progress for this project
        # We'll store it per project, not per course
        progress, created = StudentProgress.objects.get_or_create(
            student=request.user,
            # If your Project has a course field, use it
            # Otherwise, we'll create a workaround
            defaults={'current_topic': topic}
        )
        
        if not created:
            progress.current_topic = topic
            progress.save()
        
        print(f"✅ Student {request.user.username} set topic to: {topic.title}")
        
        return JsonResponse({
            "status": "success",
            "message": f"Now studying: {topic.title}",
            "topic_id": topic.id,
            "topic_title": topic.title
        })
        
    except Exception as e:
        print(f"❌ Error setting topic: {e}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)



@csrf_exempt
def get_code_examples(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"})
    
    try:
        data = json.loads(request.body)
        code = data.get("code", "")
        cursor_line = data.get("cursor_line", 1)
        selected_text = data.get("selected_text", "")
        
        # Build prompt for examples
        prompt = build_examples_prompt(code, cursor_line, selected_text)
        
        # ================= OPENAI CALL =================
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a Python coding tutor. Provide relevant, practical code examples. Always respond with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        
        response_text = response.choices[0].message.content
        
        # Parse response
        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            examples = result.get("examples", [])
            
            return JsonResponse({
                "status": "success",
                "examples": examples
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Failed to parse examples"
            })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            "status": "error",
            "message": str(e),
            "details": traceback.format_exc()
        })


def build_examples_prompt(code, cursor_line, selected_text):
    """Build prompt for getting relevant code examples"""
    
    return f"""Analyze this Python code and provide 3-4 relevant, practical examples that would help the student learn related concepts.

Student's current code:
```python
{code}
```

Based on what they're working on, provide examples that:
1. Build on their current knowledge
2. Show related concepts they should learn next
3. Are simple and practical
4. Include clear explanations

Return ONLY valid JSON in this format:
{{
  "examples": [
    {{
      "category": "input|loops|conditionals|functions|lists|strings|math|files",
      "title": "Short descriptive title",
      "explanation": "1-2 sentences explaining what this example does and why it's useful",
      "code": "Complete, runnable Python code example"
    }}
  ]
}}

IMPORTANT:
- Provide 3-4 examples
- Each example should be complete and runnable
- Keep examples short (5-10 lines max)
- Examples should be progressively more advanced
- Use clear variable names and add comments
- Make sure code is properly formatted with correct indentation

Example response:
{{
  "examples": [
    {{
      "category": "input",
      "title": "Getting Multiple Inputs",
      "explanation": "Learn how to ask for multiple pieces of information and store them in variables.",
      "code": "name = input(\\"Enter your name: \\")\\nage = input(\\"Enter your age: \\")\\ncity = input(\\"Enter your city: \\")\\nprint(f\\"{{name}} is {{age}} years old and lives in {{city}}\\")"
    }},
    {{
      "category": "conditionals",
      "title": "Age Checker",
      "explanation": "Use if-else to make decisions based on user input.",
      "code": "age = int(input(\\"Enter your age: \\"))\\nif age >= 18:\\n    print(\\"You're an adult!\\")\\nelse:\\n    print(\\"You're a minor!\\")"
    }},
    {{
      "category": "loops",
      "title": "Print Multiple Greetings",
      "explanation": "Use a loop to repeat actions multiple times.",
      "code": "name = input(\\"Enter your name: \\")\\nfor i in range(3):\\n    print(f\\"Hello {{name}}! ({{i+1}})\\")"
    }}
  ]
}}
"""




# At the very top of views.py, after all imports
from django.conf import settings
from openai import OpenAI
from .sandbox_runner import run_code


# webprojects/views.py

def award_xp(user, amount=100):
    from datetime import date, timedelta
    xp, _ = StudentXP.objects.get_or_create(student=user)
    
    # Update streak
    today = date.today()
    if xp.last_active == today - timedelta(days=1):
        xp.streak_days += 1
    elif xp.last_active != today:
        xp.streak_days = 1
    xp.last_active = today
    
    xp.total_xp += int(amount)
    xp.save()
    
    return {
        'xp_gained':  int(amount),
        'total_xp':   xp.total_xp,
        'streak':     xp.streak_days,
    }


@login_required
def get_xp_stats(request):
    xp, _ = StudentXP.objects.get_or_create(student=request.user)
    return JsonResponse({
        'status':   'success',
        'total_xp': xp.total_xp,
        'streak':   xp.streak_days,
    })

# ================= OPENAI CLIENT INITIALIZATION =================
# Initialize once when the module loads, not on every request



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json

def _safe_rename(src: Path, dst: Path, retries: int = 30, delay: float = 1.0):
    """Windows can hold file handles open briefly after a process is killed
    (SQLite connections, runserver's autoreload child process, antivirus
    scanning, etc.), causing os.rename to fail with WinError 32 even though
    nothing is actually still using the directory a moment later. Retry
    with backoff instead of failing immediately."""
    last_error = None
    for attempt in range(retries):
        try:
            src.rename(dst)
            return
        except (PermissionError, OSError) as e:
            last_error = e
            time.sleep(delay)
    raise last_error



@login_required
@require_http_methods(["POST"])
def update_active_topic(request):
    """Update the student's current active topic for scoring"""
    try:
        data = json.loads(request.body.decode()) if request.body else {}
        topic_id = data.get('topic_id')
        course_id = data.get('course_id')
        
        if not course_id:
            return JsonResponse({"status": "error", "message": "Course ID is required"}, status=400)
        
        # Get the course
        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Course not found"}, status=404)
        
        # Get or create student progress
        from .models import StudentProgress
        from django.utils import timezone
        
        progress, created = StudentProgress.objects.get_or_create(
            student=request.user,
            course=course
        )
        
        # ===== TIME TRACKING: Record time spent on previous topic =====
        if progress.module_start_time:
            time_spent = (timezone.now() - progress.module_start_time).total_seconds()
            progress.total_time_spent_seconds += int(time_spent)
            print(f"⏱️ Recorded {int(time_spent)}s for previous topic. Total: {progress.total_time_spent_seconds}s")
        
        # Update the current topic
        if topic_id:
            try:
                topic = Topics.objects.get(id=topic_id)
                progress.current_topic = topic
                # ===== Start timer for new topic =====
                progress.module_start_time = timezone.now()
            except Topics.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Topic not found"}, status=404)
        else:
            progress.current_topic = None
            progress.module_start_time = None  # Stop timer if no topic
        
        progress.save(update_fields=['current_topic', 'total_time_spent_seconds', 'module_start_time'])
        
        # ===== Update leaderboard with new time data =====
        from .views_leaderboard import update_leaderboard_entry
        entry = update_leaderboard_entry(request.user, course)
        
        return JsonResponse({
            "status": "success",
            "message": "Active topic updated",
            "current_topic_id": topic_id,
            "total_time_spent_seconds": progress.total_time_spent_seconds,
            "champion_xp": entry.champion_xp if entry else 0,
            "rank": entry.rank if entry else None,
        })
        
    except Exception as e:
        print(f"❌ Error updating active topic: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
        




# OpenAI client (initialize from settings)
client = None
if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
    except ImportError:
        client = None



import shutil
import subprocess
import sys

from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import socket
import time
import psutil  # pip install psutil

# Module-level dict to track running dev servers by project id.
# NOTE: this lives in process memory only — if the host Django process
# restarts (e.g. autoreload), this dict is lost and any still-running
# child `runserver` processes become orphans. Fine for a dev tool; if
# that becomes a problem, persist PIDs to disk/DB instead.

def get_pidfile_path(export_dir):
    return export_dir / ".runserver.pid"


def kill_previous_server(export_dir, project_id):
    """Kill any previous server for this project — whether tracked in
    memory (same process lifetime) or orphaned (host app restarted)."""
    # 1. Try the in-memory tracker first (fast path, same process lifetime)
    old_proc = _running_servers.pop(project_id, None)
    if old_proc and old_proc.poll() is None:
        old_proc.terminate()
        try:
            old_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            old_proc.kill()
            old_proc.wait()

    # 2. Also check the pidfile in case the host app restarted and lost
    # track of it in memory (this is what's biting you right now)
    pidfile = get_pidfile_path(export_dir)
    if pidfile.exists():
        try:
            pid = int(pidfile.read_text().strip())
            if psutil.pid_exists(pid):
                p = psutil.Process(pid)
                p.terminate()
                p.wait(timeout=5)
        except (ValueError, psutil.NoSuchProcess, psutil.TimeoutExpired):
            pass
        finally:
            pidfile.unlink(missing_ok=True)

_running_servers = {}

import socket
import time

def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def get_or_assign_port(project):
    """Get or assign a stable port for this project. Uses a genuinely
    random OS-assigned port (not a fixed scan range) so different
    projects don't all converge on the same low port number."""
    if project.assigned_port and is_port_free(project.assigned_port):
        return project.assigned_port

    port, sock = get_free_port()
    sock.close()  # release the reservation now that we've recorded the port
    project.assigned_port = port
    project.save(update_fields=['assigned_port'])
    print(f"📌 Assigned stable port {port} to project {project.id}")
    return port


def get_free_port():
    """Get an unused port and keep it reserved while we start Django."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    # DON'T close the socket yet - keep it open to reserve the port
    # We'll pass it to the subprocess
    return port, sock



def wait_for_server(port, timeout=20, warmup=True):
    """Wait for the server to accept connections. Returns (True, status_code)
    the moment ANY HTTP response comes back — including error responses.
    An error response means the server is up but the app itself is broken,
    which is a different problem than 'still starting' and shouldn't be
    retried the same way.

    Explicitly bypasses any system HTTP_PROXY/HTTPS_PROXY env vars for this
    request — otherwise `requests` can try to route 127.0.0.1 through a
    proxy (common with VPNs / corporate network tooling), which silently
    times out even though the server is actually up and reachable directly."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                f"http://127.0.0.1:{port}/",
                timeout=5,
                proxies={"http": None, "https": None},
            )
            return True, response.status_code
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(0.3)
    return False, None


def start_dev_server(export_dir, env, project, max_attempts=3):
    """Start Django dev server. Autoreload is left ON (Django's own
    file-watcher) so ordinary .py edits are picked up automatically and
    cheaply, instead of requiring a manual kill+respawn from our side."""

    for attempt in range(max_attempts):
        port = get_or_assign_port(project)
        print(f"🔍 Attempt {attempt + 1}: Using port {port}")

        if is_port_in_use(port):
            print(f"⚠️ Port {port} is in use, trying to kill existing process...")
            try:
                import psutil
                for conn in psutil.net_connections():
                    if conn.laddr.port == port and conn.status == 'LISTEN':
                        try:
                            proc = psutil.Process(conn.pid)
                            proc.terminate()
                            proc.wait(timeout=3)
                            print(f"✅ Killed process {conn.pid} using port {port}")
                        except:
                            pass
            except:
                pass
            time.sleep(1)
            continue

        print(f"🚀 Starting server on port {port} (attempt {attempt + 1})")

        proc = subprocess.Popen(
            [sys.executable, "manage.py", "runserver", "--noreload", "--nothreading" if False else "--noreload", str(port)],
            cwd=export_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for initial bind with longer timeout
        time.sleep(5)

        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            print(f"❌ Server died immediately:")
            print(f"--- stdout ---\n{stdout}")
            print(f"--- stderr ---\n{stderr}")
            continue

        # Check if server is responding with longer timeout
        print(f"⏳ Checking if server is responding on port {port}...")
        up, status_code = wait_for_server(port, timeout=20, warmup=True)

        if up and status_code and status_code >= 500:
            time.sleep(1)
            try:
                response2 = requests.get(f"http://127.0.0.1:{port}/", timeout=2)
                if response2.status_code < 500:
                    return True, response2.status_code
            except:
                pass

            proc.terminate()
            try:
                stdout, stderr = proc.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate()
            raise RuntimeError(
                f"Server started but the app is returning errors (HTTP {status_code}). "
                f"This usually means broken generated code (template syntax error, "
                f"missing view, bad import, etc). Server output:\n{stderr}"
            )

        if up:
            print(f"✅ Server ready on port {port}")
            return proc, port
        else:
            print(f"❌ Server on port {port} not responding, killing it...")
            proc.terminate()
            try:
                stdout, stderr = proc.communicate(timeout=2)
                print(f"--- stdout ---\n{stdout}")
                print(f"--- stderr ---\n{stderr}")
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate()
                print(f"--- stderr (after kill) ---\n{stderr}")
            continue

    raise RuntimeError(f"Could not start dev server after {max_attempts} attempts")



def get_pidfile_path(export_dir):
    return export_dir / ".runserver.pid"


def kill_previous_server(export_dir, project_id):
    """Kill any previous server for this project — whether tracked in
    memory (same process lifetime), orphaned (host app restarted), or
    orphaned with no pidfile at all (last-resort scan by open file)."""
    # 1. Try the in-memory tracker first (fast path, same process lifetime)
    old_proc = _running_servers.pop(project_id, None)
    if old_proc and old_proc.poll() is None:
        old_proc.terminate()
        try:
            old_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            old_proc.kill()
            old_proc.wait()

    # 2. Check the pidfile in case the host app restarted and lost
    # track of it in memory
    pidfile = get_pidfile_path(export_dir)
    if pidfile.exists():
        try:
            pid = int(pidfile.read_text().strip())
            if psutil.pid_exists(pid):
                p = psutil.Process(pid)
                p.terminate()
                p.wait(timeout=5)
        except (ValueError, psutil.NoSuchProcess, psutil.TimeoutExpired):
            pass
        finally:
            pidfile.unlink(missing_ok=True)

    # 3. Last resort: no pidfile at all (e.g. orphan from before this
    # tracking existed, or a crashed write). Scan running processes for
    # one that has this project's db.sqlite3 open.
    db_path = str((export_dir / "db.sqlite3").resolve())
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            for f in proc.open_files():
                if f.path == db_path:
                    proc.terminate()
                    proc.wait(timeout=5)
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            continue

def get_info_path(export_dir):
    return export_dir / ".server_info.json"


def get_live_server_info(export_dir):
    info_path = get_info_path(export_dir)
    print("Checking info_path:", info_path, "exists:", info_path.exists())
    if not info_path.exists():
        return None
    try:
        info = json.loads(info_path.read_text())
        pid = info.get("pid")
        print("Found pid:", pid, "alive:", psutil.pid_exists(pid) if pid else None)
        if pid and psutil.pid_exists(pid):
            return info
    except (json.JSONDecodeError, KeyError):
        pass
    return None




import socket
import time
import secrets
import subprocess
import shutil
import json
import sys
import psutil
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import requests

# Module-level dict to track running dev servers by project id
_running_servers = {}

# Tracks when each project's server was last accessed (run/restart),
# so idle ones can be cleaned up automatically.
_last_touched = {}

IDLE_TIMEOUT_SECONDS = 30 * 60  # 30 minutes


def touch_project(project_id):
    _last_touched[project_id] = time.time()


def sweep_idle_servers():
    """Kill any tracked server that hasn't been touched recently."""
    now = time.time()
    idle_ids = [
        pid for pid, last in _last_touched.items()
        if now - last > IDLE_TIMEOUT_SECONDS
    ]
    for project_id in idle_ids:
        proc = _running_servers.get(project_id)
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            print(f"🧹 Killed idle server for project {project_id}")
        _running_servers.pop(project_id, None)
        _last_touched.pop(project_id, None)


def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return False
        except socket.error:
            return True


def _kill_process_tree(pid, timeout=5):
    """Terminate a process AND all its children. Necessary because
    manage.py runserver (without --noreload) spawns a child reloader
    process — killing only the parent PID leaves the child holding
    file handles open, which causes WinError 32 on directory renames."""
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return

    children = parent.children(recursive=True)
    procs = children + [parent]

    for p in procs:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass

    gone, alive = psutil.wait_procs(procs, timeout=timeout)
    for p in alive:
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass
    psutil.wait_procs(alive, timeout=3)


def kill_previous_server(export_dir, project_id):
    """Kill any previous server for this project, including any child
    processes it spawned (e.g. Django's autoreloader), so no file handles
    in export_dir remain open afterward."""
    print(f"🔪 kill_previous_server called for project {project_id}")
    # 1. Check in-memory tracker
    old_proc = _running_servers.pop(project_id, None)
    if old_proc:
        print(f"   in-memory tracker had a process (pid={old_proc.pid}, still running={old_proc.poll() is None})")
    else:
        print(f"   in-memory tracker had nothing for project {project_id}")
    if old_proc and old_proc.poll() is None:
        try:
            _kill_process_tree(old_proc.pid)
        except Exception as e:
            print(f"⚠️ Process-tree kill failed for in-memory PID {old_proc.pid}: {e}")
            old_proc.terminate()
            try:
                old_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                old_proc.kill()
                old_proc.wait()

    # 2. Check pidfile
    pidfile = get_pidfile_path(export_dir)
    if pidfile.exists():
        try:
            pid = int(pidfile.read_text().strip())
            print(f"   pidfile has pid={pid}, still alive={psutil.pid_exists(pid)}")
            if psutil.pid_exists(pid):
                _kill_process_tree(pid)
                print(f"   killed process tree for pid={pid}")
        except (ValueError, psutil.NoSuchProcess) as e:
            print(f"⚠️ Could not kill PID from pidfile: {e}")
        finally:
            pidfile.unlink(missing_ok=True)

    # 3. Clean up info file
    info_path = get_info_path(export_dir)
    info_path.unlink(missing_ok=True)


def get_pidfile_path(export_dir):
    return export_dir / ".runserver.pid"

def get_info_path(export_dir):
    return export_dir / ".server_info.json"

def get_live_server_info(export_dir):
    """Get info about running server if it's still alive."""
    info_path = get_info_path(export_dir)
    if not info_path.exists():
        return None
    
    try:
        info = json.loads(info_path.read_text())
        pid = info.get("pid")
        port = info.get("port")
        
        # Check if process is still running
        if pid and psutil.pid_exists(pid):
            # Verify server is responding
            if wait_for_server(port, timeout=2):
                return info
            else:
                # Server not responding, kill it
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    p.wait(timeout=5)
                except:
                    pass
                info_path.unlink(missing_ok=True)
                return None
        else:
            # Process is dead
            info_path.unlink(missing_ok=True)
            return None
    except (json.JSONDecodeError, KeyError):
        info_path.unlink(missing_ok=True)
        return None


def _get_admin_credentials_path(project):
    """
    Lives one level ABOVE the export_dir, so it survives the
    shutil.rmtree(export_dir) that happens on every rebuild.
    """
    return (
        Path(settings.BASE_DIR)
        / "generated_projects"
        / f"{project.id}_admin_credentials.json"
    )



def _get_or_create_admin_password(project):
    print(f"[DEBUG] Called for project id={project.id}, current value={project.admin_password!r}")
    if project.admin_password:
        return project.admin_password
    password = secrets.token_urlsafe(12)
    project.admin_password = password
    saved = project.save(update_fields=["admin_password"])
    print(f"[DEBUG] Just saved password={password!r} for project id={project.id}")
    # Immediately re-fetch to confirm it landed
    fresh = Project.objects.get(id=project.id)
    print(f"[DEBUG] Re-fetched from DB: {fresh.admin_password!r}")
    return password

import time


def _force_release_db_lock(db_path):
    """
    Windows locks open files strictly, unlike POSIX. If kill_previous_server
    missed a process (e.g. an orphaned child not tracked in the pidfile),
    this finds anyone still holding db.sqlite3 open and kills them, then
    waits briefly for the OS to actually release the handle.
    """
    db_path_str = str(db_path.resolve())
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            for f in proc.open_files():
                if f.path == db_path_str:
                    proc.terminate()
                    proc.wait(timeout=5)
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            continue

    # Give SQLite / the OS a moment to checkpoint WAL and release the handle
    # after the process actually exits, rather than reading immediately.
    time.sleep(0.3)


def _backup_sqlite_db(export_dir):
    """
    Returns a dict of {filename: bytes} for db.sqlite3 and any WAL/journal
    sidecar files that exist, so an in-flight transaction isn't silently
    dropped by only backing up the main file.
    """
    backup = {}
    for suffix in ("", "-wal", "-shm", "-journal"):
        p = export_dir / f"db.sqlite3{suffix}"
        if p.exists():
            backup[p.name] = p.read_bytes()
    return backup


def _restore_sqlite_db(export_dir, backup):
    for name, content in backup.items():
        (export_dir / name).write_bytes(content)
    if backup:
        print(f"✅ Restored {list(backup.keys())} — user data preserved")


def rebuild_and_start_project(project):
    """Full rebuild: kill any running server, re-export files from DB,
    check/makemigrations/migrate/createsuperuser, and start a fresh
    server. Preserves db.sqlite3 (and its WAL/journal sidecars) across
    rebuilds so user data entered into the generated app isn't lost
    every time this runs."""
    export_dir = (
        Path(settings.BASE_DIR)
        / "generated_projects"
        / str(project.id)
    )

    # Kill any existing server (tracked via pidfile)
    kill_previous_server(export_dir, project.id)

    # Belt-and-suspenders: also kill anyone still holding db.sqlite3 open,
    # in case the tracked process wasn't the only one (or wasn't tracked
    # at all), then give the OS a moment to release the file lock.
    db_path = export_dir / "db.sqlite3"
    if db_path.exists():
        _force_release_db_lock(db_path)

    # Preserve the database (+ WAL/journal sidecars) across rebuilds —
    # only code files get wiped
    db_backup = _backup_sqlite_db(export_dir)

    # Clean and recreate export directory
    if export_dir.exists():
                # Retry rmtree with timeout
        if export_dir.exists():
            for attempt in range(5):
                try:
                    shutil.rmtree(export_dir)
                    break
                except OSError:
                    print(f"⚠️ Directory locked, retrying... ({attempt + 1}/5)")
                    time.sleep(1)
                    # Force release any open handles
                    import gc
                    gc.collect()
            else:
                # If still locked, skip deletion and just overwrite files
                print("⚠️ Could not delete export_dir — overwriting files instead")
    export_dir.mkdir(parents=True, exist_ok=True)

    # Export files
    files = File.objects.filter(project=project)
    if not files.exists():
        return {"status": "error", "message": "No project files found."}

    for f in files:
        full_path = export_dir / f.name
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(f.content, encoding="utf-8")
        print("Exported:", full_path)

    # Restore the database now that fresh code files are in place
    _restore_sqlite_db(export_dir, db_backup)

    # Get project name from settings file
    settings_file = next(
        (f.name for f in files if f.name.endswith("/settings.py")),
        None
    )
    if not settings_file:
        return {"status": "error", "message": "No settings.py found in project files."}
    project_name = settings_file.split("/")[0]

    env = build_subprocess_env(export_dir, project_name)

    # STEP 1 - Django Check
    check = subprocess.run(
        [sys.executable, "manage.py", "check"],
        cwd=export_dir,
        capture_output=True,
        text=True,
        env=env,
    )
    if check.returncode != 0:
        return {
            "status": "error", "step": "check",
            "stdout": check.stdout, "stderr": check.stderr,
        }

    # STEP 2 - Makemigrations
    makemigrations = subprocess.run(
        [sys.executable, "manage.py", "makemigrations"],
        cwd=export_dir,
        capture_output=True,
        text=True,
        env=env,
    )
    if makemigrations.returncode != 0:
        return {
            "status": "error", "step": "makemigrations",
            "stdout": makemigrations.stdout, "stderr": makemigrations.stderr,
        }

    # STEP 3 - Migrate (safe even with a restored DB — Django tracks
    # already-applied migrations inside the DB itself and only runs new ones)
    migrate = subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        cwd=export_dir,
        capture_output=True,
        text=True,
        env=env,
    )
    if migrate.returncode != 0:
        return {
            "status": "error", "step": "migrate",
            "stdout": migrate.stdout, "stderr": migrate.stderr,
        }
    
    def smoke_test_project(export_dir, env, port_for_test=None):
        """Actually boot the app briefly and hit '/' — catches runtime errors
        (TemplateDoesNotExist, missing imports at request time, etc.) that
        check/makemigrations can't see, since those don't render any pages."""
        test_script = (
            "import django, os, sys\n"
            "os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ['DJANGO_SETTINGS_MODULE'])\n"
            "django.setup()\n"
            "from django.test import Client\n"
            "c = Client()\n"
            "resp = c.get('/')\n"
            "print(f'STATUS:{resp.status_code}')\n"
            "if resp.status_code >= 500:\n"
            "    print('ERROR_CONTENT_START')\n"
            "    print(resp.content.decode('utf-8', errors='replace')[:3000])\n"
            "    print('ERROR_CONTENT_END')\n"
        )

        result = subprocess.run(
            [sys.executable, "manage.py", "shell", "-c", test_script],
            cwd=export_dir,
            capture_output=True,
            text=True,
            env=env,
            timeout=15,
        )

        output = result.stdout + result.stderr

        status_match = re.search(r'STATUS:(\d+)', output)
        status_code = int(status_match.group(1)) if status_match else None

        if status_code and status_code >= 500:
            error_match = re.search(r'ERROR_CONTENT_START\n(.*?)\nERROR_CONTENT_END', output, re.DOTALL)
            error_detail = error_match.group(1) if error_match else output[-2000:]
            # Pull out the exception type/message for a clean summary
            exc_match = re.search(r'(\w+Error|\w+Exception):\s*(.+)', error_detail)
            summary = exc_match.group(0) if exc_match else error_detail[:300]
            return False, summary

        if status_code is None:
            return False, f"Smoke test produced no readable status. Output:\n{output[-1000:]}"

        return True, None

    # STEP 4 - Ensure an admin user exists. Only create one on first-ever
    # build (no DB backup existed) — if the DB was restored, the admin
    # user already exists inside it with whatever password it was created
    # with, so don't touch it.
    admin_password = _get_or_create_admin_password(project)

    if not db_backup:
        createsuperuser_env = env.copy()
        createsuperuser_env["DJANGO_SUPERUSER_USERNAME"] = "admin"
        createsuperuser_env["DJANGO_SUPERUSER_EMAIL"] = "admin@example.com"
        createsuperuser_env["DJANGO_SUPERUSER_PASSWORD"] = admin_password

        subprocess.run(
            [sys.executable, "manage.py", "createsuperuser", "--noinput"],
            cwd=export_dir,
            capture_output=True,
            text=True,
            env=createsuperuser_env,
        )

    # STEP 5 - Run Server with retry logic
    try:
        proc, PORT = start_dev_server(export_dir, env, project)
    except RuntimeError as e:
        return {
            "status": "error",
            "step": "runserver",
            "message": str(e),
        }

    # Store server info
    _running_servers[project.id] = proc
    get_pidfile_path(export_dir).write_text(str(proc.pid))
    get_info_path(export_dir).write_text(json.dumps({
        "pid": proc.pid,
        "port": PORT,
        "admin_password": admin_password,
    }))

    # Verify the server one more time before returning
    if not wait_for_server(PORT, timeout=3):
        return {
            "status": "error",
            "step": "verify",
            "message": f"Server started but not responding on port {PORT}",
        }
    
    update_project_port_mapping(project)
    return {
        "status": "success",
        "message": "Project started successfully.",

      "preview_url": f"https://{getattr(project, 'subdomain', None) or f'project-{project.id}'}.codethinkers.org/" if os.environ.get('PRODUCTION') else f"http://127.0.0.1:{port}/",
        "admin_url": f"http://127.0.0.1:{PORT}/admin/",
        "admin_credentials": {"username": "admin", "password": admin_password},
        "check_output": check.stdout,
        "migrate_output": migrate.stdout,
        "port": PORT,
    }



def get_existing_project_context(project):
    existing_apps = set()
    existing_models = set()
    existing_url_namespaces = set()
    existing_templates = set()
    has_auth_urls = False
    has_login_template = False
    has_signup_template = False

    files = File.objects.filter(project=project)

    for f in files:
        content = f.content or ""

        # ── App detection (from apps.py or settings.py INSTALLED_APPS) ──
        if f.name.endswith("apps.py"):
            match = re.search(r"name\s*=\s*['\"]([\w\.]+)['\"]", content)
            if match:
                existing_apps.add(match.group(1))

        # ── Model detection ──
        if f.name.endswith("models.py"):
            for m in re.finditer(r"class\s+(\w+)\s*\(\s*models\.Model", content):
                existing_models.add(m.group(1))

        # ── URL namespace detection (app_name = '...') ──
        if f.name.endswith("urls.py"):
            match = re.search(r"app_name\s*=\s*['\"](\w+)['\"]", content)
            if match:
                existing_url_namespaces.add(match.group(1))

            # ── Explicit auth-urls detection — app_name regex above
            # CANNOT catch this, since django.contrib.auth.urls has no
            # app_name in the project's own code. Check separately.
            if "django.contrib.auth.urls" in content:
                has_auth_urls = True

        # ── Template detection ──
        if "/templates/" in f.name:
            template_path = f.name.split("/templates/", 1)[1]
            existing_templates.add(template_path)

            if template_path in ("registration/login.html", "login.html"):
                has_login_template = True
            if template_path in ("registration/signup.html", "signup.html"):
                has_signup_template = True

    return {
        "existing_apps": sorted(existing_apps),
        "existing_models": sorted(existing_models),
        "existing_url_namespaces": sorted(existing_url_namespaces),
        "existing_templates": sorted(existing_templates),
        "has_auth_urls": has_auth_urls,
        "has_login_template": has_login_template,
        "has_signup_template": has_signup_template,
    }


# views.py
@login_required
@require_http_methods(["POST"])
def update_project_subdomain(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        subdomain = data.get("subdomain", "").strip().lower()
        
        # Validate: only letters, numbers, hyphens
        if subdomain and not re.match(r'^[a-z0-9-]+$', subdomain):
            return JsonResponse({"status": "error", "message": "Only letters, numbers, and hyphens allowed."})
        
        # Check uniqueness
        if subdomain and Project.objects.filter(subdomain=subdomain).exclude(id=project_id).exists():
            return JsonResponse({"status": "error", "message": "This subdomain is already taken."})
        
        project.subdomain = subdomain or None
        project.save(update_fields=['subdomain'])
        
        preview_url = f"https://{subdomain}.codethinkers.org/" if subdomain else f"https://project-{project.id}.codethinkers.org/"
        
        return JsonResponse({
            "status": "success",
            "subdomain": subdomain,
            "preview_url": preview_url,
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def run_project(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id, user=request.user)
        sweep_idle_servers()
        touch_project(project.id)
        export_dir = Path(settings.BASE_DIR) / "generated_projects" / str(project.id)

        force_rebuild = request.GET.get("force") == "1"
        live_info = get_live_server_info(export_dir) if not force_rebuild else None

        if live_info:
            port = live_info['port']
            return JsonResponse({
                "status": "success",
                "message": "Project already running.",

              "preview_url": f"https://{getattr(project, 'subdomain', None) or f'project-{project.id}'}.codethinkers.org/" if os.environ.get('PRODUCTION') else f"http://127.0.0.1:{port}/",
                "admin_url": f"http://127.0.0.1:{port}/admin/",
                "admin_credentials": {
                    "username": "admin",
                    "password": project.admin_password or "admin123",
                },
                "port": port,
            })

        files = File.objects.filter(project=project)
        if not files.exists():
            return JsonResponse({
                "status": "error",
                "message": "No project files found."
            })

        settings_file = files.filter(name__endswith="/settings.py").first()
        if not settings_file:
            return JsonResponse({
                "status": "error",
                "message": "No settings.py found in project files."
            })
        project_name = settings_file.name.split("/")[0]

        # Re-apply everything already saved in the DB, through the same
        # staged pipeline used for builds/edits — static validation,
        # staging export, manage.py check, migrations, smoke test, and
        # rollback-on-failure. "Run" is just "apply with zero new changes."
        pseudo_changes = [
            {"file_path": f.name, "action": "update", "content": f.content}
            for f in files
        ]

        apply_result = _attempt_apply(
            project, pseudo_changes,
            requires_migration=True,
            requires_server_restart=True,
        )

        if not apply_result["ok"]:
            return JsonResponse({
                "status": "error",
                "step": "apply",
                "message": "Project failed validation or crashed on load.",
                "detail": apply_result["failure_summary"],
                "validation_errors": apply_result.get("validation_errors"),
                "smoke_test_errors": apply_result.get("smoke_test_errors"),
            })

        # ── Ensure an admin user exists (not handled by _attempt_apply) ──
        if not project.admin_password:
            project.admin_password = secrets.token_urlsafe(12)
            project.save(update_fields=['admin_password'])
        admin_password = project.admin_password

        env = build_subprocess_env(export_dir, project_name, project.id)
        create_admin_script = f'''
from django.contrib.auth import get_user_model
User = get_user_model()
user, created = User.objects.get_or_create(
    username="admin",
    defaults={{'email': 'admin@example.com', 'is_superuser': True, 'is_staff': True}}
)
user.set_password("{admin_password}")
user.save()
print("Admin user setup complete")
'''
        subprocess.run(
            [sys.executable, "manage.py", "shell", "-c", create_admin_script],
            cwd=export_dir, capture_output=True, text=True, env=env,
        )

        payload = apply_result["payload"]
        restart_result = payload.get("restart_result")
        port = restart_result.get("port") if isinstance(restart_result, dict) else project.assigned_port

        if not port:
            return JsonResponse({
                "status": "error",
                "step": "verify",
                "message": "Project applied successfully but no server port was returned.",
            })
        
        update_project_port_mapping(project)
        return JsonResponse({
            "status": "success",
            "message": "Project started successfully.",

         "preview_url": f"https://{getattr(project, 'subdomain', None) or f'project-{project.id}'}.codethinkers.org/" if os.environ.get('PRODUCTION') else f"http://127.0.0.1:{port}/",
            "admin_url": f"http://127.0.0.1:{port}/admin/",
            "admin_credentials": {
                "username": "admin",
                "password": admin_password,
            },
            "port": port,
            "migration_result": payload.get("migration_result"),
        })

    except Exception as e:
        print(f"❌ Error in run_project: {traceback.format_exc()}")
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=500)
    



#ai build section with app helpers

def normalize_name(raw, fallback="app"):
    name = re.sub(r'[^a-zA-Z0-9_]', '', raw or '').lower()
    if not name or name[0].isdigit():
        name = f"{fallback}_{name}" if name else fallback
    return name


def build_apps_py(app_name):
    class_name = app_name.capitalize() + "Config"
    return f'''from django.apps import AppConfig


class {class_name}(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{app_name}"
'''

def inject_admin_branding(urls_content, project_name, app_name):
    """Sets a custom site_header/site_title/index_title on the admin site,
    replacing the default 'Django administration' branding everywhere it
    appears (page header, browser tab title, and the login page)."""
    display_name = project_name.replace('_', ' ').title()

    branding_block = (
        f"\nadmin.site.site_header = '{display_name} Admin'\n"
        f"admin.site.site_title = '{display_name}'\n"
        f"admin.site.index_title = 'Dashboard'\n"
    )

    if "from django.contrib import admin" in urls_content:
        urls_content = urls_content.replace(
            "from django.contrib import admin",
            "from django.contrib import admin" + branding_block,
            1
        )
    else:
        urls_content = "from django.contrib import admin\n" + branding_block + urls_content

    return urls_content


def build_admin_custom_css():
    return """
/* ── Modern admin theme ── */
:root {
    --primary: #4f46e5;
    --primary-fg: #fff;
    --header-bg: #1e1b3a;
    --header-color: #ffffff;
    --link-fg: #4f46e5;
    --link-hover-color: #4338ca;
    --link-selected-fg: #4f46e5;
    --hairline-color: #e5e7eb;
    --border-color: #e5e7eb;
    --button-bg: #4f46e5;
    --button-hover-bg: #4338ca;
    --default-button-bg: #4f46e5;
    --default-button-hover-bg: #4338ca;
    --close-button-bg: #6b7280;
    --close-button-hover-bg: #4b5563;
    --delete-button-bg: #dc2626;
    --delete-button-hover-bg: #b91c1c;
    --object-tools-bg: #4f46e5;
    --object-tools-hover-bg: #4338ca;
    --font-family-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

body { font-family: var(--font-family-primary); background: #f9fafb; }

#header {
    background: var(--header-bg);
    color: var(--header-color);
    padding: 14px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}
#header a:link, #header a:visited { color: #fff; }
#branding h1 { font-weight: 700; font-size: 20px; }

.module { border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid var(--border-color); }
.module h2, .module caption { background: #f3f4f6; color: #111827; font-weight: 600; }

.button, input[type=submit], input[type=button], .submit-row input, a.button {
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    box-shadow: none;
}

#changelist-filter { border-radius: 10px; border: 1px solid var(--border-color); }
#changelist-filter h2 { border-radius: 10px 10px 0 0; }

.paginator { border-radius: 8px; }

/* Login page */
.login #container {
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    overflow: hidden;
    max-width: 420px;
    margin-top: 80px;
}
.login #header {
    text-align: center;
    padding: 28px 24px;
}
.login .form-row { padding: 12px 24px; }
.login .submit-row { padding: 16px 24px 24px; }
.login .submit-row input {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background: var(--primary);
    font-size: 15px;
}
.login .submit-row input:hover { background: var(--button-hover-bg) !important; }
"""


def build_admin_base_site_html():
    return """{% extends "admin/base_site.html" %}
{% load static %}
{% block extrastyle %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'admin/css/custom_admin.css' %}">
{% endblock %}
"""


def inject_installed_app(settings_content, app_name):
    """Add app_name to INSTALLED_APPS if not already present."""
    if not settings_content:
        return settings_content
    if f"'{app_name}'" in settings_content or f'"{app_name}"' in settings_content:
        return settings_content  # already registered
    pattern = r'(INSTALLED_APPS\s*=\s*\[)'
    replacement = rf"\1\n    '{app_name}',"
    new_content, count = re.subn(pattern, replacement, settings_content, count=1)
    if count == 0:
        new_content = settings_content + f"\n\nINSTALLED_APPS += ['{app_name}']\n"
    return new_content


def validate_and_repair_python_files(files_dict):
    """Compile-check all Python files, auto-repair f-string quote collisions."""
    unrecoverable = []
    
    if not files_dict:
        return {}, unrecoverable
    
    for path, content in list(files_dict.items()):
        if not path.endswith(".py") or not content:
            continue
        
        # Fix "from x import y," → "from x import y" (AI common mistake)
        if path.endswith("urls.py"):
            content = re.sub(r'(from django\.urls import path),(\s*\n)', r'\1\2', content)
        
        try:
            compile(content, path, "exec")
            continue
        except SyntaxError:
            pass

        repaired = repair_fstring_quote_collision(content)
        try:
            compile(repaired, path, "exec")
            files_dict[path] = repaired
            print(f"🔧 Auto-repaired f-string quote collision in {path}")
        except SyntaxError as e2:
            unrecoverable.append(f"{path}: {e2.msg} at line {e2.lineno}")
            print(f"❌ Unrecoverable syntax error in {path}: {e2.msg} at line {e2.lineno}")
    
    return files_dict, unrecoverable



def _assemble_and_autofix_scaffold_files(app_data, app_name, project_name, settings_content, urls_content):
    """Builds the full new_files dict from AI-generated app_data, running every
    deterministic auto-fix pass (template path normalization, missing templates,
    missing views/urls/admin for any model lacking full wiring). This MUST be
    used for both the first attempt and any retry — skipping it on retry is
    what caused retries to reproduce the same validation failures despite the
    AI's output actually changing each time."""

    default_models = app_data.get("models_py", "") or "from django.db import models\n\n# No models needed for this app\n"
    default_admin = app_data.get("admin_py", "") or "from django.contrib import admin\n\n# Register your models here\n"
    default_urls = app_data.get("urls_py", "") or f"app_name = '{app_name}'\n\nurlpatterns = []\n"
    default_tests = app_data.get("tests_py", "") or "from django.test import TestCase\n\n# Create your tests here\n"

    views_content_check = app_data.get("views_py", "")
    default_forms = app_data.get("forms_py") or None
    if default_forms and "class " in default_forms and ":" in default_forms:
        pass
    else:
        default_forms = None

    if not default_forms and ("from .forms import" in views_content_check or "from forms import" in views_content_check):
        form_imports = re.findall(r'from .forms import ([\w,\s]+)', views_content_check)
        form_classes = [f.strip() for f in form_imports[0].split(',')] if form_imports else []
        forms_code = "from django import forms\nfrom .models import *\n\n"
        for form_class in form_classes:
            forms_code += f"class {form_class}(forms.ModelForm):\n    class Meta:\n        model = None\n        fields = '__all__'\n\n"
        default_forms = forms_code.strip()

    new_files = {
        "manage.py": build_manage_py(project_name),
        f"{project_name}/__init__.py": "",
        f"{project_name}/settings.py": settings_content,
        f"{project_name}/urls.py": urls_content,
        f"{project_name}/asgi.py": build_asgi_py(project_name),
        f"{project_name}/wsgi.py": build_wsgi_py(project_name),
        f"{project_name}/templates/admin/base_site.html": build_admin_base_site_html(),
        "static/admin/css/custom_admin.css": build_admin_custom_css(),
        f"{app_name}/__init__.py": "",
        f"{app_name}/apps.py": build_apps_py(app_name),
        f"{app_name}/migrations/__init__.py": "",
        f"{app_name}/models.py": default_models,
        f"{app_name}/views.py": app_data.get("views_py", ""),
        f"{app_name}/admin.py": default_admin,
        f"{app_name}/urls.py": default_urls,
        f"{app_name}/tests.py": default_tests,
        "requirements.txt": "Pillow>=10.0.0\npython-docx>=1.0.0\n",
    }
    if default_forms:
        new_files[f"{app_name}/forms.py"] = default_forms

    template_files = app_data.get("templates", {}) or {}
    for template_name, template_content in template_files.items():
        safe_name = template_name.strip().lstrip("/").split("/")[-1]
        new_files[f"{app_name}/templates/{safe_name}"] = template_content

    # GUARANTEE base.html exists
    base_html_path = f"{app_name}/templates/base.html"
    if base_html_path not in new_files:
        app_type_hint = app_data.get("thinking", {}).get("app_type", "")
        new_files[base_html_path] = _fallback_base_html(app_name, project_name, app_type_hint)
        print(f"🔧 Auto-created missing base.html for {app_name}")

    # Auto-fix: missing components
    all_template_content = "\n".join(
        v for k, v in new_files.items() if k.startswith(f"{app_name}/templates/") and v
    )
    component_refs = set(re.findall(
        r"""\{%\s*include\s+['"]([^'"]+)['"]""", all_template_content
    ))
    for comp_ref in component_refs:
        comp_path = f"{app_name}/templates/{comp_ref}"
        if comp_path not in new_files:
            new_files[comp_path] = _fallback_component_html(comp_ref)
            print(f"🔧 Auto-created missing component: {comp_ref}")

    # Auto-fix: templates referenced by template_name= but not provided
    views_content = new_files.get(f"{app_name}/views.py", "")
    if views_content:
        template_refs = set(re.findall(r"template_name\s*=\s*['\"]([^'\"]+)['\"]", views_content))
        existing_templates = {k.split('/')[-1] for k in new_files if '/templates/' in k}
        for tpl in template_refs:
            if tpl not in existing_templates:
                tpl_path = f"{app_name}/templates/{tpl}"
                new_files[tpl_path] = _fallback_template_html(tpl, project_name)
                print(f"🔧 Auto-created missing template: {tpl}")

    # Auto-fix: every model needs at least a ListView as safety net
    models_content = new_files.get(f"{app_name}/models.py", "")
    views_content = new_files.get(f"{app_name}/views.py", "")
    urls_content_app = new_files.get(f"{app_name}/urls.py", "")
    admin_content = new_files.get(f"{app_name}/admin.py", "")

    if models_content:
        model_names = re.findall(r'class\s+(\w+)\s*\(\s*models\.Model\s*\)', models_content)

        for model_name in model_names:
            model_lower = model_name.lower()
            has_view = f"model = {model_name}" in views_content or f"{model_name}.objects" in views_content
            has_url = f"{model_lower}_list" in urls_content_app

            if not has_view:
                other_views_exist = bool(re.findall(r'class\s+\w+(?:ListView|DetailView|CreateView|UpdateView|DeleteView)', views_content))
            
                if not other_views_exist and 'HomeView' in views_content:
                    print(f"ℹ️ Model '{model_name}' has no views (private app — admin handles it)")
                    # Still ensure the model is imported in admin.py even
                    # though we're skipping view generation — admin.py may
                    # already reference this model (e.g. @admin.register)
                    # without importing it.
                    if f"import {model_name}" not in admin_content and "from .models import *" not in admin_content:
                        if "from .models import" in admin_content:
                            admin_content = re.sub(
                                r'from \.models import (.+)',
                                rf'from .models import \1, {model_name}',
                                admin_content
                            )
                        else:
                            admin_content = f"from .models import {model_name}\n" + admin_content
                        print(f"🔧 Auto-added import for {model_name} in admin.py (private/no-view model)")
                    continue

                print(f"⚠️ Model '{model_name}' has no views — generating minimal ListView fallback")
                if 'from django.views.generic import ListView' not in views_content:
                    views_content = 'from django.views.generic import ListView\n' + views_content
                if 'from .models import' not in views_content:
                    views_content = f'from .models import {model_name}\n' + views_content
                elif model_name not in views_content:
                    views_content = re.sub(r'from \.models import (.+)', rf'from .models import \1, {model_name}', views_content)

                views_content += f'''
class {model_name}ListView(ListView):
    template_name = '{model_lower}_list.html'
    model = {model_name}
    paginate_by = 25
    ordering = ['-id']
'''

            # Auto-generate missing form only if CreateView/UpdateView already exist
            if f'class {model_name}CreateView' in views_content or f'class {model_name}UpdateView' in views_content:
                forms_content = new_files.get(f"{app_name}/forms.py", "")
                if not forms_content:
                    forms_content = "from django import forms\nfrom .models import *\n\n"
                if f"class {model_name}Form" not in forms_content:
                    if f"import {model_name}" not in forms_content and "from .models import *" not in forms_content:
                        if "from .models import" in forms_content:
                            forms_content = re.sub(
                                r'from \.models import (.+)',
                                rf'from .models import \1, {model_name}',
                                forms_content
                            )
                        else:
                            forms_content = f"from .models import {model_name}\n" + forms_content

                    forms_content += f'''
class {model_name}Form(forms.ModelForm):
    class Meta:
        model = {model_name}
        fields = '__all__'
'''
                    new_files[f"{app_name}/forms.py"] = forms_content
                    print(f"🔧 Auto-created missing form: {model_name}Form (with import)")

            # Auto-generate missing URL patterns for views that exist
            if not has_url:
                existing_view_names = set()
                if f'class {model_name}ListView' in views_content:
                    existing_view_names.add('list')
                if f'class {model_name}DetailView' in views_content:
                    existing_view_names.add('detail')
                if f'class {model_name}CreateView' in views_content:
                    existing_view_names.add('create')
                if f'class {model_name}UpdateView' in views_content:
                    existing_view_names.add('update')
                if f'class {model_name}DeleteView' in views_content:
                    existing_view_names.add('delete')

                if existing_view_names:
                    print(f"🔧 Auto-generating missing URL patterns for model: {model_name}")
                    missing_urls = ""
                    if 'list' in existing_view_names:
                        missing_urls += f"    path('{model_lower}/', views.{model_name}ListView.as_view(), name='{model_lower}_list'),\n"
                    if 'detail' in existing_view_names:
                        missing_urls += f"    path('{model_lower}/<int:pk>/', views.{model_name}DetailView.as_view(), name='{model_lower}_detail'),\n"
                    if 'create' in existing_view_names:
                        missing_urls += f"    path('{model_lower}/create/', views.{model_name}CreateView.as_view(), name='{model_lower}_create'),\n"
                    if 'update' in existing_view_names:
                        missing_urls += f"    path('{model_lower}/<int:pk>/update/', views.{model_name}UpdateView.as_view(), name='{model_lower}_update'),\n"
                    if 'delete' in existing_view_names:
                        missing_urls += f"    path('{model_lower}/<int:pk>/delete/', views.{model_name}DeleteView.as_view(), name='{model_lower}_delete'),\n"

                    if '\n]' in urls_content_app:
                        urls_content_app = urls_content_app.replace('\n]', '\n' + missing_urls + ']', 1)
                    else:
                        urls_content_app += f"\nurlpatterns = [\n{missing_urls}]\n"

            # Ensure the model is imported in admin.py
            if f"import {model_name}" not in admin_content and "from .models import *" not in admin_content:
                if "from .models import" in admin_content:
                    admin_content = re.sub(
                        r'from \.models import (.+)',
                        rf'from .models import \1, {model_name}',
                        admin_content
                    )
                    print(f"🔧 Auto-added import for {model_name} in admin.py (appended to existing)")
                else:
                    admin_content = f"from .models import {model_name}\n" + admin_content
                    print(f"🔧 Auto-added import for {model_name} in admin.py (new import line)")

            # Auto-generate missing admin registration with list_select_related
            if f"class {model_name}Admin" not in admin_content:
                fk_fields = _extract_fk_fields_per_model(models_content).get(model_name, set())
                select_related_line = ""
                if fk_fields:
                    select_related_line = f"    list_select_related = {tuple(sorted(fk_fields))}\n"

                missing_admin = f'''
@admin.register({model_name})
class {model_name}Admin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('id', '__str__', 'created_at')
    search_fields = ('id',)
    list_per_page = 25
{select_related_line}'''
                admin_content += missing_admin
                print(f"🔧 Auto-created admin for {model_name} with list_select_related={sorted(fk_fields) if fk_fields else 'none'}")

    # Auto-fix: Add list_select_related to existing admin classes missing it
    if models_content and admin_content:
        fk_map = _extract_fk_fields_per_model(models_content)
        for model_name, fk_fields in fk_map.items():
            if not fk_fields:
                continue
            pattern = rf'(@admin\.register\({model_name}\).*?class\s+\w+Admin\([^)]+\).*?)(?=\n@admin\.register|\nclass\s|\Z)'
            match = re.search(pattern, admin_content, re.DOTALL)
            if match and 'list_select_related' not in match.group(1):
                replacement = match.group(1).replace(
                    'list_per_page = 25',
                    f'list_per_page = 25\n    list_select_related = {tuple(sorted(fk_fields))}'
                )
                admin_content = admin_content.replace(match.group(1), replacement)
                print(f"🔧 Auto-added list_select_related for {model_name}Admin: {sorted(fk_fields)}")

    # Auto-fix: Remove self.request.user if no auth
    if views_content:
        views_content = re.sub(
            r'(\s+)form\.instance\.author\s*=\s*self\.request\.user',
            r'\1# Auto-fix: removed self.request.user (no auth requested)\n\1form.instance.author = None',
            views_content
        )
        views_content = re.sub(
            r'(\s+)(\w+)\s*=\s*self\.request\.user',
            r'\1# Auto-fix: removed self.request.user to avoid LoginRequiredMixin\n\1# \2 = self.request.user',
            views_content
        )

    # Ensure app urls.py is wired into root urls.py
    root_urls_path = f"{project_name}/urls.py"
    root_urls_content = new_files.get(root_urls_path, "")
    if root_urls_content and f"include('{app_name}.urls')" not in root_urls_content:
        root_urls_content = inject_url_include(root_urls_content, app_name)
        new_files[root_urls_path] = root_urls_content
        print(f"🔧 Auto-wired {app_name}.urls into root urls.py")

    # Write the auto-fixed content back
    new_files[f"{app_name}/views.py"] = views_content
    new_files[f"{app_name}/admin.py"] = admin_content
    new_files[f"{app_name}/urls.py"] = urls_content_app

    new_files = ensure_proper_html_structure_for_files(new_files, app_name)
    
 
    # Re-run template auto-fix for views that were JUST generated
    if views_content:
        template_refs = set(re.findall(r"template_name\s*=\s*['\"]([^'\"]+)['\"]", views_content))
        existing_templates = {k.split('/')[-1] for k in new_files if '/templates/' in k}
        for tpl in template_refs:
            if tpl not in existing_templates:
                tpl_path = f"{app_name}/templates/{tpl}"
                new_files[tpl_path] = _fallback_template_html(tpl, project_name)
                print(f"🔧 Auto-created missing template (post-fix): {tpl}")

    new_files, _syntax_errors = validate_and_repair_python_files(new_files)
    return new_files


def _fallback_base_html(app_name, project_name, app_type=""):
    display_name = project_name.replace('_', ' ').title()
    app_type_lower = (app_type or "").lower()

    if "private" in app_type_lower or "admin" in app_type_lower or "internal" in app_type_lower:
        footer_html = f'''<footer class="bg-gray-800 text-white mt-auto">
        <div class="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-400">
            &copy; {{% now "Y" %}} {display_name}. Internal use only. All rights reserved.
        </div>
    </footer>'''
    elif "blog" in app_type_lower or "content" in app_type_lower or "read-only" in app_type_lower:
        footer_html = f'''<footer class="bg-gray-800 text-white mt-auto">
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                    <h3 class="text-lg font-semibold mb-4">{display_name}</h3>
                    <p class="text-gray-400 text-sm">Your source for quality content.</p>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="/" class="hover:text-white transition">Home</a></li>
                        <li><a href="/admin/" class="hover:text-white transition">Admin</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Connect</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="#" class="hover:text-white transition">Twitter</a></li>
                        <li><a href="#" class="hover:text-white transition">LinkedIn</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-700 mt-8 pt-6 text-center text-sm text-gray-400">
                &copy; {{% now "Y" %}} {display_name}. All rights reserved.
            </div>
        </div>
    </footer>'''
    else:
        # Default: Footer 3 (SaaS) — safest general-purpose choice
        footer_html = f'''<footer class="bg-gray-800 text-white mt-auto">
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div>
                    <h3 class="text-lg font-semibold mb-4">{display_name}</h3>
                    <p class="text-gray-400 text-sm">Built with Django & Tailwind CSS.</p>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Product</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="/" class="hover:text-white transition">Home</a></li>
                        <li><a href="/admin/" class="hover:text-white transition">Admin</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Support</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="#" class="hover:text-white transition">Help Center</a></li>
                        <li><a href="#" class="hover:text-white transition">Contact</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Legal</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="#" class="hover:text-white transition">Privacy</a></li>
                        <li><a href="#" class="hover:text-white transition">Terms</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-700 mt-8 pt-6 text-center text-sm text-gray-400">
                &copy; {{% now "Y" %}} {display_name}. All rights reserved.
            </div>
        </div>
    </footer>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% block title %}}{display_name}{{% endblock %}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen flex flex-col">
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <a href="/" class="text-lg font-semibold text-gray-900">{display_name}</a>
                <div class="flex items-center gap-3">
                    <a href="/admin/" class="text-sm text-gray-600 hover:text-gray-900">Admin</a>
                </div>
            </div>
        </div>
    </nav>
    {{% if messages %}}
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 space-y-2">
        {{% for message in messages %}}
        <div class="rounded-md p-4 text-sm {{% if message.tags == 'success' %}}bg-emerald-50 text-emerald-800{{% elif message.tags == 'error' %}}bg-red-50 text-red-800{{% else %}}bg-blue-50 text-blue-800{{% endif %}}">
            {{{{ message }}}}
        </div>
        {{% endfor %}}
    </div>
    {{% endif %}}
    <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {{% block content %}}{{% endblock %}}
    </main>
    {{% block footer %}}
    {footer_html}
    {{% endblock %}}
</body>
</html>'''




def _fallback_component_html(component_name):
    """Minimal, safe fallback for any components/*.html referenced but not
    generated. Not styled to match the real component — just enough to not
    crash the page. The validator should flag these so a real one gets
    generated on the next pass, this is a last-resort safety net only."""
    name = component_name.replace('.html', '').replace('_', ' ').replace('components/', '').title()
    if 'pagination' in component_name:
        return '''{% if is_paginated %}
<div class="flex justify-center gap-2 mt-6">
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}" class="px-3 py-2 text-sm rounded-md border border-gray-200 text-gray-600 hover:bg-gray-50">Previous</a>
    {% endif %}
    <span class="px-3 py-2 text-sm text-gray-600">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}" class="px-3 py-2 text-sm rounded-md border border-gray-200 text-gray-600 hover:bg-gray-50">Next</a>
    {% endif %}
</div>
{% endif %}'''
    if 'empty_state' in component_name:
        return '''<div class="text-center py-12">
    <p class="text-gray-500">No items found.</p>
</div>'''
    if 'card' in component_name:
        return '''<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition">
    <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
        </svg>
        <div>
            <h3 class="text-gray-900 font-medium">{{ title }}</h3>
            <p class="text-sm text-gray-500 mt-1">{{ subtitle }}</p>
        </div>
    </div>
</div>'''
    return f'<!-- Auto-generated placeholder for {name} -->'


    
def _fallback_template_html(tpl_name, project_name, model_name=None, title=None):
    heading = f"{model_name} {title}" if model_name else tpl_name.replace('.html', '').replace('_', ' ').title()
    return (
        '{% extends "base.html" %}\n'
        '{% block content %}\n'
        f'<h2 class="text-2xl font-bold text-gray-800 mb-4">{heading}</h2>\n'
        '<p class="text-gray-600">Content coming soon.</p>\n'
        '{% endblock %}\n'
    )

def ensure_proper_html_structure_for_files(new_files, app_name):
    """Same HTML-structure normalization as the original ensure_proper_html_structure,
    adapted to operate on the assembled new_files dict (path -> content) instead of
    the raw templates dict, so it works after auto-fix templates have been merged in too."""
    TAILWIND_SCRIPT = '<script src="https://cdn.tailwindcss.com"></script>'
    prefix = f"{app_name}/templates/"
    for path in list(new_files.keys()):
        if not path.startswith(prefix) or not new_files[path]:
            continue
        content = new_files[path]

        # Templates using inheritance (the standard pattern per
        # 10_ui_architecture.md) must NOT be wrapped in a full HTML
        # document — they intentionally have no <!DOCTYPE>/<html>/<body>,
        # since base.html owns all of that. Wrapping them here would break
        # Django's template inheritance (extends must be the first tag).
        if '{% extends' in content:
            new_files[path] = content
            continue

        content = re.sub(r'<link[^>]*tailwind[^>]*>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<script[^>]*tailwindcss[^>]*></script>', '', content, flags=re.IGNORECASE)
        has_doctype = '<!DOCTYPE html>' in content or '<!doctype html>' in content
        has_html = '<html' in content
        has_head = '<head>' in content
        has_body = '<body' in content
        if has_doctype and has_html and has_head and has_body:
            if TAILWIND_SCRIPT not in content:
                content = content.replace('<head>', '<head>\n    ' + TAILWIND_SCRIPT)
        else:
            name = path[len(prefix):]
            title = name.replace('.html', '').replace('_', ' ').title()
            if has_body:
                body_start = content.find('<body')
                body_content = content[body_start:]
                if not has_head:
                    content = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>' + title + '</title>\n    ' + TAILWIND_SCRIPT + '\n</head>\n' + body_content + '\n</html>'
            else:
                content = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>' + title + '</title>\n    ' + TAILWIND_SCRIPT + '\n</head>\n<body class="bg-gray-50 min-h-screen flex flex-col">\n' + content + '\n</body>\n</html>'
        new_files[path] = content
    return new_files


def inject_url_include(urls_content, app_name):
    """Add an include() route for the app's urls.py and make it the root URL."""
    if not urls_content:
        urls_content = (
            "from django.contrib import admin\n"
            "from django.urls import path, include\n\n"
            "urlpatterns = [\n"
            f"    path('', include('{app_name}.urls')),\n"  # App is at root
            "    path('admin/', admin.site.urls),\n"
            "]\n"
        )
        return urls_content

    # Check if already wired
    if f"include('{app_name}.urls')" in urls_content or f'include("{app_name}.urls")' in urls_content:
        return urls_content

    # Add include import if missing
    if "from django.urls import" in urls_content:
        # Check if include is already imported
        import_lines = [l for l in urls_content.split('\n') if 'from django.urls import' in l]
        if import_lines and 'include' not in import_lines[0]:
            urls_content = re.sub(
                r'from django\.urls import (.+)',
                lambda m: f"from django.urls import {m.group(1).rstrip()}, include",
                urls_content,
                count=1,
            )
    elif "from django.urls import" not in urls_content:
        urls_content = "from django.urls import path, include\n" + urls_content

    # ===== FIX: Remove duplicate app_name if it exists =====
    # Remove any existing app_name declaration to avoid duplicate namespace warnings
    urls_content = re.sub(
        r'app_name\s*=\s*[\'"][^\'"]+[\'"]\s*\n',
        '',
        urls_content
    )

    # Insert the app as the root URL pattern

    pattern = r'(urlpatterns\s*=\s*\[)'
    replacement = rf"\1\n    path('', include('{app_name}.urls')),  # App at root"
    new_content, count = re.subn(pattern, replacement, urls_content, count=1)
    
    if count == 0:
        # If urlpatterns not found, append it
        new_content = urls_content + f"\n\nurlpatterns = [\n    path('', include('{app_name}.urls')),\n    path('{app_name}/', include('{app_name}.urls')),\n]\n"
    
    return new_content



def build_subprocess_env(export_dir, project_name, project_id=None):
    """
    Build environment for subprocess with:
    - Persistent database location (survives rebuilds)
    - WAL mode enabled for better concurrency
    - Proper timeout settings
    """
    env = os.environ.copy()
    env.pop("DJANGO_SETTINGS_MODULE", None)
    env["DJANGO_SETTINGS_MODULE"] = f"{project_name}.settings"
    env["PYTHONPATH"] = str(export_dir)
    
    # Store database in persistent location on disk (survives rebuilds)
    from django.conf import settings
    persistent_db_dir = Path(settings.BASE_DIR) / 'project_databases'
    persistent_db_dir.mkdir(parents=True, exist_ok=True)
    
    # Use consistent naming: project_id is enough (project_name might change)
    if project_id:
        db_filename = f"project_{project_id}.sqlite3"
    else:
        db_filename = f"{project_name}.sqlite3"
    
    db_path = persistent_db_dir / db_filename
    env["DB_PATH"] = str(db_path)
    
    # ── Initialize SQLite with WAL mode if DB exists ──
    if db_path.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            conn.execute('PRAGMA journal_mode=WAL;')
            conn.execute('PRAGMA synchronous=NORMAL;')
            conn.execute('PRAGMA busy_timeout=5000;')
            conn.execute('PRAGMA cache_size=-8000;')  # 8MB cache
            conn.execute('PRAGMA foreign_keys=ON;')
            conn.execute('PRAGMA temp_store=MEMORY;')
            conn.close()
            print(f"⚡ SQLite optimized (WAL mode) for {db_filename}")
        except Exception as e:
            print(f"⚠️ SQLite optimization skipped: {e}")
    
    return env



def build_manage_py(project_name):
    return f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
'''


def build_wsgi_py(project_name):
    return f'''import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")

application = get_wsgi_application()
'''


def build_asgi_py(project_name):
    return f'''import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")

application = get_asgi_application()
'''


def build_settings_py(project_name):
    template = '''"""Django settings for __PROJECT_NAME__ project."""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.codethinkers.org']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '__PROJECT_NAME__.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / '__PROJECT_NAME__' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '__PROJECT_NAME__.wsgi.application'

# ── Database with persistent path (survives rebuilds) ──
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DB_PATH', str(BASE_DIR / 'db.sqlite3')),
        'OPTIONS': {
            'timeout': 20,  # Wait up to 20 seconds for lock release
        },
    }
}

# ── Enable WAL mode for better concurrent read/write ──
from django.db.backends.signals import connection_created

def _set_sqlite_pragmas(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA journal_mode=WAL;')
        cursor.execute('PRAGMA synchronous=NORMAL;')
        cursor.execute('PRAGMA busy_timeout=5000;')
        cursor.execute('PRAGMA cache_size=-8000;')  # 8MB cache
        cursor.execute('PRAGMA foreign_keys=ON;')
        cursor.execute('PRAGMA temp_store=MEMORY;')

connection_created.connect(_set_sqlite_pragmas)


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / 'static']   # so custom_admin.css is found
STATIC_URL = 'static/'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
    return template.replace("__PROJECT_NAME__", project_name)


def _check_login_required_on_user_filtered_views(all_files):
    """Blocks if a view filters by self.request.user (or sets it in form_valid)
    without LoginRequiredMixin — AnonymousUser passed into a FK filter/lookup
    crashes with TypeError the moment an anonymous visitor loads the page."""
    errors = []
    for file_path, content in all_files.items():
        if not file_path.endswith("views.py") or not content:
            continue

        uses_request_user = bool(re.search(r'self\.request\.user', content))
        if not uses_request_user:
            continue

        view_classes = re.finditer(
            r'class\s+(\w+)\s*\(([^)]*)\)\s*:(.*?)(?=\nclass\s|\Z)',
            content, re.DOTALL
        )
        for match in view_classes:
            view_name, bases, body = match.group(1), match.group(2), match.group(3)
            if 'self.request.user' not in body:
                continue
            if 'LoginRequiredMixin' not in bases:
                errors.append(
                    f"❌ {view_name} in {file_path} uses self.request.user but doesn't inherit "
                    f"LoginRequiredMixin — this crashes with TypeError for anonymous visitors. "
                    f"Add: class {view_name}(LoginRequiredMixin, ...)"
                )
    return errors
    

def build_base_urls_py():
    return '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''


def normalize_module_refs(content, project_name):
    """Force any hardcoded project-module references in AI-generated
    settings.py / urls.py to match the actual folder name on disk."""
    if not content:
        return content
    # Replace ROOT_URLCONF = "xxx.urls" -> correct project_name
    content = re.sub(
        r"(ROOT_URLCONF\s*=\s*)['\"][\w.]+\.urls['\"]",
        rf"\1'{project_name}.urls'",
        content,
    )
    # Replace WSGI_APPLICATION = "xxx.wsgi.application"
    content = re.sub(
        r"(WSGI_APPLICATION\s*=\s*)['\"][\w.]+\.wsgi\.application['\"]",
        rf"\1'{project_name}.wsgi.application'",
        content,
    )
    # Replace ASGI_APPLICATION similarly, if present
    content = re.sub(
        r"(ASGI_APPLICATION\s*=\s*)['\"][\w.]+\.asgi\.application['\"]",
        rf"\1'{project_name}.asgi.application'",
        content,
    )
    return content

 
@login_required
@require_http_methods(["GET"])
def project_state(request, project_id):
    """Return complete project state for AI analysis"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    files = File.objects.filter(project=project)
    
    state = {
        "file_count": files.count(),
        "apps": [],
        "models": [],
        "views": [],
        "urls": [],
        "templates": [],
        "settings": {},
        "file_map": {}
    }
    
    for f in files:
        state["file_map"][f.name] = {
            "id": f.id,
            "size": len(f.content or ""),
            "extension": f.extension()
        }
        
        # Extract app names from folder structure
        parts = f.name.split("/")
        if len(parts) >= 1 and parts[0] not in ['manage.py', 'requirements.txt']:
            if parts[0] not in state["apps"] and not parts[0].startswith('.'):
                state["apps"].append(parts[0])
        
        # Parse models
        if f.name.endswith("models.py") and f.content:
            from django.apps import apps
            model_matches = re.findall(r'class\s+(\w+)\s*\(\s*models\.Model\s*\)', f.content)
            state["models"].extend(model_matches)
        
        # Parse views
        if f.name.endswith("views.py") and f.content:
            view_matches = re.findall(r'def\s+(\w+)\s*\(', f.content)
            state["views"].extend(view_matches)
        
        # Parse URLs
        if f.name.endswith("urls.py") and f.content:
            url_matches = re.findall(r"path\(\s*['\"]([^'\"]+)['\"]", f.content)
            state["urls"].extend(url_matches)
        
        # Track templates
        if "/templates/" in f.name:
            state["templates"].append(f.name)
    
    return JsonResponse(state)



@login_required
def project_status(request, project_id):
    """Check if server is running WITHOUT triggering a rebuild"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    export_dir = Path(settings.BASE_DIR) / "generated_projects" / str(project.id)
    
    live_info = get_live_server_info(export_dir)
    
    if live_info:
        return JsonResponse({
            "status": "success",
            "running": True,
            "preview_url": f"http://{get_public_host()}:{live_info['port']}/",
            "admin_url": f"http://{get_public_host()}:{live_info['port']}/admin/",
            # "preview_url": f"http://127.0.0.1:{live_info['port']}/",
            # "admin_url": f"http://127.0.0.1:{live_info['port']}/admin/",
            "port": live_info['port'],
            "admin_password": live_info.get('admin_password', ''),
        })
    
    return JsonResponse({"status": "success", "running": False})



def _load_ai_rules():
    """Load AI rule files: the explicit list below first (in this exact
    order), then auto-append any other NN_name.md file found in ai_rules/
    that isn't already listed — so a new rule file (12_*.md, 13_*.md, ...)
    is picked up automatically on the next build, no code edit required."""
    rules_dir = Path(settings.BASE_DIR) / "ai_rules"

    rule_files = [
        "01_workflow.md",
        "02_application_types.md",
        "03_django_architecture.md",
        "04_dependency_rules.md",
        "05_validation.md",
        "06_project_intelligence.md",
        "07_code_generation.md",
        "08_requirements_analysis.md",
        "09_skill_templates.md",
        "10_ui_architecture.md",
        "11_ui_patterns.md",
       
    ]

    combined = []

    for filename in rule_files:
        filepath = rules_dir / filename
        if filepath.exists():
            combined.append(filepath.read_text(encoding="utf-8"))
        else:
            print(f"⚠️ Missing rule file: {filepath}")

    # Auto-pick-up: any NN_name.md file in the folder not already listed above
    if rules_dir.exists():
        known = set(rule_files)
        extra_files = sorted(
            f for f in rules_dir.glob("[0-9][0-9]_*.md")
            if f.name not in known
        )
        for filepath in extra_files:
            combined.append(filepath.read_text(encoding="utf-8"))
            print(f"📄 Auto-loaded new rule file: {filepath.name}")

    return "\n\n".join(combined)


def get_public_host():
    """Returns the host to use in preview/admin URLs shown to the user.
    Locally this is 127.0.0.1 (browser and server are the same machine).
    On a real server, set PUBLIC_HOST in .env to the domain or public IP
    so generated preview links are actually reachable."""
    return os.environ.get("PUBLIC_HOST", "127.0.0.1")


@login_required
@require_http_methods(["POST"])
def ai_build_project(request, project_id):
    """
    AI Build Project - handles BOTH:
    1. Full scaffold generation for new/fresh projects
    2. Incremental updates to existing projects (full-stack aware)
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)

    try:
        data = json.loads(request.body.decode()) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    prompt = data.get("prompt", "").strip()
    apply_now = data.get("apply", False)
    
    if not prompt and not apply_now:
        return JsonResponse({"status": "error", "message": "Please enter a prompt"}, status=400)

    if client is None:
        return JsonResponse({"status": "error", "message": "🔑 OpenAI API is not configured."}, status=500)

    # ─────────────────────────────────────────────────────────────
    # DETECT: Is this a new project or an existing one?
    # ─────────────────────────────────────────────────────────────
    existing_files = File.objects.filter(project=project)
    existing_file_count = existing_files.count()
    
    # Consider "existing" if there's a Django project structure already
    has_settings = existing_files.filter(name__regex=r'^[^/]+/settings\.py$').exists()
    has_models = existing_files.filter(name__regex=r'^[^/]+/models\.py$').exists()
    has_views = existing_files.filter(name__regex=r'^[^/]+/views\.py$').exists()
    
    is_existing_project = has_settings and (has_models or has_views) and existing_file_count > 5
    
    print(f"🔍 Project state: {existing_file_count} files, settings={has_settings}, models={has_models}, views={has_views}")
    print(f"🔍 is_existing_project={is_existing_project}, apply_now={apply_now}")

    # ─────────────────────────────────────────────────────────────
    # PATH A: APPLY PENDING INCREMENTAL CHANGES
    # ─────────────────────────────────────────────────────────────
    if apply_now and data.get("changes"):
        return _apply_incremental_changes(project, data)

    # ─────────────────────────────────────────────────────────────
    # PATH B: INCREMENTAL UPDATE (existing project)
    # ─────────────────────────────────────────────────────────────
    if is_existing_project:
        return _incremental_build(project, prompt, existing_files)

    # ─────────────────────────────────────────────────────────────
    # PATH C: FULL SCAFFOLD (new/fresh project) - Original logic
    # ─────────────────────────────────────────────────────────────
    return _scaffold_build(project, prompt)


# ═════════════════════════════════════════════════════════════════
# HELPER: Incremental Build (existing project)
# ═════════════════════════════════════════════════════════════════
def _incremental_build(project, prompt, existing_files):
    """
    Handle updates to an existing Django project.
    AI thinks like a senior architect before proposing changes.
    Follows the 10-step thinking framework.
    """
    try:
        # Build comprehensive project context
        project_context = get_existing_project_context(project)
        file_map = {}
        
        for f in existing_files:
            content = f.content or ""
            # Include full content for small files, truncated for large ones
            if len(content) > 2000:
                content = content[:800] + "\n\n... (truncated) ...\n\n" + content[-800:]
            
            file_map[f.name] = {
                "id": f.id,
                "content": content,
                "size": len(f.content or ""),
                "extension": f.extension()
            }
        
        # Detect existing project structure
        settings_file = existing_files.filter(name__regex=r'^[^/]+/settings\.py$').first()
        project_name = "project"
        if settings_file:
            parts = settings_file.name.split("/")
            project_name = parts[0] if len(parts) >= 1 else "project"
        
        # ── THE ARCHITECT SYSTEM PROMPT FOR INCREMENTAL UPDATES ──

        # ── Load AI rules from modular files ──
        system_prompt = _load_ai_rules()
        system_prompt += """

⚠️ INCREMENTAL MODE: You are MODIFYING an existing project. Return ONLY the changes format:
{
    "analysis": "Brief summary",
    "changes": [{"file_path": "...", "action": "create|update|delete", "content": "...", "reason": "..."}],
    "requires_migration": true/false,
    "requires_server_restart": true/false
}
Do NOT return the scaffold format (app_name, models_py, views_py, etc.). Only return the CHANGES that need to be applied.
"""
        system_prompt += f"""

═══ CURRENT PROJECT STATE ═══

Project name: {project_name}
Total files: {len(file_map)}
Apps: {project_context['existing_apps']}
Models: {project_context['existing_models']}
URL namespaces: {project_context['existing_url_namespaces']}
Templates: {project_context['existing_templates']}
Has working login (accounts/ URLs + login template): {project_context.get('has_auth_urls', False) and project_context.get('has_login_template', False)}
Has signup template: {project_context.get('has_signup_template', False)}

COMPLETE FILE MAP (with content):
{json.dumps(file_map, indent=2, default=str, ensure_ascii=False)}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Request: {prompt}"}
            ],
            temperature=0.2,
            max_tokens=16000,
            response_format={"type": "json_object"}
        )

        choice = response.choices[0]
        raw_text = choice.message.content
        print(f"✅ Incremental AI response: {len(raw_text)} chars, finish_reason={choice.finish_reason}")
        print(f"🔍 First 500 chars of response: {raw_text[:500]}")

        if choice.finish_reason == "length":
            return JsonResponse({
                "status": "error",
                "message": (
                    "The AI's response was too large and got cut off before finishing. "
                    "Try asking for fewer changes at once, or a more focused request."
                ),
                "detail": "finish_reason=length",
            }, status=500)

        try:
            result = json.loads(raw_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            if start == -1 or end <= start:
                return JsonResponse({
                    "status": "error",
                    "message": "No valid JSON in AI response. Try again.",
                }, status=500)
            try:
                result = json.loads(raw_text[start:end])
            except json.JSONDecodeError:
                fixed = raw_text[start:end]
                fixed += '}' * (fixed.count('{') - fixed.count('}'))
                try:
                    result = json.loads(fixed)
                    print("🔧 Repaired JSON with missing closing braces")
                except json.JSONDecodeError as e2:
                    return JsonResponse({
                        "status": "error",
                        "message": "Invalid JSON from AI. Try again with a simpler request.",
                        "detail": str(e2)[:200],
                    }, status=500)
                
   
        # Validate the response
        if not result.get("changes"):
            return JsonResponse({
                "status": "error",
                "message": "AI did not propose any changes"
            }, status=500)

        # Repair known failure patterns (template path mismatches,
        # f-string syntax errors) before these changes are shown to
        # the user or applied to disk.
        result["changes"], repair_warnings = validate_and_repair_changes(result["changes"])
        if repair_warnings:
            print(f"⚠️ Change validation warnings: {repair_warnings}")

        
        # Extract thinking process
        thinking = result.get("thinking", {})
        print(f"🧠 AI Thinking:")
        print(f"   Understanding: {thinking.get('understanding', 'N/A')[:100]}")
        print(f"   Impact: {thinking.get('impact_analysis', 'N/A')[:100]}")
        print(f"   Solution: {thinking.get('solution_design', 'N/A')[:100]}")
        print(f"   DB Changes: {thinking.get('database_changes', 'N/A')}")
        print(f"   Page Changes: {thinking.get('page_changes', 'N/A')}")
        print(f"   Suggested: {thinking.get('suggested_improvements', [])}")
        print(f"✅ Incremental analysis: {len(result['changes'])} changes proposed")
        
        return JsonResponse({
            "status": "success",
            "build_type": "incremental",
            "message": f"✅ Analysis complete — {len(result['changes'])} changes proposed",
            "thinking": thinking,
            "analysis": result.get("analysis", ""),
            "changes": result["changes"],
            "requires_migration": result.get("requires_migration", False),
            "requires_server_restart": result.get("requires_server_restart", False),
            "validation_warnings": repair_warnings,
        })
        
    except Exception as e:
        print(f"❌ Incremental build error: {traceback.format_exc()}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    

def _export_project_files(project, export_dir):
    """Export all project files to disk, injecting persistent DB path into settings.py"""
    export_dir.mkdir(parents=True, exist_ok=True)
    
    persistent_db_dir = Path(settings.BASE_DIR) / "project_databases"
    persistent_db_dir.mkdir(parents=True, exist_ok=True)
    persistent_db_path = persistent_db_dir / f"project_{project.id}.sqlite3"
    
    for f in File.objects.filter(project=project):
        full_path = export_dir / f.name
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = f.content or ""
        
        if f.name.endswith("/settings.py"):
            db_path_str = str(persistent_db_path).replace("\\", "/")
            content = content.replace(
                "os.environ.get('DB_PATH', str(BASE_DIR / 'db.sqlite3'))",
                f"os.environ.get('DB_PATH', '{db_path_str}')"
            )
            content = content.replace(
                "str(BASE_DIR / 'db.sqlite3')",
                f"'{db_path_str}'"
            )
            content = content.replace(
                "'NAME': BASE_DIR / 'db.sqlite3'",
                f"'NAME': '{db_path_str}'"
            )
        
        full_path.write_text(content, encoding="utf-8")
    
    print(f"✅ Exported {File.objects.filter(project=project).count()} files to {export_dir}")


# ═════════════════════════════════════════════════════════════════
# ENTRY POINT — call this from ai_build_project's apply_now branch
# ═════════════════════════════════════════════════════════════════

MAX_RETRIES = 2

def _apply_incremental_changes(project, data):
    prompt = data.get("prompt", "").strip()
    changes = data.get("changes", [])
    requires_migration = data.get("requires_migration", False)
    requires_server_restart = data.get("requires_server_restart", False)

    if not changes:
        return JsonResponse({"status": "error", "message": "No changes to apply"}, status=400)

    attempt = 0
    retry_log = []

    while True:
        attempt += 1
        print(f"🔍 Applying {len(changes)} changes: {[c.get('file_path') for c in changes]}")
        print(f"🔍 requires_migration={requires_migration}, requires_server_restart={requires_server_restart}")
        try:
            result = _attempt_apply(
                project, changes, requires_migration, requires_server_restart
            )
        except Exception as e:
            print(f"❌ _attempt_apply crashed: {traceback.format_exc()}")
            return JsonResponse({
                "status": "error",
                "message": f"Apply failed with an unexpected error: {e}",
                "retry_log": retry_log,
            }, status=500)

        if result["ok"]:
            response = result["payload"]
            if retry_log:
                response["auto_fixed_after_retries"] = retry_log
            return JsonResponse(response)

        # Failed. Can we retry?
        failure_summary = result["failure_summary"]
        retry_log.append({"attempt": attempt, "reason": failure_summary})

        if attempt > MAX_RETRIES or not prompt:
            print(f"❌ APPLY FAILED — retry_log: {json.dumps(retry_log, indent=2)}")
            return JsonResponse({
                "status": "error",
                "message": (
                    f"Failed after {attempt} attempt(s)."
                    if prompt else
                    "Failed and no 'prompt' was provided, so it could not be auto-retried."
                ),
                "validation_errors": result.get("validation_errors"),
                "smoke_test_errors": result.get("smoke_test_errors"),
                "retry_log": retry_log,
            }, status=400 if result.get("validation_errors") else 500)

        # Regenerate changes from the AI using the real failure as context
        existing_files = File.objects.filter(project=project)
        regenerated = _generate_ai_changes(
            project, prompt, existing_files,
            retry_context=[failure_summary],
            previous_changes=changes,
        )
        
        print(f"🔍 regenerated type: {type(regenerated)}")
        if isinstance(regenerated, dict):
            print(f"🔍 regenerated keys: {list(regenerated.keys())}")
            print(f"🔍 regenerated changes count: {len(regenerated.get('changes', []))}")
        else:
            print(f"🔍 regenerated is NOT a dict: {regenerated}")
        
        if not regenerated or not regenerated.get("changes"):
            return JsonResponse({
                "status": "error",
                "message": "Retry attempt did not produce usable changes.",
                "retry_log": retry_log,
            }, status=500)

        changes = regenerated["changes"]
        requires_migration = regenerated.get("requires_migration", requires_migration)
        requires_server_restart = regenerated.get("requires_server_restart", requires_server_restart)
        print(f"🔍 Regenerated {len(changes)} changes: {[c.get('file_path') for c in changes]}")
        # loop and try again

# ═════════════════════════════════════════════════════════════════
# ONE FULL ATTEMPT: validate -> save -> stage -> check -> promote -> smoke test
# ═════════════════════════════════════════════════════════════════
def _attempt_apply(project, changes, requires_migration, requires_server_restart):
    applied = []
    errors = []
    has_model_changes = False
    has_python_changes = False

    files_before = {f.name: (f.content or "") for f in File.objects.filter(project=project)}
    all_files = dict(files_before)
    for change in changes:
        if change.get("action") in ("create", "update"):
            all_files[change["file_path"]] = change.get("content", "")


    # Auto-fix: Add list_select_related to admin classes missing it (incremental path)
    for file_path, content in all_files.items():
        if file_path.endswith("admin.py") and content:
            models_path = file_path.replace("admin.py", "models.py")
            models_content = all_files.get(models_path, "")
            if models_content:
                fk_map = _extract_fk_fields_per_model(models_content)
                for model_name, fk_fields in fk_map.items():
                    if not fk_fields:
                        continue
                    pattern = rf'(@admin\.register\({model_name}\).*?class\s+\w+Admin\([^)]+\).*?)(?=\n@admin\.register|\nclass\s|\Z)'
                    match = re.search(pattern, content, re.DOTALL)
                    if match and 'list_select_related' not in match.group(1):
                        replacement = match.group(1).replace(
                            'list_per_page = 25',
                            f'list_per_page = 25\n    list_select_related = {tuple(sorted(fk_fields))}'
                        )
                        content = content.replace(match.group(1), replacement)
                        all_files[file_path] = content
                        # Also update the actual change content
                        for change in changes:
                            if change.get("file_path") == file_path:
                                change["content"] = content
                        print(f"🔧 [incremental] Auto-added list_select_related for {model_name}Admin: {sorted(fk_fields)}")

    validation_errors = _run_static_validation(changes, files_before, all_files)
    if validation_errors:
        return {
            "ok": False,
            "failure_summary": "Static validation errors:\n" + "\n".join(validation_errors),
            "validation_errors": validation_errors,
        }

    # ── Save to DB ──
    with transaction.atomic():
        for change in changes:
            try:
                file_path = change.get("file_path", "").strip()
                action = change.get("action", "").strip()
                content = change.get("content", "")

                if not file_path or not action:
                    errors.append({"file": file_path or "unknown", "error": "Missing file_path or action"})
                    continue

                if action == "create":
                    existing = File.objects.filter(project=project, name=file_path).first()
                    if existing:
                        errors.append({"file": file_path, "error": "File already exists — use update instead"})
                    else:
                        File.objects.create(project=project, name=file_path, content=content)
                        applied.append({"file": file_path, "action": "created"})
                        if file_path.endswith("models.py"):
                            has_model_changes = True
                        if file_path.endswith(".py"):
                            has_python_changes = True

                elif action == "update":
                    file = File.objects.filter(project=project, name=file_path).first()
                    if file:
                        file.content = content
                        file.save(update_fields=["content"])
                        applied.append({"file": file_path, "action": "updated"})
                    else:
                        File.objects.create(project=project, name=file_path, content=content)
                        applied.append({"file": file_path, "action": "created (was update)"})
                    if file_path.endswith("models.py"):
                        has_model_changes = True
                    if file_path.endswith(".py"):
                        has_python_changes = True

                elif action == "delete":
                    deleted_count, _ = File.objects.filter(project=project, name=file_path).delete()
                    if deleted_count > 0:
                        applied.append({"file": file_path, "action": "deleted"})
                    else:
                        errors.append({"file": file_path, "error": "File not found"})
                else:
                    errors.append({"file": file_path, "error": f"Unknown action: {action}"})
            except Exception as e:
                errors.append({"file": file_path, "error": str(e)})

    export_dir = Path(settings.BASE_DIR) / "generated_projects" / str(project.id)
    staging_dir = Path(settings.BASE_DIR) / "generated_projects" / f"{project.id}_staging"
    backup_dir = Path(settings.BASE_DIR) / "generated_projects" / f"{project.id}_prev"
    persistent_db_dir = Path(settings.BASE_DIR) / "project_databases"
    persistent_db_dir.mkdir(parents=True, exist_ok=True)
    persistent_db_path = persistent_db_dir / f"project_{project.id}.sqlite3"
    export_db_path = export_dir / "db.sqlite3"

    # ── Export to staging, run manage.py check ──
    if staging_dir.exists():
        shutil.rmtree(staging_dir, ignore_errors=True)
    try:
        _export_project_files(project, staging_dir)
    except Exception as e:
        shutil.rmtree(staging_dir, ignore_errors=True)
        return {"ok": False, "failure_summary": f"Staging export failed: {e}"}

    settings_file = File.objects.filter(project=project, name__endswith="/settings.py").first()
    project_name = settings_file.name.split("/")[0] if settings_file else None

    if project_name:
        env = build_subprocess_env(staging_dir, project_name, project.id)
        check_result = subprocess.run(
            [sys.executable, "manage.py", "check"],
            cwd=staging_dir, capture_output=True, text=True, env=env,
        )
        if check_result.returncode != 0:
            full_error = (check_result.stderr + "\n" + check_result.stdout).strip()
            print(f"❌ DJANGO CHECK FAILED:\n{full_error}")
            # Don't delete staging so we can debug
            # shutil.rmtree(staging_dir, ignore_errors=True)
            return {
                "ok": False,
                "failure_summary": f"Django system check failed:\n{full_error[-3000:]}",
                "validation_errors": [full_error[-3000:]],
            }

    # ── DB backup (only if models unchanged) ──

    db_backup = None
    for db_path in [persistent_db_path, export_db_path]:
        if db_path.exists() and db_path.stat().st_size > 0:
            try:
                # WAL mode keeps recent writes in a separate -wal file that
                # is NOT part of the main .sqlite3 file's bytes. Force a
                # checkpoint to flush everything into the main file BEFORE
                # backing it up — otherwise this backup silently misses any
                # writes that haven't been checkpointed yet, and later
                # deleting the -wal file (below) permanently discards them.
                try:
                    conn = sqlite3.connect(str(db_path))
                    conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
                    conn.close()
                except Exception as e:
                    print(f"⚠️ WAL checkpoint before backup failed: {e}")

                db_backup = db_path.read_bytes()
                break
            except Exception:
                pass

    # ALWAYS kill any running server before renaming export_dir, regardless
    # of change type — the rename below happens unconditionally, so any
    # live server holding files open in export_dir (from this apply or an
    # earlier "Run Project" click) will block it, template-only change or not.
    kill_previous_server(export_dir, project.id)
    for _ in range(10):
        if project.id not in _running_servers or _running_servers[project.id].poll() is not None:
            break
        time.sleep(0.5)
    time.sleep(1)  # small extra buffer for Windows handle release even after process exit


    # ── Promote: keep old live dir as backup instead of deleting it ──
    if backup_dir.exists():
        shutil.rmtree(backup_dir, ignore_errors=True)
    if export_dir.exists():
        _safe_rename(export_dir, backup_dir)
    _safe_rename(staging_dir, export_dir)

    if db_backup:
        try:
            persistent_db_path.write_bytes(db_backup)
            for suffix in ("-wal", "-shm", "-journal"):
                stale = persistent_db_dir / f"project_{project.id}.sqlite3{suffix}"
                if stale.exists():
                    try:
                        stale.unlink()
                    except OSError:
                        pass
        except Exception:
            pass

    # ── Migrations ──
    migration_result = None
    apps_with_model_changes = {
        c["file_path"].split("/")[0] for c in changes
        if c.get("file_path", "").endswith("models.py")
    }
    

    if (has_model_changes or requires_migration) and apps_with_model_changes and project_name:
        migration_result = _run_migrations(
            export_dir, project, project_name, apps_with_model_changes,
            persistent_db_path, export_db_path,
        )
        if migration_result and migration_result.startswith("Migration error"):
            _rollback_promotion(export_dir, backup_dir, staging_dir)
            return {"ok": False, "failure_summary": migration_result}

        # Persist the newly-generated migration file(s) so they survive
        # the next rebuild-from-DB cycle instead of being silently lost.
        _sync_migration_files_to_db(project, export_dir, apps_with_model_changes)

    # ── SMOKE TEST: actually request the new/changed URLs ──
    smoke_errors = []
    if project_name:
        smoke_errors = _run_smoke_test(export_dir, project_name, project.id, changes)

    if smoke_errors:
        _rollback_promotion(export_dir, backup_dir, staging_dir)
        return {
            "ok": False,
            "failure_summary": "Runtime errors when actually loading the changed pages:\n" + "\n".join(smoke_errors),
            "smoke_test_errors": smoke_errors,
        }

    # ── Success: drop the backup, we're committed ──
    shutil.rmtree(backup_dir, ignore_errors=True)

    # ── Restart server ──
    restart_result = None
    if (has_python_changes or requires_server_restart) and project_name:
        restart_result = _restart_server(export_dir, project, project_name)

    return {
        "ok": True,
        "payload": {
            "status": "success" if not errors else "partial",
            "build_type": "incremental",
            "applied": applied,
            "errors": errors,
            "migration_result": migration_result,
            "restart_result": restart_result,
        },
    }


def _rollback_promotion(export_dir, backup_dir, staging_dir):
    """Restore the previous working live directory after a failed smoke test / migration."""
    shutil.rmtree(export_dir, ignore_errors=True)
    if backup_dir.exists():
        _safe_rename(backup_dir, export_dir)
    shutil.rmtree(staging_dir, ignore_errors=True)


def _extract_fk_fields_per_model(models_content):
    """Returns {model_name: {field_name, ...}} for every ForeignKey/OneToOneField
    declared on each model in a models.py file's content."""
    result = {}
    if not models_content:
        return result

    class_blocks = re.finditer(
        r'class\s+(\w+)\s*\(\s*models\.Model\s*\)\s*:(.*?)(?=\nclass\s|\Z)',
        models_content, re.DOTALL
    )
    for match in class_blocks:
        model_name, body = match.group(1), match.group(2)
        fk_fields = set(re.findall(
            r'(\w+)\s*=\s*models\.(?:ForeignKey|OneToOneField)\(',
            body
        ))
        result[model_name] = fk_fields
    return result

def _check_admin_list_select_related(all_files):
    """Blocks if any ModelAdmin shows a real ForeignKey field in list_display
    or list_filter without also listing it in list_select_related — that
    combination causes N+1 queries and slow admin list pages (this is the
    exact bug that made Products/Stock/Sale admin slow before it was fixed)."""
    errors = []

    for models_path, models_content in all_files.items():
        if not models_path.endswith("models.py") or not models_content:
            continue
        fk_map = _extract_fk_fields_per_model(models_content)
        if not fk_map:
            continue

        parts = models_path.split("/")
        admin_path = "/".join(parts[:-1]) + "/admin.py" if len(parts) > 1 else "admin.py"
        admin_content = all_files.get(admin_path, "")
        if not admin_content:
            continue

        admin_classes = re.finditer(
            r'@admin\.register\((\w+)\)\s*\nclass\s+(\w+)\s*\([^)]*\)\s*:(.*?)(?=\n@admin\.register|\nclass\s|\Z)',
            admin_content, re.DOTALL
        )
        for match in admin_classes:
            model_name, admin_class_name, body = match.group(1), match.group(2), match.group(3)
            fk_fields = fk_map.get(model_name)
            if not fk_fields:
                continue

            def _extract_tuple(field_name, text):
                m = re.search(rf'{field_name}\s*=\s*\(([^)]*)\)', text)
                if not m:
                    return set()
                return {f.strip().strip("'\"") for f in m.group(1).split(',') if f.strip()}

            shown_fields = _extract_tuple('list_display', body) | _extract_tuple('list_filter', body)
            select_related_fields = _extract_tuple('list_select_related', body)

            fk_shown = shown_fields & fk_fields
            missing = fk_shown - select_related_fields
            if missing:
                errors.append(
                    f"❌ {admin_class_name} in {admin_path} shows ForeignKey field(s) "
                    f"{sorted(missing)} in list_display/list_filter without list_select_related "
                    f"— this causes N+1 queries and slow admin pages. Add: "
                    f"list_select_related = {tuple(sorted(fk_shown))}"
                )
    return errors


def _check_views_select_related(all_files):
    """
    Blocks if a view's template accesses ForeignKey fields (e.g. {{ obj.category.name }})
    but the view's get_queryset() doesn't use .select_related('category').
    Cross-checks against the actual model definition so ImageField/FileField
    attribute access (e.g. {{ obj.photo.url }}) is never mistaken for a
    ForeignKey relation.
    """
    errors = []

    # Attributes commonly accessed on non-relational field types — accessing
    # these via dotted template syntax does NOT imply a ForeignKey.
    NON_RELATIONAL_ATTRS = {
        'url', 'name', 'size', 'path',           # File/ImageField
        'year', 'month', 'day', 'date', 'time',  # Date/DateTimeField
        'strftime',
    }

    template_content_map = {}
    for file_path, content in all_files.items():
        if file_path.endswith(".html") and content:
            template_content_map[file_path] = content

    # Build a map of app_name -> {field_name: is_fk} from every models.py,
    # so we can confirm a field is actually a relation before flagging it.
    model_fk_fields = {}  # app_name -> set of field names that are FK/O2O/M2M
    for file_path, content in all_files.items():
        if file_path.endswith("models.py") and content:
            app_name = file_path.split("/")[0]
            fk_fields = set(re.findall(
                r'(\w+)\s*=\s*models\.(?:ForeignKey|OneToOneField|ManyToManyField)\(',
                content
            ))
            model_fk_fields.setdefault(app_name, set()).update(fk_fields)

    for file_path, content in all_files.items():
        if not file_path.endswith("views.py") or not content:
            continue

        app_name = file_path.split("/")[0]
        known_fk_fields = model_fk_fields.get(app_name, set())

        template_names = set(re.findall(r"template_name\s*=\s*['\"]([^'\"]+)['\"]", content))
        template_names |= set(re.findall(r"render\([^,]+,\s*['\"]([^'\"]+)['\"]", content))

        real_fk_accesses = set()
        for tpl_name in template_names:
            for tpl_path, tpl_content in template_content_map.items():
                if tpl_path.endswith(tpl_name) or tpl_path.endswith(f"/{tpl_name}"):
                    for match in re.finditer(r'\{\{\s*\w+\.(\w+)\.(\w+)\s*\}\}', tpl_content):
                        field_name, accessed_attr = match.group(1), match.group(2)
                        # Only flag if the field is a CONFIRMED FK/O2O/M2M on
                        # this app's models AND the accessed attribute isn't
                        # a known non-relational field method/property.
                        if field_name in known_fk_fields and accessed_attr not in NON_RELATIONAL_ATTRS:
                            real_fk_accesses.add(field_name)

        if not real_fk_accesses:
            continue

        has_select_related = 'select_related(' in content
        has_prefetch_related = 'prefetch_related(' in content

        if not has_select_related and not has_prefetch_related:
            view_classes = re.findall(r'class\s+(\w+)\s*\([^)]*\)\s*:', content)
            for vc in view_classes:
                errors.append(
                    f"❌ {vc} in {file_path}: template accesses FK fields {sorted(real_fk_accesses)} "
                    f"but get_queryset() has no .select_related()/.prefetch_related() — N+1 query risk"
                )

    return errors


# ═════════════════════════════════════════════════════════════════
# STATIC VALIDATION
# ═════════════════════════════════════════════════════════════════
def _run_static_validation(changes, files_before, all_files):
    validation_errors = []

    for file_path, content in all_files.items():
        if file_path.endswith(".py") and content and content.strip():
            try:
                compile(content, file_path, "exec")
            except SyntaxError as e:
                validation_errors.append(f"❌ {file_path} line {e.lineno}: {e.msg}")

    for change in changes:
        if change.get("action") != "update":
            continue
        file_path = change.get("file_path", "")
        old_content = files_before.get(file_path, "")
        new_content = change.get("content", "")
        if len(old_content) > 500 and len(new_content) < len(old_content) * 0.6:
            validation_errors.append(
                f"⚠️ {file_path}: new content ({len(new_content)} chars) looks truncated "
                f"vs original ({len(old_content)} chars). Not applying."
            )
    
    # www
    for file_path, content in all_files.items():
        if file_path.endswith("views.py") and content:
            view_classes = re.findall(r'class\s+(\w+)\s*\(\s*(\w+)\s*\)', content)
            imports = set()
            for match in re.finditer(r'from\s+([\w.]+)\s+import\s+(.+?)(?:\n|$)', content):
                items = [i.strip() for i in match.group(2).replace('(', '').replace(')', '').split(',')]
                imports.update(items)
            required_parents = {'ListView', 'DetailView', 'CreateView', 'UpdateView',
                                 'DeleteView', 'TemplateView', 'FormView', 'View'}
            for class_name, parent in view_classes:
                if parent in required_parents and parent not in imports:
                    validation_errors.append(
                        f"❌ {file_path}: '{parent}' used by '{class_name}' but not imported."
                    )
            
            # Check every CBV has template_name explicitly set
            for match in re.finditer(r'class\s+(\w+)\s*\(\s*(\w+)\s*\)\s*:', content):
                class_name, parent = match.group(1), match.group(2)
                if parent in required_parents:
                    rest = content[match.end():]
                    next_class = re.search(r'\nclass\s+\w+\s*\(', rest)
                    class_body = rest[:next_class.start()] if next_class else rest
                    if 'template_name' not in class_body:
                        validation_errors.append(
                            f"❌ {class_name}({parent}) in {file_path} is missing template_name. "
                            f"Every class-based view MUST set template_name explicitly."
                        )

    for file_path, content in all_files.items():
        if file_path.endswith("urls.py") and content:
            views_used = set(re.findall(r'views\.(\w+)', content))
            if views_used:
                parts = file_path.split("/")
                views_path = "/".join(parts[:-1]) + "/views.py" if len(parts) > 1 else "views.py"
                views_content = all_files.get(views_path, "")
                for view_name in views_used:
                    if f'class {view_name}' not in views_content and f'def {view_name}' not in views_content:
                        validation_errors.append(
                            f"❌ {file_path} references views.{view_name}, not found in {views_path}"
                        )

    for file_path, content in all_files.items():
        if file_path.endswith("views.py") and content:
            models_used = set(re.findall(r'(\w+)\.objects\.', content))
            model_imports = set()
            for match in re.finditer(r'from\s+\.models\s+import\s+(.+?)(?:\n|$)', content):
                items = [i.strip() for i in match.group(1).replace('(', '').replace(')', '').split(',')]
                model_imports.update(items)
            for model in models_used:
                if model not in model_imports and model != 'User':
                    validation_errors.append(f"❌ {file_path}: Model '{model}' used but not imported")

    settings_content = next((c for p, c in all_files.items() if p.endswith("settings.py")), "")
    new_apps = {
        c["file_path"].split("/")[0] for c in changes
        if c.get("action") == "create" and c["file_path"].endswith("models.py")
    }
    for app in new_apps:
        if f"'{app}'" not in settings_content and f'"{app}"' not in settings_content:
            validation_errors.append(f"❌ App '{app}' not registered in INSTALLED_APPS")
   
    settings_file_path = next((p for p in all_files if p.endswith("/settings.py")), None)
    project_name = settings_file_path.split("/")[0] if settings_file_path else None
    root_urls_path = f"{project_name}/urls.py" if project_name else None
    root_urls_content = all_files.get(root_urls_path, "") if root_urls_path else ""

    for file_path in all_files:
        if file_path.endswith("urls.py") and file_path != root_urls_path:
            parts = file_path.split("/")
            app_name = parts[0] if len(parts) > 1 else None
            if not app_name:
                continue
            if (f"include('{app_name}.urls')" not in root_urls_content
                    and f'include("{app_name}.urls")' not in root_urls_content):
                validation_errors.append(f"❌ {file_path} not wired into root urls.py")

    for file_path, content in all_files.items():
        if file_path.endswith("views.py") and content:
            template_refs = set(re.findall(r'template_name\s*=\s*[\'"]([^\'"]+)[\'"]', content))
            template_refs |= set(re.findall(r'render\([^,]+,\s*[\'"]([^\'"]+)[\'"]', content))
            for tmpl in template_refs:
                if not any(p.endswith(tmpl) for p in all_files):
                    validation_errors.append(f"❌ {file_path} references missing template '{tmpl}'")

        # Built-in auth URLs that come from django.contrib.auth.urls (always available)
    BUILT_IN_AUTH_URLS = {'login', 'logout', 'password_change', 'password_change_done', 
                          'password_reset', 'password_reset_done', 'password_reset_confirm', 
                          'password_reset_complete'}
    
    url_names_defined = set()
    for file_path, content in all_files.items():
        if file_path.endswith("urls.py"):
            url_names_defined |= set(re.findall(r'name=[\'"](\w+)[\'"]', content))
    
    url_names_defined |= BUILT_IN_AUTH_URLS  # These come from django.contrib.auth.urls
    
    for file_path, content in all_files.items():
        if file_path.endswith(".html"):
            for name in re.findall(r"\{%\s*url\s+['\"](\w+)['\"]", content):
                if name not in url_names_defined:
                    validation_errors.append(f"❌ {file_path} calls {{% url '{name}' %}} — undefined name")

    # Admin registration check for new models
    # Admin registration check for new models (now blocking, not just a warning)
    for file_path, content in all_files.items():
        if file_path.endswith("models.py") and content:
            model_names = re.findall(r'class\s+(\w+)\s*\(\s*models\.Model\s*\)', content)
            if not model_names:
                continue
            parts = file_path.split("/")
            admin_path = "/".join(parts[:-1]) + "/admin.py" if len(parts) > 1 else "admin.py"
            admin_content = all_files.get(admin_path, "")
            for model_name in model_names:
                registered = (
                    f"register({model_name})" in admin_content
                    or f"register([{model_name}" in admin_content
                    or f", {model_name})" in admin_content
                    or re.search(rf'@admin\.register\({model_name}\)', admin_content)
                )
                if not registered:
                    validation_errors.append(
                        f"❌ Model '{model_name}' in {file_path} isn't registered in {admin_path} "
                        f"— add @admin.register({model_name}) with list_display, list_filter, search_fields"
                    )
                    continue

                has_export_mixin_defined = "class ExportAdminMixin" in admin_content
                if not has_export_mixin_defined:
                    validation_errors.append(
                        f"❌ {admin_path} is missing the ExportAdminMixin class (csv + docx export actions) "
                        f"— define it once at the top of the file"
                    )

                # Registered — but is it a real config, or a bare/lazy registration?
                admin_class_match = re.search(
                    rf'@admin\.register\({model_name}\)\s*\nclass\s+(\w+)\s*\(([^)]*)\)',
                    admin_content
                )
                if admin_class_match:
                    admin_class_name = admin_class_match.group(1)
                    base_classes = admin_class_match.group(2)
                    class_start = admin_content.find(f'class {admin_class_name}')
                    class_body = admin_content[class_start:class_start + 1500]

                    if "ExportAdminMixin" not in base_classes:
                        validation_errors.append(
                            f"❌ {admin_class_name} in {admin_path} doesn't inherit ExportAdminMixin — "
                            f"change to: class {admin_class_name}(ExportAdminMixin, admin.ModelAdmin)"
                        )

                    has_list_display = 'list_display' in class_body
                    if not has_list_display:
                        validation_errors.append(
                            f"⚠️ {model_name}'s admin config in {admin_path} has no list_display — "
                            f"add 3-5 useful fields so the list view isn't just default __str__"
                        )
                elif f"admin.site.register({model_name})" in admin_content:
                    validation_errors.append(
                        f"⚠️ Model '{model_name}' is registered with admin.site.register({model_name}) "
                        f"and no ModelAdmin class — use @admin.register({model_name}) with ExportAdminMixin, "
                        f"list_display, list_filter, and search_fields instead"
                    )


    validation_errors.extend(_check_admin_list_select_related(all_files))
    # Views select_related check — warning only, doesn't block build
    select_related_warnings = _check_views_select_related(all_files)
    if select_related_warnings:
        for w in select_related_warnings:
            print(f"⚠️ {w}")
   # Only check LoginRequiredMixin if the project has auth URLs set up
    root_urls = all_files.get(f"{project_name}/urls.py", "") if project_name else ""
    has_auth = 'accounts/' in root_urls
    if has_auth:
        validation_errors.extend(_check_login_required_on_user_filtered_views(all_files))

   

    return validation_errors


def _check_new_models_have_full_wiring(files_before, all_files):
    """For every model class that's newly added (didn't exist in files_before),
    require: at least one view referencing it, that view wired into urls.py,
    and (transitively, via the existing template-existence check) a template."""
    errors = []
    model_class_re = re.compile(r'class\s+(\w+)\s*\(\s*models\.Model\s*\)')

    for file_path, new_content in all_files.items():
        if not file_path.endswith("models.py") or not new_content:
            continue
        old_content = files_before.get(file_path, "")
        old_models = set(model_class_re.findall(old_content))
        new_models = set(model_class_re.findall(new_content))
        added_models = new_models - old_models
        if not added_models:
            continue

        parts = file_path.split("/")
        app_dir = "/".join(parts[:-1]) if len(parts) > 1 else ""
        views_path = f"{app_dir}/views.py" if app_dir else "views.py"
        urls_path = f"{app_dir}/urls.py" if app_dir else "urls.py"
        views_content = all_files.get(views_path, "")
        urls_content = all_files.get(urls_path, "")

        for model_name in added_models:
            has_view_ref = (
                bool(re.search(rf'\bmodel\s*=\s*{model_name}\b', views_content))
                or bool(re.search(rf'\b{model_name}\.objects\b', views_content))
            )
            if not has_view_ref:
                errors.append(
                    f"❌ New model '{model_name}' has no view in {views_path} — "
                    f"add at least a ListView and DetailView for it (e.g. `model = {model_name}`)"
                )
                continue

            view_names = re.findall(rf'class\s+(\w*{model_name}\w*View)\s*\(', views_content)
            wired = any(f'views.{vn}' in urls_content for vn in view_names)
            if not wired:
                errors.append(
                    f"❌ New model '{model_name}' has a view but it's not wired into {urls_path} "
                    f"— add a path() entry with a name= for it"
                )
    return errors


# ═════════════════════════════════════════════════════════════════
# SMOKE TEST — actually request the changed URLs, catch real tracebacks
# ═════════════════════════════════════════════════════════════════
_SMOKE_TEST_SCRIPT = '''
import os, sys, json, traceback
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")
import django
django.setup()
from django.test import Client
from django.urls import reverse, NoReverseMatch

names = {url_names!r}
results = []
c = Client()
for name in names:
    try:
        url = reverse(name)
    except NoReverseMatch:
        continue  # requires args, skip — can't smoke test without knowing valid pk/slug
    try:
        resp = c.get(url, follow=True)
        entry = {{"name": name, "url": url, "status": resp.status_code}}
        if resp.status_code >= 500:
            entry["error"] = "HTTP " + str(resp.status_code)
        results.append(entry)
    except Exception:
        results.append({{
            "name": name, "url": url, "status": None,
            "error": traceback.format_exc()[-1500:],
        }})

print("__SMOKE_TEST_RESULT__")
print(json.dumps(results))
'''


import json
from pathlib import Path

PROJECT_PORTS_FILE = Path("/var/www/codethinkers-staging/project_ports.json")

def update_project_port_mapping(project):
    """Write project subdomain → port mapping for the router."""
    import os
    if not os.environ.get('PRODUCTION'):
        return  # Only runs on production server
    
    mapping = {}
    if PROJECT_PORTS_FILE.exists():
        try:
            mapping = json.loads(PROJECT_PORTS_FILE.read_text())
        except json.JSONDecodeError:
            mapping = {}
    
    subdomain = project.subdomain or f"project-{project.id}"
    mapping[subdomain] = project.assigned_port
    
    PROJECT_PORTS_FILE.write_text(json.dumps(mapping))
    print(f"📝 Updated port mapping: {subdomain}.codethinkers.org → port {project.assigned_port}")



def _run_smoke_test(export_dir, project_name, project_id, changes):
    """Only tests parameterless named URLs from urls.py files touched by this change,
    so it can't test detail/edit views that need a real pk. Those still get the
    static + manage.py check coverage, just not live rendering."""
    url_names = set()
    for change in changes:
        fp = change.get("file_path", "")
        if fp.endswith("urls.py"):
            content = change.get("content", "")
            url_names |= set(re.findall(r'name=[\'"](\w+)[\'"]', content))

    if not url_names:
        return []

    script_path = export_dir / "_smoke_test_runner.py"
    script_path.write_text(
        _SMOKE_TEST_SCRIPT.format(project_name=project_name, url_names=sorted(url_names)),
        encoding="utf-8",
    )

    try:
        env = build_subprocess_env(export_dir, project_name, project_id)
        result = subprocess.run(
            [sys.executable, "_smoke_test_runner.py"],
            cwd=export_dir, capture_output=True, text=True, env=env, timeout=30,
        )
    except subprocess.TimeoutExpired:
        return ["⚠️ Smoke test timed out after 30s — one of the new pages may be hanging"]
    finally:
        try:
            script_path.unlink()
        except OSError:
            pass

    if "__SMOKE_TEST_RESULT__" not in result.stdout:
        # The script itself crashed (e.g. django.setup() failed) — that's a real failure too
        return [f"⚠️ Smoke test runner crashed:\n{(result.stderr or result.stdout)[-1500:]}"]

    json_part = result.stdout.split("__SMOKE_TEST_RESULT__")[-1].strip()
    try:
        results = json.loads(json_part)
    except json.JSONDecodeError:
        return [f"⚠️ Could not parse smoke test output:\n{json_part[-1000:]}"]

    errors = []
    for r in results:
        if r.get("error"):
            errors.append(f"❌ {r['name']} ({r.get('url', '?')}): {r['error']}")
    return errors


def _sync_migration_files_to_db(project, export_dir, apps_with_model_changes):
    """After makemigrations runs, the new migration file only exists on
    disk in export_dir — save it into the File table too, or the next
    _attempt_apply rebuild (which re-exports from File records) will
    silently lose it and regenerate 0001_initial from scratch forever."""
    for app_name in apps_with_model_changes:
        migrations_dir = Path(export_dir) / app_name / "migrations"
        if not migrations_dir.exists():
            continue
        for f in migrations_dir.glob("*.py"):
            if f.name == "__init__.py":
                continue
            file_path = f"{app_name}/migrations/{f.name}"
            File.objects.update_or_create(
                project=project,
                name=file_path,
                defaults={"content": f.read_text(encoding="utf-8")}
            )
            print(f"💾 Synced migration file to DB: {file_path}")


# ═════════════════════════════════════════════════════════════════
# MIGRATIONS
# ═════════════════════════════════════════════════════════════════
def _run_migrations(export_dir, project, project_name, apps_with_model_changes,
                     persistent_db_path, export_db_path):
    """Runs makemigrations/migrate for the changed apps. Uses real
    incremental migrations against the existing DB — does NOT delete
    migration history on every change, since that breaks the moment a
    model is genuinely altered (not just added), causing Django to try
    to re-create tables that already exist."""
    env = build_subprocess_env(export_dir, project_name, project.id)

    print(f"🔍 _run_migrations DB_PATH env: {env.get('DB_PATH')}")
    print(f"🔍 persistent_db_path: {persistent_db_path}")
    print(f"🔍 persistent_db_path exists: {persistent_db_path.exists()}")
    print(f"🔍 persistent_db_path size: {persistent_db_path.stat().st_size if persistent_db_path.exists() else 0}")

    try:
        db_is_fresh = not persistent_db_path.exists() or persistent_db_path.stat().st_size < 10000

        if db_is_fresh:
            # No real DB yet — safe to clear any stale migration files
            # and start clean, since there's nothing to preserve.
            for app_name in apps_with_model_changes:
                migrations_dir = Path(export_dir) / app_name / "migrations"
                if migrations_dir.exists():
                    for f in migrations_dir.glob("*.py"):
                        if f.name != "__init__.py":
                            f.unlink()
                    pycache = migrations_dir / "__pycache__"
                    if pycache.exists():
                        shutil.rmtree(pycache)
                print(f"🆕 Fresh DB — cleared any stale migration files for {app_name}")

        # Generate migrations against whatever migration history already
        # exists — incremental (0002_, 0003_, ...) for an existing DB,
        # or a fresh 0001_initial if we just cleared it above.
        makemigration_errors = []
        for app_name in apps_with_model_changes:
            mk = subprocess.run(
                [sys.executable, "manage.py", "makemigrations", app_name],
                cwd=export_dir, capture_output=True, text=True, env=env,
            )
            if mk.returncode != 0:
                makemigration_errors.append(f"{app_name}: {mk.stderr[:400]}")
            else:
                print(f"📝 makemigrations {app_name}: {mk.stdout[:300]}")

        if makemigration_errors:
            return "Migration error: " + " | ".join(makemigration_errors)

        # Regular migrate — safe in both cases now, since we never faked
        # or deleted history for an existing DB, so Django's own tracking
        # of what's applied stays accurate and consistent with real tables.
        migrate_all = subprocess.run(
            [sys.executable, "manage.py", "migrate"],
            cwd=export_dir, capture_output=True, text=True, env=env,
        )
        print(f"📝 Migrate stdout: {migrate_all.stdout[:300]}")
        if migrate_all.stderr:
            print(f"⚠️ Migrate stderr: {migrate_all.stderr[:300]}")

        admin_password = project.admin_password or secrets.token_urlsafe(12)
        if not project.admin_password:
            project.admin_password = admin_password
            project.save(update_fields=['admin_password'])

        subprocess.run(
            [sys.executable, "manage.py", "shell", "-c",
             f"from django.contrib.auth import get_user_model; User = get_user_model(); "
             f"User.objects.create_superuser('admin', 'admin@example.com', '{admin_password}') "
             f"if not User.objects.filter(username='admin').exists() else None"],
            cwd=export_dir, capture_output=True, text=True, env=env,
        )

        if migrate_all.returncode == 0:
            return f"Migrations applied for: {', '.join(apps_with_model_changes)}"
        return f"Migration error: {migrate_all.stderr[:800]}"
    except Exception as e:
        return f"Migration error: {str(e)}"


        
# ═════════════════════════════════════════════════════════════════
# SERVER RESTART
# ═════════════════════════════════════════════════════════════════
def _restart_server(export_dir, project, project_name):
    try:
        if project.assigned_port and is_port_free(project.assigned_port):
            use_port = project.assigned_port
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 0))
            use_port = sock.getsockname()[1]
            sock.close()
            project.assigned_port = use_port
            project.save(update_fields=['assigned_port'])

        env = build_subprocess_env(export_dir, project_name, project.id)
        proc = subprocess.Popen(
            [sys.executable, "manage.py", "runserver", "--noreload", str(use_port)],
            cwd=export_dir, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        time.sleep(3)

        if proc.poll() is None:
            _running_servers[project.id] = proc
            get_pidfile_path(export_dir).write_text(str(proc.pid))
            get_info_path(export_dir).write_text(json.dumps({"pid": proc.pid, "port": use_port}))
            import os
            is_prod = os.environ.get('PRODUCTION')
            subdomain = getattr(project, 'subdomain', None) or f"project-{project.id}"
            
            return {
                "status": "success",
                "preview_url": f"https://{subdomain}.codethinkers.org/" if is_prod else f"http://127.0.0.1:{use_port}/",
                "admin_url": f"https://{subdomain}.codethinkers.org/admin/" if is_prod else f"http://127.0.0.1:{use_port}/admin/",
                "port": use_port,
            }
        stderr_tail = proc.stderr.read()[-1000:] if proc.stderr else ""
        return f"Server failed to start: {stderr_tail}"
    except Exception as e:
        return f"Server restart failed: {str(e)}"


# ═════════════════════════════════════════════════════════════════
# AI REGENERATION (used both by the normal incremental-build endpoint
# and by the retry loop above)
# ═════════════════════════════════════════════════════════════════
def _generate_ai_changes(project, prompt, existing_files, retry_context=None, previous_changes=None):
    """Returns the parsed {analysis, changes, requires_migration, ...} dict,
    or None on failure. retry_context, if given, is a list of error strings
    from a failed previous attempt. previous_changes, if given, is the full
    change list from that failed attempt — included so the model doesn't
    silently drop unrelated files while fixing the reported error."""
    project_context = get_existing_project_context(project)
    file_map = {}
    for f in existing_files:
        content = f.content or ""
        if len(content) > 8000:
            content = content[:3000] + "\n\n... (truncated) ...\n\n" + content[-3000:]
        file_map[f.name] = {"id": f.id, "content": content, "size": len(f.content or ""), "extension": f.extension()}

    settings_file = existing_files.filter(name__regex=r'^[^/]+/settings\.py$').first()
    project_name = settings_file.name.split("/")[0] if settings_file else "project"

    system_prompt = _build_incremental_system_prompt(project_name, file_map, project_context)

    user_message = f"Request: {prompt}"

    if retry_context:
        prev_files_list = ""
        if previous_changes:
            prev_files_list = "\n".join(
                f"  - {c.get('action', '?')}: {c.get('file_path', '?')}"
                for c in previous_changes
            )
        user_message += (
            "\n\nYour previous attempt proposed these file changes:\n"
            + (prev_files_list or "(none captured)")
            + "\n\nBut it FAILED with these real errors "
              "(from static validation and/or actually loading the pages):\n"
            + "\n".join(retry_context)
            + "\n\nFix these specific issues WITHOUT dropping any of the other files "
              "listed above — you must resubmit the COMPLETE, corrected change set "
              "including every file from the list above that's still needed, not just "
              "the ones related to the error. If the error says a new model is missing "
              "a view, url, template, or admin registration, add that missing piece — "
              "do not remove the model instead. Resubmit COMPLETE file content for every "
              "affected file — do not use diffs."
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=16000,
            response_format={"type": "json_object"},
        )
        choice = response.choices[0]
        raw_text = choice.message.content
        print(f"✅ _generate_ai_changes response: {len(raw_text)} chars, finish_reason={choice.finish_reason}")

        if choice.finish_reason == "length":
            print("❌ Response truncated by max_tokens — cannot repair, only regenerate smaller")
            return None

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            if start == -1 or end <= start:
                return None
            try:
                return json.loads(raw_text[start:end])
            except json.JSONDecodeError:
                fixed = raw_text[start:end]
                fixed += '}' * (fixed.count('{') - fixed.count('}'))
                try:
                    result = json.loads(fixed)
                    print("🔧 Repaired JSON with missing closing braces")
                    return result
                except json.JSONDecodeError as e2:
                    print(f"❌ Could not repair JSON: {e2}")
                    return None
    except Exception as e:
        print(f"❌ _generate_ai_changes crashed: {e}")
        return None




# def _build_incremental_system_prompt(project_name, file_map, project_context):
#     return f"""You are an expert Full-Stack Software Architect and Senior Django Engineer making INCREMENTAL changes to an existing project.

# ═══ CURRENT PROJECT STATE ═══
# Project name: {project_name}
# Total files: {len(file_map)}
# Apps: {project_context['existing_apps']}
# Models: {project_context['existing_models']}
# URL namespaces: {project_context['existing_url_namespaces']}
# Templates: {project_context['existing_templates']}
# Has working login (accounts/ URLs + login template): {project_context.get('has_auth_urls', False) and project_context.get('has_login_template', False)}
# Has signup template: {project_context.get('has_signup_template', False)}

# COMPLETE FILE MAP (with content):
# {json.dumps(file_map, indent=2, default=str, ensure_ascii=False)}

# ═══ CRITICAL RULES ═══

# - For UPDATE: Provide the COMPLETE file with ALL existing code preserved
# - If adding models → register them in admin.py using @admin.register(ModelName). If admin.py
#   doesn't already define ExportAdminMixin (csv + docx export actions), add it once at the top
#   of the file. The new model's ModelAdmin MUST inherit it: class XAdmin(ExportAdminMixin,
#   admin.ModelAdmin). Set list_display (3-5 real fields), list_filter, search_fields,
#   list_per_page = 25, and readonly_fields for created_at/updated_at. Add date_hierarchy if the
#   model has a date field. Use autocomplete_fields for FKs to models that have search_fields.
#   If list_display or list_filter includes any ForeignKey field, list_select_related MUST list
#   that same field — required to avoid slow N+1 queries on the admin list page. Use TabularInline
#   if this model is clearly a child of another existing model. If admin.py already has
#   ExportAdminMixin defined, do NOT redefine it — just reuse it.
# - If adding views → also update urls.py and create necessary templates
# - **If adding, modifying, or removing ANY field in models.py: ALWAYS set requires_migration: true**
# - Any new field used for filtering/ordering (dates, status fields, booleans used in list_filter)
#   MUST have db_index=True set on it.
# - **If models.py is in the changes list at all: set requires_migration: true**
# - If modifying Python files → set requires_server_restart: true
# - Maintain consistent naming with existing code style
# - Every template referenced in views MUST have a corresponding entry in templates dict
# - All QuerySets MUST use .order_by('-id')
# - Every ListView MUST set paginate_by = 25 — never render an unpaginated list
# - If a model has ForeignKey/OneToOneField fields shown in the view's template, get_queryset MUST
#   use .select_related('field_name') for those fields. Use .prefetch_related('field_name') for
#   ManyToManyField or reverse FK relations. This avoids N+1 queries — required, not optional.
# - Any view whose queryset filters by self.request.user, or whose form_valid sets
#   form.instance.user = self.request.user, MUST inherit LoginRequiredMixin
#   (from django.contrib.auth.mixins) — request.user is AnonymousUser when logged out,
#   and using it in a FK filter without this guard crashes with TypeError.
# - ⚠️ MANDATORY: Every class-based view MUST have template_name = '...' as the VERY FIRST LINE inside the class body. This is the #1 cause of failures. NEVER omit it. Example:
#     class PostListView(ListView):
#         template_name = 'post_list.html'  # ← THIS IS REQUIRED, ALWAYS
#         model = Post
#         paginate_by = 25
#   If template_name is missing, the validation WILL reject your response. Every ListView, DetailView, CreateView, UpdateView, DeleteView needs this. NEVER rely on Django's default template path (which uses app_name/model_form.html).
# - Every CreateView and UpdateView with form_class or model MUST also include success_url (or override get_success_url). Without this, the form will crash after successful submission.
# - Template paths MUST be bare filenames: 'list.html' NOT 'app_name/list.html'. The templates dict keys must also be bare: "list.html" NOT "app_name/list.html".
# - If you reference views.X in urls.py, verify X actually exists as a class or function in your views.py content.
# - If you use a model in views.py (Model.objects.), verify it's imported from .models.

# - CONSISTENCY VERIFICATION (hard requirement, not a suggestion):
#   Before finalizing your JSON response, mentally trace every URL name you used in a
#   {{% url %}} tag back to a matching path(..., name=X) in urls.py, and every view class
#   referenced in urls.py back to a class actually present in your returned views.py content.
#   A model with no admin registration, a url with no matching view, or a template
#   referencing a url name that doesn't exist are all treated as incomplete work — fix them
#   before returning the response, do not leave them for a follow-up request.

# - AUTHENTICATION REQUIREMENT — if you add LoginRequiredMixin, @login_required, or any
#   user-filtered queryset ANYWHERE in this change, and "Has working login" in CURRENT
#   PROJECT STATE above is False, you MUST also include ALL of the following in your
#   changes list:
#     1. Update the project-level urls.py to include:
#        path('accounts/', include('django.contrib.auth.urls')),
#        (add the include() import if not already present)
#     2. Create <app_name>/templates/registration/login.html — extend the SAME base
#        template used by this project's other templates (match {{% extends %}} and
#        block names exactly), rendering the login form.
#     3. Add LOGIN_REDIRECT_URL to settings.py, set to the actual name= of this
#        project's home/index url (check existing urls.py — do not guess 'home' if the
#        project uses a different name).
#     4. If the change introduces user-owned content (any model with a user FK the
#        request user creates/edits), also add a signup view + urls.py entry
#        (/accounts/signup/) using Django's UserCreationForm, plus a matching
#        registration/signup.html template linked from login.html.
#   If "Has working login" is True, reuse the existing setup — do not duplicate urls.py
#   entries or overwrite existing templates.
#   Conversely, do NOT add LoginRequiredMixin or user-filtered querysets at all unless the
#   user's request implies private, per-account data — for simple/public/single-admin
#   features, leave views open and skip authentication entirely.

# - Always import `from django.db import models` when using models.Sum/Count/Avg/etc.
# - CRITICAL JSON RULES:
# - All code content MUST use JSON-safe escaping
# - Double quotes inside strings: \\"
# - Backslashes: \\\\\\\\
# - Newlines: \\\\n (but keep them as real newlines in the JSON string)
# - Template HTML: Use single quotes for attributes where possible
# - NEVER use unescaped double quotes inside JSON string values

# Return this EXACT JSON structure:
# {{"analysis": "...", "changes": [{{"file_path", "action", "content", "reason"}}], "requires_migration": bool, "requires_server_restart": bool}}
# No markdown, no explanation outside the JSON."""

def _build_incremental_system_prompt(project_name, file_map, project_context):
    base = _load_ai_rules()
    base += """

    ⚠️ INCREMENTAL MODE: You are MODIFYING an existing project. Return ONLY:
    {
        "analysis": "Brief summary",
        "changes": [{"file_path": "...", "action": "create|update|delete", "content": "...", "reason": "..."}],
        "requires_migration": true/false,
        "requires_server_restart": true/false
    }
    Do NOT return the scaffold format (app_name, models_py, etc.). Only return CHANGES.
    """
    base += f"""

═══ CURRENT PROJECT STATE ═══
Project name: {project_name}
Total files: {len(file_map)}
Apps: {project_context['existing_apps']}
Models: {project_context['existing_models']}
URL namespaces: {project_context['existing_url_namespaces']}
Templates: {project_context['existing_templates']}
Has working login (accounts/ URLs + login template): {project_context.get('has_auth_urls', False) and project_context.get('has_login_template', False)}
Has signup template: {project_context.get('has_signup_template', False)}

COMPLETE FILE MAP (with content):
{json.dumps(file_map, indent=2, default=str, ensure_ascii=False)}
"""
    return base


def repair_fstring_quote_collision(content):
            if not content or ("f'" not in content and 'f"' not in content):
                return content

            result = []
            i = 0
            n = len(content)

            while i < n:
                if content[i] == "f" and i + 1 < n and content[i + 1] in ("'", '"'):
                    quote_char = content[i + 1]
                    other_quote = '"' if quote_char == "'" else "'"
                    j = i + 2
                    depth = 0
                    found_end = None

                    while j < n:
                        c = content[j]
                        if c == "\\":
                            j += 2
                            continue
                        if c == "{":
                            depth += 1
                        elif c == "}":
                            depth -= 1
                        elif c == quote_char and depth == 0:
                            found_end = j
                            break
                        elif c == "\n":
                            break
                        j += 1

                    if found_end is not None:
                        body = content[i + 2:found_end]
                        if quote_char in body and other_quote not in body:
                            result.append(f"f{other_quote}{body}{other_quote}")
                        else:
                            result.append(content[i:found_end + 1])
                        i = found_end + 1
                        continue

                result.append(content[i])
                i += 1

            return "".join(result)

# ═════════════════════════════════════════════════════════════════
# HELPER: Scaffold Build (new project) - Your ORIGINAL code
# ═════════════════════════════════════════════════════════════════
def validate_and_repair_changes(changes):
    """Run the same class of repairs we already do for full builds
    (template path mismatches, syntax errors) over an incremental
    changes[] list, which has a different shape (file_path/content
    pairs, not an app_data dict)."""
    errors = []

    templates_by_app = {}
    for change in changes:
        path = change.get("file_path", "")
        if "/templates/" in path:
            app_name, template_name = path.split("/templates/", 1)
            templates_by_app.setdefault(app_name, set()).add(template_name)

    for change in changes:
        path = change.get("file_path", "")
        content = change.get("content", "")
        if not content or change.get("action") == "delete":
            continue

        if path.endswith("views.py"):
            app_name = path.split("/")[0]
            prefix = f"{app_name}/"

            def fix_render_call(match, app_name=app_name, prefix=prefix):
                full = match.group(0)
                template_name = match.group(1)
                if template_name.startswith(prefix):
                    bare_name = template_name[len(prefix):]
                    return full.replace(template_name, bare_name)
                return full

            content = re.sub(
                r"""render\([^,]+,\s*['"]([^'"]+)['"]""",
                fix_render_call,
                content,
            )
            change["content"] = content

            app_templates = templates_by_app.get(app_name, set())
            for template_ref in re.findall(
                r"""render\([^,]+,\s*['"]([^'"]+)['"]""", content
            ):
                if template_ref not in app_templates:
                    errors.append(
                        f"{path}: render() references '{template_ref}' "
                        f"which isn't in this change set's templates for '{app_name}' "
                        f"— it must already exist on disk, or this will fail."
                    )

     
        if path.endswith(".py"):
            # Fix literal \n in AI responses (common with JSON escaping issues)
            if '\\n' in content and '\n' not in content:
                content = content.replace('\\n', '\n')
            # Fix trailing commas in import lines
            content = re.sub(r'(from\s+[\w.]+\s+import\s+[\w\s,]+),(\s*\n)', r'\1\2', content)
            try:
                compile(content, path, "exec")
            except SyntaxError:
                                # Fix trailing commas in imports
                content = re.sub(r',\s*\n\s*from\s+', r'\nfrom ', content)
                content = re.sub(r',\s*\)', r')', content)
                repaired = repair_fstring_quote_collision(content)
                try:
                    compile(repaired, path, "exec")
                    change["content"] = repaired
                    print(f"🔧 Auto-repaired f-string quote collision in {path}")
                except SyntaxError as e2:
                    errors.append(f"{path}: {e2.msg} at line {e2.lineno}")

    return changes, errors

def validate_and_repair_python_files(files_dict):
            unrecoverable = []
            
            if not files_dict:
                return {}, unrecoverable
            
            for path, content in list(files_dict.items()):
                if not path.endswith(".py") or not content:
                    continue
                
                # Fix "from x import y," → "from x import y" (AI common mistake)
                if path.endswith("urls.py"):
                    content = re.sub(r'(from django\.urls import path),(\s*\n)', r'\1\2', content)
                
                try:
                    compile(content, path, "exec")

                    continue
                except SyntaxError:
                    pass

                                # Fix trailing commas in imports
                content = re.sub(r',\s*\n\s*from\s+', r'\nfrom ', content)
                content = re.sub(r',\s*\)', r')', content)
                repaired = repair_fstring_quote_collision(content)
                try:
                    compile(repaired, path, "exec")
                    files_dict[path] = repaired
                    print(f"🔧 Auto-repaired f-string quote collision in {path}")
                except SyntaxError as e2:
                    unrecoverable.append(f"{path}: {e2.msg} at line {e2.lineno}")
                    print(f"❌ Unrecoverable syntax error in {path}: {e2.msg} at line {e2.lineno}")
            
            return files_dict, unrecoverable




def _scaffold_build(project, prompt):
    """
    Full scaffold — AI thinks like a senior architect before generating code.
    Follows the 10-step thinking framework for production-quality Django apps.
    """
    try:
        # -----------------------------------------------------------
        # Helper: Validate AI-generated app data
        # -----------------------------------------------------------
        def validate_app_data(app_data):
            errors = []
            warnings = []

            if not app_data:
                return errors, warnings

           
            required_fields = ["app_name", "views_py", "urls_py"]
            for field in required_fields:
                if not app_data.get(field):
                    errors.append(f"Missing required field: {field}")
            # models_py and admin_py are only required if the app actually
            # needs persistent data — a static site (portfolio, landing
            # page) may legitimately have none.
            if app_data.get("models_py") and not app_data.get("admin_py"):
                errors.append("Missing required field: admin_py (models_py is present, so admin registration is expected)")

            if app_data.get("models_py"):
                model_count = len(re.findall(r'class\s+\w+\s*\(.*models\.Model\)', app_data["models_py"]))
                if model_count == 0:
                    errors.append("models_py must contain at least one Django model class")

            if app_data.get("views_py") and app_data.get("templates"):
                template_refs = re.findall(
                    r"render\([^,]+,\s*['\"]([^'\"]+)['\"]",
                    app_data["views_py"]
                )
                clean_refs = set()
                for ref in template_refs:
                    clean_refs.add(ref.split("/")[-1] if "/" in ref else ref)
                provided_templates = set(app_data["templates"].keys())
                missing = clean_refs - provided_templates
                if missing:
                    errors.append(f"Views reference templates not provided: {missing}")

            if app_data.get("models_py") and app_data.get("admin_py"):
                model_names = re.findall(r"class\s+(\w+)\s*\(.*Model\)", app_data["models_py"])
                for model in model_names:
                    if (f"admin.site.register({model}" not in app_data["admin_py"] and
                        f"@admin.register({model}" not in app_data["admin_py"]):
                        warnings.append(f"Model '{model}' may not be registered in admin.py")

            if app_data.get("urls_py"):
                if "app_name" not in app_data["urls_py"]:
                    warnings.append("urls.py missing app_name declaration")

            if app_data.get("views_py"):
                views_content = app_data["views_py"]
                if "form.save()" not in views_content and "objects.create(" not in views_content:
                    if "request.method == 'POST'" in views_content:
                        warnings.append("views.py has POST handling but may not save data")

            return errors, warnings

  
        # -----------------------------------------------------------
        # Helper: Repair AI-generated views
        # -----------------------------------------------------------

        def repair_views_py(content):
            if not content:
                return content

            pattern = r'(\w+)\s*=\s*(\w+)\.objects\.all\(\)(?!\s*\.order_by)'
            def fix_queryset(match):
                var_name = match.group(1)
                model = match.group(2)
                return f'{var_name} = {model}.objects.all().order_by("-id")'
            content = re.sub(pattern, fix_queryset, content)

            content = re.sub(
                r'\.filter\([^)]*\)\.all\(\)(?!\s*\.order_by)',
                lambda m: m.group(0).replace('.all()', '.all().order_by("-id")'),
                content
            )

            content = re.sub(
                r"render\(request,\s*['\"][\w]+/(\w+\.html)['\"]",
                r"render(request, '\1'",
                content
            )

            return content
        

        def normalize_template_paths(app_name, views_py, templates):
            """Fix template references that mistakenly use 'app_name/file.html'
            instead of the bare 'file.html' filename your pipeline expects.
            Handles both render() calls AND template_name = '...' assignments."""
            if not views_py:
                return views_py, templates

            prefix = f"{app_name}/"

            def fix_path(match):
                full = match.group(0)
                template_name = match.group(1)
                if template_name.startswith(prefix):
                    bare_name = template_name[len(prefix):]
                    return full.replace(template_name, bare_name)
                return full

            # Fix render() calls
            fixed_views = re.sub(
                r"""render\([^,]+,\s*['"]([^'"]+)['"]""",
                fix_path,
                views_py,
            )
            
            # Fix template_name = 'app_name/file.html'
            fixed_views = re.sub(
                r"""template_name\s*=\s*['"]([^'"]+)['"]""",
                fix_path,
                fixed_views,
            )
            
            return fixed_views, templates   
        # -----------------------------------------------------------
        # Helper: f-string quote collision repair
        # -----------------------------------------------------------
    
        # ─────────────────────────────────────────────────────
        # STEP 1-2: Generate project name
        # ─────────────────────────────────────────────────────
        scaffold_cache_key = f"scaffold_{hashlib.md5(prompt.encode()).hexdigest()}"
        scaffold_data = cache.get(scaffold_cache_key)

        if not scaffold_data:
            scaffold_system = """You are an expert Django developer.
Given a project description, choose a short, descriptive Django project name.
Return ONLY this JSON: {"project_name": "mysite"}
RULES: project_name must be a valid Python identifier (lowercase, underscores only). No markdown, no explanation."""

            scaffold_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": scaffold_system},
                    {"role": "user", "content": f"Generate a Django project scaffold for: {prompt}"},
                ],
                max_tokens=3000, temperature=0.3,
                response_format={"type": "json_object"}
            )

            scaffold_text = scaffold_response.choices[0].message.content.strip()
            try:
                scaffold_data = json.loads(scaffold_text)
            except json.JSONDecodeError:
                start = scaffold_text.find("{")
                end = scaffold_text.rfind("}") + 1
                if start != -1 and end > start:
                    scaffold_data = json.loads(scaffold_text[start:end])
                else:
                    return JsonResponse({"status": "error", "message": "No valid JSON in scaffold response"}, status=500)

            if not isinstance(scaffold_data, dict):
                return JsonResponse({"status": "error", "message": "Invalid scaffold response format"}, status=500)

            cache.set(scaffold_cache_key, scaffold_data, timeout=3600)
            print("✅ Generated new scaffold (cache miss)")
        else:
            print("✅ Using cached scaffold")

        project_name = normalize_name(scaffold_data.get("project_name", "mysite"), fallback="mysite")

        # ─────────────────────────────────────────────────────
        # STEPS 3-10: AI ARCHITECT + FULL CODE GENERATION
        # ─────────────────────────────────────────────────────
        context = get_existing_project_context(project)
        context_note = ""
        if context["existing_apps"] or context["existing_models"]:
            context_note = f"""
EXISTING PROJECT STATE (avoid collisions):
- Existing app names: {context['existing_apps'] or "none"}
- Existing model names: {context['existing_models'] or "none"}
Pick distinct, descriptive names."""

        state_fingerprint = hashlib.md5(
            prompt.encode() +
            str(sorted(context["existing_apps"])).encode() +
            str(sorted(context["existing_models"])).encode()
        ).hexdigest()
        app_cache_key = f"app_{project.id}_{state_fingerprint}_v5_architect"
        cache.delete(app_cache_key)

        # ── THE ARCHITECT SYSTEM PROMPT ──
        # ── Load AI rules from modular files ──
        architect_system = _load_ai_rules()
       
        architect_system = architect_system.replace("__CONTEXT_NOTE__", context_note)

        app_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": architect_system},
                {"role": "user", "content": f"Build a complete Django application for: {prompt}"},
            ],
            max_tokens=16000,
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        app_choice = app_response.choices[0]
        app_text = app_choice.message.content.strip()
        print(f"✅ AI Architect Response: {len(app_text)} chars, finish_reason={app_choice.finish_reason}")

        if app_choice.finish_reason == "length":
            print("⚠️ Response truncated — retrying with minimal template instructions")
            retry_prompt = f"{prompt}\n\n[SYSTEM NOTE: Your previous response was truncated because it was too large. Generate a complete response but keep templates minimal — single-file functional HTML, no inline CSS beyond Tailwind classes, reuse navbar/footer structure. Prioritize completeness over visual polish.]"
            
            retry_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": architect_system},
                    {"role": "user", "content": f"Build a complete Django application for: {retry_prompt}"},
                ],
                max_tokens=16000,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            retry_choice = retry_response.choices[0]
            app_text = retry_choice.message.content.strip()
            print(f"🔄 Retry response: {len(app_text)} chars, finish_reason={retry_choice.finish_reason}")
            
            if retry_choice.finish_reason == "length":
                # Third attempt: split into two phases
                print("⚠️ Still truncated — splitting into architecture + templates phases")
                
                # Phase 1: Architecture only (no templates)
                arch_prompt = f"{prompt}\n\n[SYSTEM NOTE: Generate ONLY the architecture files — models.py, admin.py, urls.py, views.py, forms.py, tests.py. Do NOT generate any templates. Templates will be generated in a separate pass.]"
                
                arch_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": architect_system},
                        {"role": "user", "content": f"Build a complete Django application (architecture only, no templates): {arch_prompt}"},
                    ],
                    max_tokens=16000,
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                
                arch_choice = arch_response.choices[0]
                arch_text = arch_choice.message.content.strip()
                print(f"🏗️ Architecture response: {len(arch_text)} chars, finish_reason={arch_choice.finish_reason}")
                
                if arch_choice.finish_reason == "length":
                    return JsonResponse({
                        "status": "error",
                        "message": "Project is too large even without templates. Try fewer models/pages.",
                        "detail": "finish_reason=length (architecture-only also truncated)",
                    }, status=500)
                
                # Parse architecture
                try:
                    arch_data = json.loads(arch_text)
                except json.JSONDecodeError:
                    start = arch_text.find("{")
                    end = arch_text.rfind("}") + 1
                    if start != -1 and end > start:
                        arch_data = json.loads(arch_text[start:end])
                    else:
                        return JsonResponse({"status": "error", "message": "Invalid JSON in architecture response"}, status=500)
                
                # Phase 2: Templates only
                arch_summary = json.dumps({
                    "app_name": arch_data.get("app_name", ""),
                    "models": arch_data.get("models_py", "")[:500],
                    "views": arch_data.get("views_py", "")[:500],
                    "urls": arch_data.get("urls_py", "")[:300],
                }, indent=2)
                
                template_prompt = f"Based on this architecture:\n{arch_summary}\n\nGenerate ALL required templates. Include: home.html (dashboard with stats), list.html, detail.html, form.html (create/edit), confirm_delete.html. Use Tailwind CDN, same navbar/footer on every page. Keep each template functional and minimal — prioritize completeness."
                
                template_system = """You are a Django template expert. Return ONLY valid JSON with a templates dict. Every template must have proper HTML structure with Tailwind CDN navbar and footer. Use bare template names (no app prefix)."""
                
                template_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": template_system},
                        {"role": "user", "content": template_prompt},
                    ],
                    max_tokens=16000,
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                
                template_choice = template_response.choices[0]
                template_text = template_choice.message.content.strip()
                print(f"📄 Templates response: {len(template_text)} chars, finish_reason={template_choice.finish_reason}")
                
                try:
                    template_data = json.loads(template_text)
                except json.JSONDecodeError:
                    start = template_text.find("{")
                    end = template_text.rfind("}") + 1
                    if start != -1 and end > start:
                        template_data = json.loads(template_text[start:end])
                    else:
                        # Use fallback templates
                        template_data = {"templates": {}}
                
                # Merge: architecture data + templates
                app_text = json.dumps({**arch_data, "templates": template_data.get("templates", {})})
                print(f"🔗 Merged response: {len(app_text)} chars")
                
                app_choice = type('obj', (object,), {
                    'message': type('obj', (object,), {'content': app_text}),
                    'finish_reason': 'stop'
                })()
            
            app_choice = retry_choice if 'app_choice' not in dir() or app_choice is retry_choice else app_choice


                # Fix common JSON issues in AI responses

        # 1. Remove markdown code fences if present
        app_text = re.sub(r'^```json\s*', '', app_text)
        app_text = re.sub(r'\s*```$', '', app_text)
        
        # 2. Try to fix unescaped quotes in string values
        # Find the error position and log it
        try:
            json.loads(app_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON error at line {e.lineno}, column {e.colno}, char {e.pos}")
            # Show context around the error
            start_ctx = max(0, e.pos - 100)
            end_ctx = min(len(app_text), e.pos + 100)
            print(f"   Context: ...{app_text[start_ctx:end_ctx]}...")


        try:
            app_data = json.loads(app_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            # Try to fix common issues
            start = app_text.find("{")
            end = app_text.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    app_data = json.loads(app_text[start:end])
                except json.JSONDecodeError as e2:
                    # Try adding missing closing braces
                    fixed = app_text[start:end]
                    # Count braces
                    open_braces = fixed.count('{') - fixed.count('}')
                    fixed += '}' * open_braces
                    try:
                        app_data = json.loads(fixed)
                        print("🔧 Repaired JSON with missing closing braces")
                    except json.JSONDecodeError:
                        print(f"❌ Could not repair JSON: {e2}")
                        return JsonResponse({
                            "status": "error", 
                            "message": f"Invalid JSON from AI. Try again with a simpler prompt.",
                            "detail": str(e2)[:200]
                        }, status=500)
            else:
                return JsonResponse({
                    "status": "error", 
                    "message": "No valid JSON in AI response. Try again."
                }, status=500)
        if not isinstance(app_data, dict):
            return JsonResponse({"status": "error", "message": "Invalid app response format"}, status=500)

        # ── Extract thinking process ──
        thinking = app_data.get("thinking", {})
        self_check = app_data.get("self_check", {})
        print(f"🔎 AI Self-Check: {json.dumps(self_check, indent=2)}")

        print(f"🧠 AI Thinking:")
        print(f"   Business: {thinking.get('business_understanding', 'N/A')[:100]}")
        print(f"   App Type: {thinking.get('app_type', 'N/A')}")
        print(f"   Modules: {thinking.get('core_modules', [])}")
        print(f"   DB Design: {thinking.get('database_design', 'N/A')[:100]}")
        print(f"   Pages: {thinking.get('page_plan', [])}")
        print(f"   Suggested: {thinking.get('suggested_features', [])}")

        app_name = normalize_name(app_data.get("app_name", "core"), fallback="core")
        if app_name == project_name:
            app_name = f"{app_name}_app"

        existing_apps = get_existing_project_context(project)["existing_apps"]
        original_app_name = app_name
        suffix = 2
        while app_name in existing_apps:
            app_name = f"{original_app_name}_{suffix}"
            suffix += 1

        # ── Fix namespaced URLs ──
        def namespace_url_references(app_name, urls_py, views_py, templates):
            route_names = set(re.findall(r"""name=['"](\w+)['"]""", urls_py or ""))
            if not route_names:
                return views_py, templates

            def fix_py_calls(content):
                if not content: return content
                def fix(match):
                    fn, name = match.group(1), match.group(2)
                    if name in route_names: return f"{fn}('{app_name}:{name}'"
                    return match.group(0)
                return re.sub(r"""\b(redirect|reverse|reverse_lazy)\(\s*['"](\w+)['"]""", fix, content)

            def fix_template_tags(content):
                if not content: return content
                def fix(match):
                    name = match.group(1)
                    if name in route_names: return "{% url '" + app_name + ":" + name + "'"
                    return match.group(0)
                return re.sub(r"""\{%\s*url\s+['"](\w+)['"]""", fix, content)

            return fix_py_calls(views_py), {n: fix_template_tags(c) for n, c in (templates or {}).items()}

        app_data["views_py"], app_data["templates"] = normalize_template_paths(
            app_name, app_data.get("views_py", ""), app_data.get("templates", {})
            )

        # ── Repair views (with fallback) ──
        views_content = app_data.get("views_py", "")
        if views_content and views_content.strip():
            app_data["views_py"] = repair_views_py(views_content)
        else:
            fallback_views = f'''from django.views.generic import ListView
from django.db import models

class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'objects'
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self):
        from django.apps import apps
        try:
            app_config = apps.get_app_config('{app_name}')
            first_model = list(app_config.get_models())[0] if app_config.get_models() else None
            if first_model:
                return first_model.objects.all().order_by('-id')
        except Exception:
            pass
        return models.QuerySet()
'''
            app_data["views_py"] = fallback_views
            print("⚠️ Generated fallback views.py")

        # ── Validate ──
        errors, warnings = validate_app_data(app_data)
        if errors: print(f"⚠️ Validation errors: {errors}")
        if warnings: print(f"⚠️ Validation warnings: {warnings}")

        cache.set(app_cache_key, app_data, timeout=3600)

        # ─────────────────────────────────────────────────────
        # ASSEMBLE FILES — via the SHARED function, so attempt 0
        # and any retry run through the exact same auto-fix passes.
        # ─────────────────────────────────────────────────────
        db_pattern = str(Path(settings.BASE_DIR) / "project_databases" / f"*{project.id}*.sqlite3*")
        for db_file in glob.glob(db_pattern):
            try: os.remove(db_file)
            except Exception: pass

        settings_content = build_settings_py(project_name)
        urls_content = build_base_urls_py()
        settings_content = inject_installed_app(settings_content, app_name)
        urls_content = inject_url_include(urls_content, app_name)
        urls_content = inject_admin_branding(urls_content, project_name, app_name)

        new_files = _assemble_and_autofix_scaffold_files(
            app_data, app_name, project_name, settings_content, urls_content
        )

        new_files, syntax_errors = validate_and_repair_python_files(new_files)
        if syntax_errors:
            return JsonResponse({
                "status": "error",
                "message": "Generated code has syntax errors",
                "errors": syntax_errors,
            }, status=500)
        # ─────────────────────────────────────────────────────
        # Route through the same staged apply pipeline the
        # incremental path uses — static validation, staging
        # export, manage.py check, migrations, smoke test, and
        # rollback-on-failure, all for free instead of duplicated.
        # ─────────────────────────────────────────────────────
        is_fresh_project = not File.objects.filter(project=project).exists()
        action = "create" if is_fresh_project else "update"

        pseudo_changes = [
            {"file_path": path, "action": action if File.objects.filter(project=project, name=path).exists() else "create",
             "content": content}
            for path, content in new_files.items()
            if content is not None
        ]

        
        # A fresh scaffold build always needs migrations (new models)
        # and a server restart (all-new Python code).
        # Retry up to 2 times if validation fails, feeding errors back to AI.
        max_scaffold_retries = 2
        for scaffold_attempt in range(max_scaffold_retries + 1):
            apply_result = _attempt_apply(
                project, pseudo_changes,
                requires_migration=True,
                requires_server_restart=True,
            )
      
            if apply_result["ok"]:
                break
            
            # If auto-fix already ran (we generated views/templates), skip AI retry
            # and just let the validation errors through — they're likely from AI overwriting our fixes
            if scaffold_attempt == 0 and (
                apply_result.get("validation_errors") or apply_result.get("smoke_test_errors")
            ):
                error_context = apply_result.get("failure_summary", "")[:2000]
                print(f"⚠️ Scaffold validation failed (attempt {scaffold_attempt + 1}) — regenerating with error context")

                common_fixes_path = Path(settings.BASE_DIR) / "ai_rules" / "common_fixes.md"
                common_fixes = common_fixes_path.read_text(encoding="utf-8") if common_fixes_path.exists() else ""

                retry_prompt = (
                    f"{prompt}\n\n"
                    f"[❌ YOUR PREVIOUS RESPONSE FAILED WITH THESE EXACT ERRORS:]\n"
                    f"{error_context}\n\n"
                    f"[YOU MUST FIX EVERY ERROR ABOVE BEFORE RETURNING.]\n\n"
                    f"{common_fixes}"
                )
                
                retry_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": architect_system},
                        {"role": "user", "content": f"Build a complete Django application for: {retry_prompt}"},
                    ],
                    max_tokens=16000,
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                
                retry_choice = retry_response.choices[0]
                retry_text = retry_choice.message.content.strip()
                print(f"🔄 Retry {scaffold_attempt + 1} response: {len(retry_text)} chars, finish_reason={retry_choice.finish_reason}")
                
                if retry_choice.finish_reason == "length":
                    print("⚠️ Retry truncated — trying one more time with minimal templates")
                    continue
                
                # Re-parse the retry response
                try:
                    retry_data = json.loads(retry_text)
                except json.JSONDecodeError:
                    start = retry_text.find("{")
                    end = retry_text.rfind("}") + 1
                    if start != -1 and end > start:
                        try:
                            retry_data = json.loads(retry_text[start:end])
                        except json.JSONDecodeError:
                            continue
                    else:
                        continue
                
                if not isinstance(retry_data, dict):
                    continue
                
                # Rebuild pseudo_changes from retry data
                retry_app_name = normalize_name(retry_data.get("app_name", "core"), fallback="core")
                if retry_app_name == project_name:
                    retry_app_name = f"{retry_app_name}_app"
                
            
                retry_data["views_py"], retry_data["templates"] = normalize_template_paths(
                    retry_app_name, retry_data.get("views_py", ""), retry_data.get("templates", {})
                )
                retry_urls_content = inject_url_include(build_base_urls_py(), retry_app_name)
                retry_urls_content = inject_admin_branding(retry_urls_content, project_name, retry_app_name)
                if retry_app_name != app_name:
                    settings_content = inject_installed_app(settings_content, retry_app_name)

                retry_new_files = _assemble_and_autofix_scaffold_files(
                    retry_data, retry_app_name, project_name, settings_content, retry_urls_content
                )
                retry_new_files, _retry_syntax_errors = validate_and_repair_python_files(retry_new_files)

                pseudo_changes = [
                    {"file_path": path, "action": "create", "content": content}
                    for path, content in retry_new_files.items()
                    if content is not None
                ]
                
               
                # Update app_name for the success response
                app_name = retry_app_name
                app_data = retry_data
                thinking = retry_data.get("thinking", thinking)
            elif scaffold_attempt > 0:
                # Already retried once — don't keep trying
                print(f"⚠️ Validation still failing after AI retry — exiting retry loop")
                break

        if not apply_result["ok"]:
            
            print(f"❌ Apply failed after {scaffold_attempt + 1} attempt(s): {apply_result['failure_summary'][:500]}")
            return JsonResponse({
                "status": "error",
                "message": f"Generated app failed validation after {scaffold_attempt + 1} attempt(s).",
                "detail": apply_result["failure_summary"],
                "validation_errors": apply_result.get("validation_errors"),
                "smoke_test_errors": apply_result.get("smoke_test_errors"),
                "thinking": thinking,
            }, status=500)

        payload = apply_result["payload"]
        files_created = [a["file"] for a in payload["applied"]]

        return JsonResponse({
            "status": "success",
            "build_type": "scaffold",
            "message": f"✨ Generated project '{project_name}' with app '{app_name}' — {len(files_created)} files",
            "files_created": files_created,
            "project_name": project_name,
            "app_name": app_name,
            "thinking": thinking,
            "warnings": warnings if warnings else [],
            "migration_result": payload.get("migration_result"),
            "restart_result": payload.get("restart_result"),
        })

    except Exception as e:
        print(f"❌ Scaffold Build Error: {traceback.format_exc()}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
        





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

    # Find the exam tied to this course, if one exists
    exam = ExamCourse.objects.filter(course_name=course).first() if course else None

    # Fetch topics using the course object
    topics = Topics.objects.filter(courses=course).select_related("courses", "categories") if course else Topics.objects.none()
    
    # Get or create StudentProgress
    progress = StudentProgress.objects.filter(
        student=request.user,
        course=course
    ).prefetch_related('completed_topics').order_by('-last_updated').first()

    # Get only topic IDs that belong to THIS course
    course_topic_ids = set(topics.values_list('id', flat=True))

    completed_topic_ids = list(
        progress.completed_topics.filter(id__in=course_topic_ids).values_list('id', flat=True)
    ) if progress else []

    # ===== CALCULATE POINTS =====
    total_topics = topics.count()
    earned_points = len(completed_topic_ids)
    
    # ===== GET CHAMPION XP & RANK ON PAGE LOAD (READ ONLY) =====
    champion_xp = 0
    user_rank = None
    if course:
        leaderboard_entry = LeaderboardEntry.objects.filter(
            student=request.user, course=course
        ).first()
        if leaderboard_entry:
            champion_xp = leaderboard_entry.champion_xp
            user_rank = leaderboard_entry.rank
    
    # ===== USE STORED CURRENT_TOPIC FROM PROGRESS =====
    current_topic_id = None
    current_topic = None
    if progress and progress.current_topic:
        current_topic_id = progress.current_topic.id
        current_topic = progress.current_topic
    elif topics.exists():
        completed_ids = set(completed_topic_ids)
        for topic in topics:
            if topic.id not in completed_ids:
                current_topic_id = topic.id
                current_topic = topic
                break
        if not current_topic_id and topics.exists():
            current_topic = topics.last()
            current_topic_id = current_topic.id
        if progress and current_topic_id:
            try:
                progress.current_topic = Topics.objects.get(id=current_topic_id)
                progress.save(update_fields=['current_topic'])
            except Topics.DoesNotExist:
                pass

    # ===== START TIME TRACKING ON PAGE LOAD =====
    if progress and current_topic_id and not progress.module_start_time:
        progress.module_start_time = timezone.now()
        progress.save(update_fields=['module_start_time'])

    # ================= SIDEBAR EXTENSIONS =================
    exts = sorted({
        os.path.splitext(f.name)[1].lstrip(".").lower()
        for f in files if "." in f.name
    })

    IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif")
    is_image = file.name.lower().endswith(IMAGE_EXTS)

    # ================= FILE TYPE =================
    ext = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
    is_python = ext == "py"

    # ================= POST =================
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode()) if request.body else {}
        except json.JSONDecodeError:
            data = {}

        new_content = data.get("content", "")
        run_plot = data.get("run_plot", False)
        run_table = data.get("run_table", False)
        prompt = data.get("prompt", "")
        ai_action = data.get("ai_action", "")
        topic_id = data.get("topic_id")

        # ================= SCORE OUTPUT =================
        if data.get("action") == "score_output":
            import re
            student_output = data.get("student_output", "").strip()
            topic_id = data.get("topic_id")
            
            if not topic_id:
                return JsonResponse({"status": "error", "message": "No topic ID provided"}, status=400)

            try:
                topic = Topics.objects.get(id=topic_id)
            except Topics.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Topic not found"}, status=404)

            topic_desc = topic.desc or ""
            topic_title = topic.title or ""
            expected = topic.expected_output or ""

            from html.parser import HTMLParser

            class HTMLStripper(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text_parts = []
                def handle_data(self, data):
                    self.text_parts.append(data)
                def get_text(self):
                    return '\n'.join(part.strip() for part in self.text_parts if part.strip())

            def strip_html(html_text):
                stripper = HTMLStripper()
                stripper.feed(html_text)
                return stripper.get_text()

            plain_desc = strip_html(topic_desc)
            print_count_in_desc = plain_desc.count('print(')

            if expected:
                expected_lines = len(expected.strip().splitlines())
                if expected_lines < print_count_in_desc:
                    print(f"⚠️ Cached expected has {expected_lines} lines but code has {print_count_in_desc} prints — regenerating")
                    expected = ""
                    topic.expected_output = ""
                    topic.save(update_fields=['expected_output'])

            if not expected:
                code_blocks = re.findall(r'```python\n(.*?)```', topic_desc, re.DOTALL)
                code_content = '\n'.join(code_blocks) if code_blocks else plain_desc

                expected_prompt = f"""You are a Python code analyzer. Analyze this code and determine what it WILL ALWAYS output when executed.

## CODE TO ANALYZE:
{code_content}

## CRITICAL INSTRUCTIONS:
1. Execute the code mentally, following ALL logic paths
2. Identify ALL print() statements
3. For each print(), determine if the output is:
   - FIXED: Always prints the same thing regardless of any input
   - CONDITIONAL: Prints based on logic that doesn't depend on user input
   - INPUT_DEPENDENT: Output changes based on user input

## DECISION TREE:
- If the code has ONLY input-dependent prints → return: VARIABLE_OUTPUT
- If the code has ONLY fixed/conditional prints → return the exact output, one line per print()
- If the code has a MIX of fixed and input-dependent prints → return only the fixed ones

## IMPORTANT RULES FOR CONDITIONALS:
- If there's an if/else that checks user input, return BOTH possibilities on separate lines

Return ONLY the output lines (or VARIABLE_OUTPUT), nothing else. No markdown, no explanation."""
                
                try:
                    if client is None:
                        return JsonResponse({"status": "error", "message": "OpenAI API is not configured"}, status=500)
                    
                    expected_response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a Python code analyzer. Determine the exact output or return VARIABLE_OUTPUT. Include outputs from ALL branches."},
                            {"role": "user", "content": expected_prompt},
                        ],
                        max_tokens=300,
                        temperature=0,
                    )
                    expected = expected_response.choices[0].message.content.strip()
                    expected = re.sub(r'^(output|result|answer)\s*:\s*', '', expected, flags=re.IGNORECASE).strip()
                    print(f"🤖 AI Generated Expected Output: '{expected}'")
                    
                    topic.expected_output = expected
                    topic.save(update_fields=['expected_output'])
                except Exception as e:
                    print(f"⚠️ Failed to generate expected output: {e}")
                    expected = ""

            if not progress:
                progress, _ = StudentProgress.objects.get_or_create(
                    student=request.user, course=course
                )
            
            new_rank = user_rank
            new_xp = champion_xp
            xp_earned = 0
            already_awarded = progress.completed_topics.filter(id=topic_id).exists()
            earned_points = progress.completed_topics.filter(id__in=course_topic_ids).count()
            display_score = earned_points

            if expected == "VARIABLE_OUTPUT" or not expected:
                return JsonResponse({
                    "status": "success",
                    "result": {
                        "score": display_score,
                        "max_score": total_topics,
                        "feedback": "✅ Code ran successfully! Output varies by input — marked as complete.",
                        "correct": True
                    },
                    "points": earned_points,
                    "total_topics": total_topics,
                    "rank": new_rank,
                    "champion_xp": new_xp,
                    "xp_earned": xp_earned,
                    "already_awarded": already_awarded,
                    "average_score": progress.get_average_score() if progress else 0,
                    "modules_completed": min(earned_points, total_topics),
                    "expected_output": "VARIABLE_OUTPUT",
                })

            scoring_prompt = f"""You are a Python output checker. Compare the student's output against the expected output.

EXPECTED OUTPUT (may have multiple possible correct answers from conditional branches):
---
{expected}
---

STUDENT'S ACTUAL OUTPUT:
---
{student_output}
---

## SCORING RULES:
1. Clean both outputs: Remove input prompts, empty lines, strip whitespace
2. If expected has MULTIPLE possible outputs: Student must match EXACTLY ONE — score = 1
3. If expected has SINGLE output: Student must contain all expected lines — score = 1
4. Extra lines in student output are OK

Return ONLY valid JSON:
{{"score": 0, "max_score": 1, "feedback": "reason here", "correct": false}}"""
            
            try:
                if client is None:
                    return JsonResponse({"status": "error", "message": "OpenAI API is not configured"}, status=500)
                    
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a strict but fair Python output checker. Handle conditional outputs correctly."},
                        {"role": "user", "content": scoring_prompt},
                    ],
                    max_tokens=300,
                    temperature=0,
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)
                
                xp_before = champion_xp
                
                if progress.module_start_time:
                    time_spent = (timezone.now() - progress.module_start_time).total_seconds()
                    progress.total_time_spent_seconds += int(time_spent)
                    progress.module_start_time = timezone.now()
                    progress.save(update_fields=['total_time_spent_seconds', 'module_start_time'])
                    print(f"⏱️ Scored: +{int(time_spent)}s | Total: {progress.total_time_spent_seconds}s")
                
                if result.get('correct', False):
                    if not already_awarded:
                        progress.completed_topics.add(topic)
                        progress.add_assessment_score(100, topic_id, first_attempt=True)
                        
                        earned_points = progress.completed_topics.filter(id__in=course_topic_ids).count()
                        display_score = earned_points
                        
                        try:
                            update_streak(request.user, course)
                            entry = update_leaderboard_entry(request.user, course)
                            check_badges(request.user, course, progress)
                            
                            if entry:
                                new_rank = entry.rank
                                new_xp = entry.champion_xp
                                xp_earned = new_xp - xp_before
                                print(f"🏆 Topic {topic_id} completed! XP: {new_xp} (+{xp_earned}), Rank: #{new_rank}")
                        except Exception as e:
                            print(f"⚠️ Failed to update leaderboard: {e}")
                    else:
                        display_score = earned_points
                        xp_earned = 0
                        result['feedback'] = (result.get('feedback', '') + 
                            '\n\n📌 Module already completed - no additional XP.')
                else:
                    progress.incorrect_code_attempts += 1
                    progress.save(update_fields=['incorrect_code_attempts'])
                    display_score = earned_points
                
                return JsonResponse({
                    "status": "success",
                    "result": {
                        "score": display_score,
                        "max_score": total_topics,
                        "feedback": result.get('feedback', ''),
                        "correct": result.get('correct', False)
                    },
                    "points": earned_points,
                    "total_topics": total_topics,
                    "rank": new_rank,
                    "champion_xp": new_xp,
                    "xp_earned": xp_earned,
                    "already_awarded": already_awarded,
                    "average_score": progress.get_average_score() if progress else 0,
                    "modules_completed": min(earned_points, total_topics),
                    "expected_output": expected,
                    "total_time_spent_seconds": progress.total_time_spent_seconds,
                })
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)

        # ================= UPDATE ACTIVE TOPIC =================
        if data.get("action") == "update_active_topic":
            topic_id = data.get("topic_id")
            course_id = data.get("course_id")
            
            if not course_id:
                return JsonResponse({"status": "error", "message": "Course ID is required"}, status=400)
            
            try:
                course_obj = Courses.objects.get(id=course_id)
            except Courses.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Course not found"}, status=404)
            
            progress_obj, _ = StudentProgress.objects.get_or_create(
                student=request.user, course=course_obj
            )
            
            if progress_obj.module_start_time:
                time_spent = (timezone.now() - progress_obj.module_start_time).total_seconds()
                progress_obj.total_time_spent_seconds += int(time_spent)
                print(f"⏱️ Topic switch: +{int(time_spent)}s | Total: {progress_obj.total_time_spent_seconds}s")
            
            if topic_id:
                try:
                    topic = Topics.objects.get(id=topic_id)
                    progress_obj.current_topic = topic
                    progress_obj.module_start_time = timezone.now()
                except Topics.DoesNotExist:
                    return JsonResponse({"status": "error", "message": "Topic not found"}, status=404)
            else:
                progress_obj.current_topic = None
                progress_obj.module_start_time = None
            
            progress_obj.save(update_fields=['current_topic', 'last_updated', 'total_time_spent_seconds', 'module_start_time'])
            
            leaderboard_entry = LeaderboardEntry.objects.filter(
                student=request.user, course=course_obj
            ).first()
            new_xp = leaderboard_entry.champion_xp if leaderboard_entry else 0
            new_rank = leaderboard_entry.rank if leaderboard_entry else None
            
            course_specific_topics = Topics.objects.filter(courses=course_obj)
            course_specific_topic_ids = set(course_specific_topics.values_list('id', flat=True))
            
            completed_ids = list(
                progress_obj.completed_topics.filter(id__in=course_specific_topic_ids).values_list('id', flat=True)
            ) if progress_obj else []
            
            # ===== AUTO-CREATE FILE =====
            auto_created_file_id = None
            if topic_id and course_obj:
                course_title_lower = course_obj.title.lower()
                is_programming = 'python' in course_title_lower or 'rust' in course_title_lower
                
                if is_programming:
                    try:
                        new_topic = Topics.objects.get(id=topic_id)
                        file_extension = 'py' if 'python' in course_title_lower else 'rs'
                        
                        import re as re_module
                        safe_title = re_module.sub(r'[^a-zA-Z0-9_\s]', '', new_topic.title)
                        safe_title = safe_title.strip().replace(' ', '_').lower()
                        file_name = f"{safe_title}.{file_extension}"
                        
                        existing_file = File.objects.filter(
                            project=project,
                            name__iexact=file_name
                        ).first()
                        
                        if not existing_file:
                            new_file = File.objects.create(
                                project=project,
                                name=file_name,
                                content=''
                            )
                            auto_created_file_id = new_file.id
                        else:
                            auto_created_file_id = existing_file.id
                    except Exception as e:
                        print(f"⚠️ Failed to auto-create file: {e}")
            
            return JsonResponse({
                "status": "success",
                "message": "Active topic updated",
                "current_topic_id": topic_id,
                "points": len(completed_ids),
                "total_topics": course_specific_topics.count(),
                "rank": new_rank,
                "champion_xp": new_xp,
                "auto_created_file_id": auto_created_file_id,
                "total_time_spent_seconds": progress_obj.total_time_spent_seconds,
            })

        # ================= AI PROMPT (redirected to separate endpoint) =================
        if prompt or ai_action == "build_project":
            return JsonResponse({
                "status": "error", 
                "message": "AI build has been moved to a separate endpoint."
            }, status=400)

        # ================= FILE SAVE =================
        if new_content and new_content != file.content:
            file.content = new_content
            file.save(update_fields=["content"])

        response_table = ""
        if ext in {"csv", "xls", "xlsx"} and file.file:
            try:
                df = pd.read_csv(file.file.path) if ext == "csv" else pd.read_excel(file.file.path)
                if run_table:
                    response_table = df.head(20).to_html(classes="table table-bordered table-sm", index=False)
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)
      
        if is_python and (run_plot or new_content.strip()):
            user_inputs = data.get("user_inputs", [])
            result = run_code(new_content, inputs=user_inputs)
            result["table"] = response_table
            if result["status"] == "error":
                return JsonResponse(result, status=500)
            return JsonResponse(result)

        return JsonResponse({"status": "saved", "message": "✓ File saved successfully"})

    # ================= GET =================
    return render(request, "webprojects/file_detail.html", {
        "file": file,
        "files": files,
        "folders": folders,
        "exts": exts,
        "project": project,
        "is_image": is_image,
        'completed_topic_ids': completed_topic_ids,
        'current_topic_id': current_topic_id,
        "topics": topics,
        "course": course,
        'course_id': course.id if course else None,
        'exam_id': exam.id if exam else None,
        'earned_points': earned_points,
        'total_topics': total_topics,
        'user_rank': user_rank,
        'champion_xp': champion_xp,
    })
  

#working view
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

#     # Fetch the course object by project name
#     try:
#         course = Courses.objects.get(title=file.project.name)
#     except Courses.DoesNotExist:
#         course = None

#     # Find the exam tied to this course, if one exists
#     exam = ExamCourse.objects.filter(course_name=course).first() if course else None

#     # Fetch topics using the course object
#     topics = Topics.objects.filter(courses=course).select_related("courses", "categories") if course else Topics.objects.none()
    
#     # Get or create StudentProgress
#     progress = StudentProgress.objects.filter(
#         student=request.user,
#         course=course
#     ).prefetch_related('completed_topics').order_by('-last_updated').first()

#     # Get only topic IDs that belong to THIS course
#     course_topic_ids = set(topics.values_list('id', flat=True))

#     completed_topic_ids = list(
#         progress.completed_topics.filter(id__in=course_topic_ids).values_list('id', flat=True)
#     ) if progress else []

#     # ===== CALCULATE POINTS =====
#     total_topics = topics.count()
#     earned_points = len(completed_topic_ids)
    
#     # ===== GET CHAMPION XP & RANK ON PAGE LOAD (READ ONLY) =====
#     champion_xp = 0
#     user_rank = None
#     if course:
#         leaderboard_entry = LeaderboardEntry.objects.filter(
#             student=request.user, course=course
#         ).first()
#         if leaderboard_entry:
#             champion_xp = leaderboard_entry.champion_xp
#             user_rank = leaderboard_entry.rank
    
#     # ===== USE STORED CURRENT_TOPIC FROM PROGRESS =====
#     current_topic_id = None
#     current_topic = None
#     if progress and progress.current_topic:
#         current_topic_id = progress.current_topic.id
#         current_topic = progress.current_topic
#     elif topics.exists():
#         completed_ids = set(completed_topic_ids)
#         for topic in topics:
#             if topic.id not in completed_ids:
#                 current_topic_id = topic.id
#                 current_topic = topic
#                 break
#         if not current_topic_id and topics.exists():
#             current_topic = topics.last()
#             current_topic_id = current_topic.id
#         if progress and current_topic_id:
#             try:
#                 progress.current_topic = Topics.objects.get(id=current_topic_id)
#                 progress.save(update_fields=['current_topic'])
#             except Topics.DoesNotExist:
#                 pass

#     # ===== START TIME TRACKING ON PAGE LOAD =====
#     if progress and current_topic_id and not progress.module_start_time:
#         progress.module_start_time = timezone.now()
#         progress.save(update_fields=['module_start_time'])

#     # ================= SIDEBAR EXTENSIONS =================
#     exts = sorted({
#         os.path.splitext(f.name)[1].lstrip(".").lower()
#         for f in files if "." in f.name
#     })

#     IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif")
#     is_image = file.name.lower().endswith(IMAGE_EXTS)

#     # ================= FILE TYPE =================
#     ext = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
#     is_python = ext == "py"

#     # ================= POST =================
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode()) if request.body else {}
#         except json.JSONDecodeError:
#             data = {}

#         new_content = data.get("content", "")
#         run_plot = data.get("run_plot", False)
#         run_table = data.get("run_table", False)
#         prompt = data.get("prompt", "")
#         ai_action = data.get("ai_action", "")
#         topic_id = data.get("topic_id")

#         # ================= SCORE OUTPUT =================
#         if data.get("action") == "score_output":
#             import re
#             student_output = data.get("student_output", "").strip()
#             topic_id = data.get("topic_id")
            
#             if not topic_id:
#                 return JsonResponse({"status": "error", "message": "No topic ID provided"}, status=400)

#             try:
#                 topic = Topics.objects.get(id=topic_id)
#             except Topics.DoesNotExist:
#                 return JsonResponse({"status": "error", "message": "Topic not found"}, status=404)

#             topic_desc = topic.desc or ""
#             topic_title = topic.title or ""
#             expected = topic.expected_output or ""

#             # ===== STRIP HTML AND EXTRACT PLAIN CODE =====
#             from html.parser import HTMLParser

#             class HTMLStripper(HTMLParser):
#                 def __init__(self):
#                     super().__init__()
#                     self.text_parts = []
#                 def handle_data(self, data):
#                     self.text_parts.append(data)
#                 def get_text(self):
#                     return '\n'.join(part.strip() for part in self.text_parts if part.strip())

#             def strip_html(html_text):
#                 stripper = HTMLStripper()
#                 stripper.feed(html_text)
#                 return stripper.get_text()

#             plain_desc = strip_html(topic_desc)
#             print_count_in_desc = plain_desc.count('print(')

#             # ===== CLEAR BAD CACHED EXPECTED OUTPUT =====
#             if expected:
#                 expected_lines = len(expected.strip().splitlines())
#                 if expected_lines < print_count_in_desc:
#                     print(f"⚠️ Cached expected has {expected_lines} lines but code has {print_count_in_desc} prints — regenerating")
#                     expected = ""
#                     topic.expected_output = ""
#                     topic.save(update_fields=['expected_output'])

#             # ===== IF NO EXPECTED OUTPUT, USE AI TO GENERATE IT =====
#             if not expected:
#                 code_blocks = re.findall(r'```python\n(.*?)```', topic_desc, re.DOTALL)
#                 code_content = '\n'.join(code_blocks) if code_blocks else plain_desc

#                 # ===== IMPROVED PROMPT TO HANDLE DETERMINISTIC OUTPUTS =====
#                 expected_prompt = f"""You are a Python code analyzer. Analyze this code and determine what it WILL ALWAYS output when executed.

# ## CODE TO ANALYZE:
# {code_content}

# ## CRITICAL INSTRUCTIONS:
# 1. Execute the code mentally, following ALL logic paths
# 2. Identify ALL print() statements
# 3. For each print(), determine if the output is:
#    - FIXED: Always prints the same thing regardless of any input (e.g., print("Hello"), print(5+3))
#    - CONDITIONAL: Prints based on logic that doesn't depend on user input (e.g., print("Even") if x%2==0)
#    - INPUT_DEPENDENT: Output changes based on user input (e.g., print("Hello " + name), print(age * 2))

# ## DECISION TREE:
# - If the code has ONLY input-dependent prints → return: VARIABLE_OUTPUT
# - If the code has ONLY fixed/conditional prints → return the exact output, one line per print()
# - If the code has a MIX of fixed and input-dependent prints → return only the fixed ones

# ## IMPORTANT RULES FOR CONDITIONALS:
# - If there's an if/else that checks user input (like password check):
#   * print("Access granted.") in if branch AND print("Access denied.") in else branch
#   * You MUST return BOTH possibilities on separate lines:
#     Access granted.
#     Access denied.
# - This counts as CONDITIONAL output, NOT input-dependent

# ## EXAMPLES:

# Example 1 - Simple fixed output:
# Code:
# print("Hello World")
# print(5 + 3)
# Response:
# Hello World
# 8

# Example 2 - Input-dependent (names):
# Code:
# name = input("Enter name: ")
# print("Hello " + name)
# Response:
# VARIABLE_OUTPUT

# Example 3 - Conditional with password check:
# Code:
# password = input("Enter password: ")
# if password == "secret":
#     print("Access granted.")
# else:
#     print("Access denied.")
# Response:
# Access granted.
# Access denied.

# Example 4 - Mixed fixed and input-dependent:
# Code:
# print("Welcome to the system")
# name = input("Enter name: ")
# print("Processing...")
# print("Hello " + name)
# Response:
# Welcome to the system
# Processing...

# Example 5 - Math with fixed values:
# Code:
# x = 10
# y = 20
# print(x + y)
# Response:
# 30

# Example 6 - Simple conditional (not input-dependent):
# Code:
# age = 18
# if age >= 18:
#     print("Adult")
# else:
#     print("Minor")
# Response:
# Adult

# Example 7 - Password check with multiple attempts:
# Code:
# password = input("Enter password: ")
# if password == "admin123":
#     print("Login successful")
#     print("Welcome admin")
# else:
#     print("Login failed")
#     print("Try again")
# Response:
# Login successful
# Welcome admin
# Login failed
# Try again

# Return ONLY the output lines (or VARIABLE_OUTPUT), nothing else. No markdown, no explanation, no labels."""
                
#                 try:
#                     if client is None:
#                         return JsonResponse({"status": "error", "message": "OpenAI API is not configured"}, status=500)
                    
#                     expected_response = client.chat.completions.create(
#                         model="gpt-4o-mini",
#                         messages=[
#                             {"role": "system", "content": "You are a Python code analyzer. Determine the exact output or return VARIABLE_OUTPUT. Be thorough with conditional logic - include outputs from ALL branches."},
#                             {"role": "user", "content": expected_prompt},
#                         ],
#                         max_tokens=300,
#                         temperature=0,
#                     )
#                     expected = expected_response.choices[0].message.content.strip()
#                     expected = re.sub(r'^(output|result|answer)\s*:\s*', '', expected, flags=re.IGNORECASE).strip()
#                     print(f"🤖 AI Generated Expected Output: '{expected}'")
                    
#                     topic.expected_output = expected
#                     topic.save(update_fields=['expected_output'])
#                 except Exception as e:
#                     print(f"⚠️ Failed to generate expected output: {e}")
#                     expected = ""

#             # ===== INITIALIZE ALL VARIABLES BEFORE CONDITIONAL BLOCKS =====
#             # Get or create progress
#             if not progress:
#                 progress, _ = StudentProgress.objects.get_or_create(
#                     student=request.user, course=course
#                 )
            
#             # Initialize defaults
#             new_rank = user_rank
#             new_xp = champion_xp
#             xp_earned = 0
#             already_awarded = progress.completed_topics.filter(id=topic_id).exists()
#             earned_points = progress.completed_topics.filter(id__in=course_topic_ids).count()
#             display_score = earned_points

#             # ===== ONLY MARK AS VARIABLE_OUTPUT IF TRULY INPUT-DEPENDENT =====
#             if expected == "VARIABLE_OUTPUT" or not expected:
#                 # Cannot score this topic automatically — mark as correct if code ran without error
#                 return JsonResponse({
#                     "status": "success",
#                     "result": {
#                         "score": display_score,
#                         "max_score": total_topics,
#                         "feedback": "✅ Code ran successfully! Output varies by input — marked as complete.",
#                         "correct": True
#                     },
#                     "points": earned_points,
#                     "total_topics": total_topics,
#                     "rank": new_rank,
#                     "champion_xp": new_xp,
#                     "xp_earned": xp_earned,
#                     "already_awarded": already_awarded,
#                     "average_score": progress.get_average_score() if progress else 0,
#                     "modules_completed": min(earned_points, total_topics),
#                     "expected_output": "VARIABLE_OUTPUT",
#                 })

#             # ===== SCORE WITH AI - IMPROVED TO HANDLE CONDITIONAL OUTPUTS =====
#             scoring_prompt = f"""You are a Python output checker. Compare the student's output against the expected output.

# EXPECTED OUTPUT (may have multiple possible correct answers from conditional branches):
# ---
# {expected}
# ---

# STUDENT'S ACTUAL OUTPUT:
# ---
# {student_output}
# ---

# ## SCORING RULES:
# 1. FIRST: Clean both outputs:
#    - Remove ALL input prompts (lines containing "Enter", "Type", "Input" etc.)
#    - Remove empty lines
#    - Strip whitespace from each line
   
# 2. If expected has MULTIPLE possible outputs (like "Access granted." and "Access denied."):
#    - Student's output must match EXACTLY ONE of the possibilities
#    - score = 1 if it matches any option, else score = 0

# 3. If expected has SINGLE output:
#    - Student's output must contain the expected output (exact match per line)
#    - Extra lines are OK
#    - score = 1 if all expected lines match, else score = 0

# 4. Be strict about whitespace but flexible about case if it makes sense

# ## EXAMPLES:

# Expected:
# Access granted.
# Access denied.

# Student output:
# Enter your password: secret
# Access granted.
# → score: 1 (matches "Access granted.")

# Expected:
# Access granted.
# Access denied.

# Student output:
# Enter your password: wrong
# Access denied.
# → score: 1 (matches "Access denied.")

# Expected:
# Welcome to the system
# Processing...

# Student output:
# Welcome to the system
# Enter name: John
# Processing...
# Hello John
# → score: 1 (both expected lines present)

# Return ONLY valid JSON:
# {{"score": 0, "max_score": 1, "feedback": "reason here", "correct": false}}"""
            
#             try:
#                 if client is None:
#                     return JsonResponse({"status": "error", "message": "OpenAI API is not configured"}, status=500)
                    
#                 response = client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[
#                         {"role": "system", "content": "You are a strict but fair Python output checker. Handle conditional outputs correctly - check if student's output matches any valid branch."},
#                         {"role": "user", "content": scoring_prompt},
#                     ],
#                     max_tokens=300,
#                     temperature=0,
#                     response_format={"type": "json_object"}
#                 )
#                 result = json.loads(response.choices[0].message.content)
                
#                 xp_before = champion_xp
                
#                 # ===== TIME TRACKING: Record time when code is scored =====
#                 if progress.module_start_time:
#                     time_spent = (timezone.now() - progress.module_start_time).total_seconds()
#                     progress.total_time_spent_seconds += int(time_spent)
#                     progress.module_start_time = timezone.now()  # Reset timer
#                     progress.save(update_fields=['total_time_spent_seconds', 'module_start_time'])
#                     print(f"⏱️ Scored: +{int(time_spent)}s | Total: {progress.total_time_spent_seconds}s")
                
#                 if result.get('correct', False):
#                     if not already_awarded:
#                         progress.completed_topics.add(topic)
#                         progress.add_assessment_score(100, topic_id, first_attempt=True)
                        
#                         earned_points = progress.completed_topics.filter(id__in=course_topic_ids).count()
#                         display_score = earned_points
                        
#                         try:
#                             update_streak(request.user, course)
#                             entry = update_leaderboard_entry(request.user, course)
#                             check_badges(request.user, course, progress)
                            
#                             if entry:
#                                 new_rank = entry.rank
#                                 new_xp = entry.champion_xp
#                                 xp_earned = new_xp - xp_before
#                                 print(f"🏆 Topic {topic_id} completed! XP: {new_xp} (+{xp_earned}), Rank: #{new_rank}")
#                         except Exception as e:
#                             print(f"⚠️ Failed to update leaderboard: {e}")
#                     else:
#                         # Already awarded - keep existing values
#                         display_score = earned_points
#                         xp_earned = 0
#                         result['feedback'] = (result.get('feedback', '') + 
#                             '\n\n📌 Module already completed - no additional XP.')
#                 else:
#                     # Incorrect answer
#                     progress.incorrect_code_attempts += 1
#                     progress.save(update_fields=['incorrect_code_attempts'])
#                     display_score = earned_points
                
#                 return JsonResponse({
#                     "status": "success",
#                     "result": {
#                         "score": display_score,
#                         "max_score": total_topics,
#                         "feedback": result.get('feedback', ''),
#                         "correct": result.get('correct', False)
#                     },
#                     "points": earned_points,
#                     "total_topics": total_topics,
#                     "rank": new_rank,
#                     "champion_xp": new_xp,
#                     "xp_earned": xp_earned,
#                     "already_awarded": already_awarded,
#                     "average_score": progress.get_average_score() if progress else 0,
#                     "modules_completed": min(earned_points, total_topics),
#                     "expected_output": expected,
#                     "total_time_spent_seconds": progress.total_time_spent_seconds,
#                 })
#             except Exception as e:
#                 return JsonResponse({"status": "error", "message": str(e)}, status=500)

#         # ================= UPDATE ACTIVE TOPIC =================
#         if data.get("action") == "update_active_topic":
#             topic_id = data.get("topic_id")
#             course_id = data.get("course_id")
            
#             if not course_id:
#                 return JsonResponse({"status": "error", "message": "Course ID is required"}, status=400)
            
#             try:
#                 course_obj = Courses.objects.get(id=course_id)
#             except Courses.DoesNotExist:
#                 return JsonResponse({"status": "error", "message": "Course not found"}, status=404)
            
#             progress_obj, _ = StudentProgress.objects.get_or_create(
#                 student=request.user, course=course_obj
#             )
            
#             # ===== TIME TRACKING: Record time spent on previous topic =====
#             if progress_obj.module_start_time:
#                 time_spent = (timezone.now() - progress_obj.module_start_time).total_seconds()
#                 progress_obj.total_time_spent_seconds += int(time_spent)
#                 print(f"⏱️ Topic switch: +{int(time_spent)}s | Total: {progress_obj.total_time_spent_seconds}s")
            
#             if topic_id:
#                 try:
#                     topic = Topics.objects.get(id=topic_id)
#                     progress_obj.current_topic = topic
#                     progress_obj.module_start_time = timezone.now()  # Start timer for new topic
#                 except Topics.DoesNotExist:
#                     return JsonResponse({"status": "error", "message": "Topic not found"}, status=404)
#             else:
#                 progress_obj.current_topic = None
#                 progress_obj.module_start_time = None  # Stop timer
            
#             progress_obj.save(update_fields=['current_topic', 'last_updated', 'total_time_spent_seconds', 'module_start_time'])
            
#             leaderboard_entry = LeaderboardEntry.objects.filter(
#                 student=request.user, course=course_obj
#             ).first()
#             new_xp = leaderboard_entry.champion_xp if leaderboard_entry else 0
#             new_rank = leaderboard_entry.rank if leaderboard_entry else None
            
#             # Get course topic IDs for the specific course
#             course_specific_topics = Topics.objects.filter(courses=course_obj)
#             course_specific_topic_ids = set(course_specific_topics.values_list('id', flat=True))
            
#             completed_ids = list(
#                 progress_obj.completed_topics.filter(id__in=course_specific_topic_ids).values_list('id', flat=True)
#             ) if progress_obj else []
            
#             # ===== AUTO-CREATE FILE =====
#             auto_created_file_id = None
#             if topic_id and course_obj:
#                 course_title_lower = course_obj.title.lower()
#                 is_programming = 'python' in course_title_lower or 'rust' in course_title_lower
                
#                 if is_programming:
#                     try:
#                         new_topic = Topics.objects.get(id=topic_id)
#                         file_extension = 'py' if 'python' in course_title_lower else 'rs'
                        
#                         import re as re_module
#                         safe_title = re_module.sub(r'[^a-zA-Z0-9_\s]', '', new_topic.title)
#                         safe_title = safe_title.strip().replace(' ', '_').lower()
#                         file_name = f"{safe_title}.{file_extension}"
                        
#                         existing_file = File.objects.filter(
#                             project=project,
#                             name__iexact=file_name
#                         ).first()
                        
#                         if not existing_file:
#                             new_file = File.objects.create(
#                                 project=project,
#                                 name=file_name,
#                                 content=''
#                             )
#                             auto_created_file_id = new_file.id
#                         else:
#                             auto_created_file_id = existing_file.id
#                     except Exception as e:
#                         print(f"⚠️ Failed to auto-create file: {e}")
            
#             return JsonResponse({
#                 "status": "success",
#                 "message": "Active topic updated",
#                 "current_topic_id": topic_id,
#                 "points": len(completed_ids),
#                 "total_topics": course_specific_topics.count(),
#                 "rank": new_rank,
#                 "champion_xp": new_xp,
#                 "auto_created_file_id": auto_created_file_id,
#                 "total_time_spent_seconds": progress_obj.total_time_spent_seconds,
#             })

        
#         # ================= AI PROMPT =================
#         if prompt or ai_action == "build_project":
#             if client is None:
#                 return JsonResponse({"status": "error", "message": "🔑 OpenAI API is not configured."}, status=500)

#             try:
#                 with transaction.atomic():
#                     html_file, _ = File.objects.get_or_create(
#                         project=project, name="index.html",
#                         defaults={"content": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Project</title>\n    <link rel='stylesheet' href='style.css'>\n</head>\n<body>\n    <script src='script.js'></script>\n</body>\n</html>"}
#                     )
#                     css_file, _ = File.objects.get_or_create(
#                         project=project, name="style.css",
#                         defaults={"content": "/* Your styles here */\n"}
#                     )
#                     js_file, _ = File.objects.get_or_create(
#                         project=project, name="script.js",
#                         defaults={"content": "// Your JavaScript here\n"}
#                     )

#                     system_message = """You are an elite UI/UX engineer who builds stunning, modern web applications.

# ## DESIGN PHILOSOPHY
# - Clean whitespace, strong visual hierarchy, consistent 8px grid
# - Subtle depth with shadows, smooth 200ms transitions
# - Mobile-first, fully responsive

# ## VISUAL DEFAULTS
# - Font: Inter/system-ui, Primary: #6366f1, hover: #4f46e5
# - Light bg: #fff/#f9fafb, Dark bg: #0f172a
# - Text: #0f172a primary, #64748b secondary
# - Border: #e2e8f0, radius: 8px cards, 6px buttons

# ## CSS RULES
# - CSS variables at :root, Flexbox/Grid layouts
# - transition: all 0.2s ease on interactive elements
# - :hover/:focus states, box-sizing: border-box
# - NO inline styles

# ## COMPONENTS
# Button: bg #6366f1, padding 10px 20px, radius 6px, font 600 15px
# Card: bg #fff, radius 12px, padding 24px, hover lift
# Input: full width, padding 10px 14px, focus ring #6366f1

# ## HTML
# - Semantic tags, lang="en", viewport meta, charset UTF-8
# - Alt text, aria-labels, CSS in head, JS before /body

# ## JS
# - Vanilla ES6+, DOMContentLoaded, CSS class toggling
# - Loading/error states

# ## PAGE STRUCTURE
# - Sticky nav, Hero with CTA, Content grid, Footer
# - 80px sections, max-width 1200px, mobile <768px single column

# ## RESPONSE
# Return ONLY: {"html": "...", "css": "...", "js": "..."}
# No markdown, raw JSON only."""

#                     user_message = f"""Current Files:
# HTML: {html_file.content[:300] if html_file.content.strip() else "Empty"}
# CSS: {css_file.content[:200] if css_file.content.strip() else "Empty"}
# JS: {js_file.content[:200] if js_file.content.strip() else "Empty"}

# Request: {prompt}

# Return ONLY JSON: {{"html": "...", "css": "...", "js": "..."}}"""

#                     response = client.chat.completions.create(
#                         model="gpt-4o-mini",
#                         messages=[
#                             {"role": "system", "content": system_message},
#                             {"role": "user", "content": user_message},
#                         ],
#                         max_tokens=6000,
#                         temperature=0.4,
#                         response_format={"type": "json_object"}
#                     )
#                     ai_text = response.choices[0].message.content.strip()
#                     print(f"✅ AI Response received: {len(ai_text)} chars")

#                     try:
#                         ai_generated = json.loads(ai_text)
#                     except json.JSONDecodeError:
#                         start = ai_text.find("{")
#                         end = ai_text.rfind("}") + 1
#                         if start != -1 and end > start:
#                             try:
#                                 ai_generated = json.loads(ai_text[start:end])
#                             except json.JSONDecodeError:
#                                 return JsonResponse({"status": "error", "message": "Failed to parse AI response"}, status=500)
#                         else:
#                             return JsonResponse({"status": "error", "message": "No valid JSON in response"}, status=500)

#                     if not isinstance(ai_generated, dict) or not any(k in ai_generated for k in ["html", "css", "js"]):
#                         return JsonResponse({"status": "error", "message": "Invalid response format"}, status=500)
                    
#                     updates_made = []
#                     for key, file_obj in [("html", html_file), ("css", css_file), ("js", js_file)]:
#                         if key in ai_generated and ai_generated[key].strip():
#                             content = ai_generated[key].strip()
#                             if key == "html" and not content.startswith("<!DOCTYPE"):
#                                 content = f"<!DOCTYPE html>\n{content}"
#                             file_obj.content = content
#                             file_obj.save(update_fields=["content"])
#                             updates_made.append(key.upper())

#                     if not updates_made:
#                         return JsonResponse({"status": "warning", "message": "No files updated"}, status=200)

#                     return JsonResponse({
#                         "status": "success",
#                         "ai_content": ai_generated,
#                         "message": f"✨ Updated: {', '.join(updates_made)}",
#                         "files_updated": updates_made,
#                     })

#             except Exception as e:
#                 print(f"❌ AI Error: {traceback.format_exc()}")
#                 return JsonResponse({"status": "error", "message": str(e)}, status=500)
            

#         # ================= FILE SAVE =================
#         if new_content and new_content != file.content:
#             file.content = new_content
#             file.save(update_fields=["content"])

#         response_table = ""
#         if ext in {"csv", "xls", "xlsx"} and file.file:
#             try:
#                 df = pd.read_csv(file.file.path) if ext == "csv" else pd.read_excel(file.file.path)
#                 if run_table:
#                     response_table = df.head(20).to_html(classes="table table-bordered table-sm", index=False)
#             except Exception as e:
#                 return JsonResponse({"status": "error", "message": str(e)}, status=400)
      
#         if is_python and (run_plot or new_content.strip()):
#             user_inputs = data.get("user_inputs", [])
#             result = run_code(new_content, inputs=user_inputs)
#             result["table"] = response_table
#             if result["status"] == "error":
#                 return JsonResponse(result, status=500)
#             return JsonResponse(result)

#         return JsonResponse({"status": "saved", "message": "✓ File saved successfully"})

#     # ================= GET =================
#     return render(request, "webprojects/file_detail.html", {
#         "file": file,
#         "files": files,
#         "folders": folders,
#         "exts": exts,
#         "project": project,
#         "is_image": is_image,
#         'completed_topic_ids': completed_topic_ids,
#         'current_topic_id': current_topic_id,
#         "topics": topics,
#         "course": course,
#         'course_id': course.id if course else None,
#         'exam_id': exam.id if exam else None,
#         'earned_points': earned_points,
#         'total_topics': total_topics,
#         'user_rank': user_rank,
#         'champion_xp': champion_xp,
#     })



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg, F, Window
from django.db.models.functions import Rank
from .models import LeaderboardEntry, StudentProgress
from sms.models import Courses, Topics


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Window, F, Sum, Avg, Count
from django.db.models.functions import Rank
from django.utils import timezone
from datetime import timedelta
from .models import LeaderboardEntry, StudentProgress, StudentXP, Badge, StudentBadge, LearningStreak
from sms.models import Courses, Topics


# ============================================
# XP CALCULATION HELPERS
# ============================================
def calculate_champion_xp(progress, total_topics):
    """Calculate Champion XP for a student"""
    xp = 0
    
    # Get course-specific topic IDs
    course_topic_ids = set(
        Topics.objects.filter(courses=progress.course).values_list('id', flat=True)
    )
    
    # Module completion: +10 XP per module (capped at total_topics)
    completed = min(
        progress.completed_topics.filter(id__in=course_topic_ids).count(), 
        total_topics
    )
    xp += completed * 10
    
    # Assessment performance XP - ONLY count unique topics (no duplicates)
    # Only count assessment scores up to the number of completed topics
    # This prevents duplicate scores from inflating XP
    completed_topic_ids = list(
        progress.completed_topics.filter(id__in=course_topic_ids).values_list('id', flat=True)
    )
    
    unique_scores = progress.assessment_scores[:len(completed_topic_ids)] if len(progress.assessment_scores) > len(completed_topic_ids) else progress.assessment_scores
    
    for score in unique_scores:
        if score >= 90:
            xp += 10  # Perfect score bonus
        elif score >= 80:
            xp += 8
        elif score >= 70:
            xp += 6
        elif score >= 60:
            xp += 4
    
    # Coding challenges: +5 XP each (capped at total_topics)
    # Only count coding challenges that match actual completed topics
    coding_xp = min(progress.coding_challenges_passed, completed) * 5
    xp += coding_xp
    
    # Course completion: +100 XP (only if all modules completed)
    if progress.course_completed and completed >= total_topics:
        xp += 100
    
    # First attempt bonuses: +5 XP each (capped at completed topics)
    # Only count first attempts for actually completed topics
    first_attempt_count = min(len(progress.first_attempt_topics), completed)
    xp += first_attempt_count * 5
    
    # Learning streak XP (only count the highest tier achieved)
    if progress.current_streak >= 30:
        xp += 50
    elif progress.current_streak >= 14:
        xp += 30
    elif progress.current_streak >= 7:
        xp += 15
    elif progress.current_streak >= 3:
        xp += 5
    # No XP for streaks less than 3 days
    
    # Add logging for debugging
    print(f"""
    📊 XP Breakdown for {progress.student.username}:
    ├─ Modules ({completed}×10): {completed * 10}
    ├─ Assessment Scores: {sum(10 if s >= 90 else 8 if s >= 80 else 6 if s >= 70 else 4 for s in unique_scores)}
    ├─ Coding Challenges ({min(progress.coding_challenges_passed, completed)}×5): {coding_xp}
    ├─ First Attempts ({first_attempt_count}×5): {first_attempt_count * 5}
    ├─ Streak Bonus (streak={progress.current_streak}): {50 if progress.current_streak >= 30 else 30 if progress.current_streak >= 14 else 15 if progress.current_streak >= 7 else 5 if progress.current_streak >= 3 else 0}
    └─ Total XP: {xp}
    """)
    
    return xp


def update_streak(student, course):
    """Update learning streak for a student"""
    today = timezone.now().date()
    
    # Record today's activity
    LearningStreak.objects.get_or_create(
        student=student,
        course=course,
        date=today
    )
    
    # Get or create progress
    progress, _ = StudentProgress.objects.get_or_create(
        student=student,
        course=course
    )
    
    # Calculate current streak
    streak_dates = LearningStreak.objects.filter(
        student=student,
        course=course
    ).values_list('date', flat=True).order_by('-date')
    
    current_streak = 0
    if streak_dates:
        current_streak = 1
        for i in range(1, len(streak_dates)):
            if streak_dates[i-1] - streak_dates[i] == timedelta(days=1):
                current_streak += 1
            else:
                break
    
    progress.current_streak = current_streak
    if current_streak > progress.longest_streak:
        progress.longest_streak = current_streak
    progress.last_activity_date = today
    progress.save(update_fields=['current_streak', 'longest_streak', 'last_activity_date'])
    
    return current_streak


def check_badges(student, course, progress):
    """Check and award badges"""
    total_topics = Topics.objects.filter(courses=course).count()
    
    badges_awarded = []
    
    # First to Finish
    if progress.course_completed and progress.first_to_complete:
        badge, _ = Badge.objects.get_or_create(
            name='first_to_finish',
            defaults={'description': 'First student to complete the course', 'icon': '🥇', 'xp_reward': 50}
        )
        _, created = StudentBadge.objects.get_or_create(student=student, badge=badge, course=course)
        if created:
            badges_awarded.append(badge)
    
    # Fast Learner - completed within 7 days
    if progress.course_completed and progress.completion_date:
        first_activity = LearningStreak.objects.filter(
            student=student, course=course
        ).order_by('date').first()
        if first_activity:
            days = (progress.completion_date.date() - first_activity.date).days
            if days <= 7:
                badge, _ = Badge.objects.get_or_create(
                    name='fast_learner',
                    defaults={'description': 'Completed course within 7 days', 'icon': '⚡', 'xp_reward': 30}
                )
                _, created = StudentBadge.objects.get_or_create(student=student, badge=badge, course=course)
                if created:
                    badges_awarded.append(badge)
    
    # Perfect Score - average >= 90%
    if progress.get_average_score() >= 90 and progress.total_assessments_taken > 0:
        badge, _ = Badge.objects.get_or_create(
            name='perfect_score',
            defaults={'description': 'Average assessment score ≥ 90%', 'icon': '🎯', 'xp_reward': 40}
        )
        _, created = StudentBadge.objects.get_or_create(student=student, badge=badge, course=course)
        if created:
            badges_awarded.append(badge)
    
    # Code Master - passed all coding challenges
    if progress.coding_challenges_passed >= total_topics and total_topics > 0:
        badge, _ = Badge.objects.get_or_create(
            name='code_master',
            defaults={'description': 'Passed every coding challenge', 'icon': '💻', 'xp_reward': 40}
        )
        _, created = StudentBadge.objects.get_or_create(student=student, badge=badge, course=course)
        if created:
            badges_awarded.append(badge)
    
    # AI Champion - passed all assessments on first attempt
    if len(progress.first_attempt_topics) >= progress.total_assessments_taken and progress.total_assessments_taken > 0:
        badge, _ = Badge.objects.get_or_create(
            name='ai_champion',
            defaults={'description': 'Passed every AI assessment on first attempt', 'icon': '🧠', 'xp_reward': 50}
        )
        _, created = StudentBadge.objects.get_or_create(student=student, badge=badge, course=course)
        if created:
            badges_awarded.append(badge)
    
    # Consistent Learner - 7-day streak
    if progress.current_streak >= 7:
        badge, _ = Badge.objects.get_or_create(
            name='consistent',
            defaults={'description': 'Maintained a 7-day learning streak', 'icon': '🔥', 'xp_reward': 25}
        )
        _, created = StudentBadge.objects.get_or_create(student=student, badge=badge, course=course)
        if created:
            badges_awarded.append(badge)
    
    return badges_awarded

def get_motivation_message(entry, progress, total_students):
    """Generate motivation messages"""
    if not entry:
        return []
    
    messages = []
    
    # Near top 20
    if entry.rank and entry.rank > 20 and entry.rank <= 25:
        modules_needed = max(1, (entry.total_modules - entry.modules_completed))
        messages.append(f"🚀 Complete {modules_needed} more module(s) to enter the Top 20!")
    
    # Close to overtaking
    next_entry = LeaderboardEntry.objects.filter(
        course=entry.course,
        rank__lt=entry.rank
    ).order_by('-rank').first()
    
    if next_entry:
        xp_needed = next_entry.champion_xp - entry.champion_xp
        if xp_needed <= 20 and xp_needed > 0:
            name = next_entry.student.get_full_name() or next_entry.student.username
            messages.append(f"🎯 Earn {xp_needed} more XP to overtake {name}!")
    
    # Assessment motivation - only if not already at 100%
    if progress and progress.get_average_score() < 100 and progress.total_assessments_taken > 0:
        messages.append(f"🎯 Aim for 100% in your next assessment for bonus XP!")
    
    # Coding challenge motivation - only if there are remaining modules
    if entry.total_modules > 0 and entry.coding_challenges_passed < entry.total_modules:
        needed = entry.total_modules - entry.coding_challenges_passed
        messages.append(f"💻 Solve {needed} more coding challenge(s) for +{needed * 5} XP!")
    
    # Streak motivation
    if progress:
        if progress.current_streak > 0:
            messages.append(f"🔥 Keep your streak alive tomorrow! ({progress.current_streak} days)")
        else:
            messages.append("🔥 Start a learning streak by completing a module today!")
    
    # Course completed - celebration message
    if entry.modules_completed >= entry.total_modules and entry.total_modules > 0:
        messages.insert(0, f"🎉 Congratulations! You've completed all {entry.total_modules} modules!")
    
    return messages[:3]  # Limit to 3 messages


def update_leaderboard_entry(student, course):
    """Update a single student's leaderboard entry"""
    total_topics = Topics.objects.filter(courses=course).count()
    progress = StudentProgress.objects.filter(student=student, course=course).first()
    
    if not progress:
        return None
    
    xp = calculate_champion_xp(progress, total_topics)
    
    # Calculate completion time in a human-readable format
    completion_time_display = None
    if progress.total_time_spent_seconds > 0:
        total_seconds = progress.total_time_spent_seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            completion_time_display = f"{hours}h {minutes}m"
        elif minutes > 0:
            completion_time_display = f"{minutes}m {seconds}s"
        else:
            completion_time_display = f"{seconds}s"
    
    # Use total_time_spent_seconds for ranking (stored as integer days for now, 
    # but we can change to store seconds directly)
    # Store seconds directly for precise ranking
    completion_time_seconds = progress.total_time_spent_seconds if progress.total_time_spent_seconds > 0 else None
    
    entry, created = LeaderboardEntry.objects.update_or_create(
        student=student,
        course=course,
        defaults={
            'champion_xp': xp,
            'modules_completed': min(progress.completed_topics.filter(courses=course).count(), total_topics),
            'total_modules': total_topics,
            'average_score': progress.get_average_score(),
            'coding_challenges_passed': progress.coding_challenges_passed,
            'incorrect_code_attempts': progress.incorrect_code_attempts,
            'completion_time_days': completion_time_seconds,  # Store seconds here
            'completion_date': progress.completion_date,
            'learning_streak': progress.current_streak,
        }
    )
    
    # Update ranks
    entry.update_rank()
    
    return entry


# ============================================
# VIEWS
# ============================================
@login_required
def course_leaderboard(request, course_id):
    """Display the leaderboard for a specific course"""
    course = get_object_or_404(Courses, id=course_id)
    total_topics = Topics.objects.filter(courses=course).count()
    
    # Update current user's entry first
    update_leaderboard_entry(request.user, course)
    
    # Check badges
    progress = StudentProgress.objects.filter(student=request.user, course=course).first()
    if progress:
        check_badges(request.user, course, progress)
        update_streak(request.user, course)
    
    # Get all entries
    leaderboard_entries = LeaderboardEntry.objects.filter(
        course=course
    ).select_related('student', 'student__profile').order_by('rank')
    
    # Fix entries with total_modules = 0
    for entry in leaderboard_entries:
        if entry.total_modules == 0 or entry.total_modules != total_topics:
            entry.total_modules = total_topics
            entry.save(update_fields=['total_modules'])
    
    total_students = leaderboard_entries.count()
    
    # Current user
    user_entry = leaderboard_entries.filter(student=request.user).first()
    user_rank = user_entry.rank if user_entry else None
    user_badges = StudentBadge.objects.filter(student=request.user, course=course).select_related('badge')
    
    # Motivation messages
    motivation_messages = get_motivation_message(user_entry, progress, total_students) if user_entry else []
    
    # All entries
    all_entries = list(leaderboard_entries)
    
    # Top performers - all with top 3 distinct ranks
    distinct_top_ranks = sorted(set(e.rank for e in all_entries if e.rank))[:3]
    top_performers = [e for e in all_entries if e.rank in distinct_top_ranks]
    if len(top_performers) > 5:
        top_performers = top_performers[:5]
    
    # ===== GET SMART COURSE RECOMMENDATIONS =====
        # ===== GET SMART COURSE RECOMMENDATIONS =====
    recommended_courses = []
    if user_entry and user_entry.modules_completed >= user_entry.total_modules and user_entry.total_modules > 0:
        # Get courses the student has already completed
        completed_course_ids = list(StudentProgress.objects.filter(
            student=request.user,
            course_completed=True
        ).values_list('course_id', flat=True))
        completed_course_ids.append(course.id)
        
        course_title_lower = course.title.lower()
        
        # Determine the primary language/technology of the completed course
        primary_tech = None
        tech_keywords = {
            'python': ['python', 'py'],
            'rust': ['rust', 'rs'],
            'javascript': ['javascript', 'js', 'node'],
            'html/css': ['html', 'css', 'web design'],
            'java': ['java'],
            'data science': ['data', 'pandas', 'numpy', 'machine learning', 'ai'],
        }
        
        for tech, keywords in tech_keywords.items():
            if any(kw in course_title_lower for kw in keywords):
                primary_tech = tech
                break
        
        if primary_tech:
            tech_keywords_list = tech_keywords.get(primary_tech, [])
            query = Q()
            for keyword in tech_keywords_list:
                query |= Q(title__icontains=keyword)
            
            # Get similar courses ordered by most recently created
            similar_courses = Courses.objects.filter(
                query
            ).exclude(
                id__in=completed_course_ids
            ).annotate(
                topic_count=Count('topics')
            ).distinct().order_by('-created', 'title')[:4]  # ORDER BY NEWEST FIRST
            
            recommended_courses = list(similar_courses)
            
            # If not enough, look for next level/related courses (also ordered by date)
            if len(recommended_courses) < 4:
                level_keywords = ['level 2', 'level 3', 'advanced', 'project', 'master', 'expert']
                for lk in level_keywords:
                    if len(recommended_courses) >= 4:
                        break
                    more_courses = Courses.objects.filter(
                        Q(title__icontains=tech_keywords_list[0]) & Q(title__icontains=lk)
                    ).exclude(
                        id__in=completed_course_ids + [c.id for c in recommended_courses]
                    ).annotate(
                        topic_count=Count('topics')
                    ).order_by('-created')[:4 - len(recommended_courses)]
                    recommended_courses.extend(list(more_courses))
            
            # If still not enough, get remaining same-tech courses
            if len(recommended_courses) < 4:
                remaining = Courses.objects.filter(
                    Q(title__icontains=tech_keywords_list[0])
                ).exclude(
                    id__in=completed_course_ids + [c.id for c in recommended_courses]
                ).annotate(
                    topic_count=Count('topics')
                ).order_by('-created')[:4 - len(recommended_courses)]
                recommended_courses.extend(list(remaining))
        
        # Fallback: newest courses available
        if not recommended_courses:
            recommended_courses = list(Courses.objects.exclude(
                id__in=completed_course_ids
            ).annotate(
                topic_count=Count('topics')
            ).order_by('-created')[:4])  # NEWEST FIRST
    
    context = {
        'course': course,
        'all_entries': all_entries,
        'top_performers': top_performers,
        'user_entry': user_entry,
        'user_rank': user_rank,
        'user_progress': progress,
        'user_badges': user_badges,
        'motivation_messages': motivation_messages,
        'total_students': total_students,
        'total_topics': total_topics,
        'recommended_courses': recommended_courses,
    }
    
    return render(request, 'webprojects/leaderboard.html', context)


@login_required
def start_course(request, course_id):
    """Start a new course - creates project and redirects to editor"""
    course = get_object_or_404(Courses, id=course_id)
    
    # Check if student already has a project for this course
    existing_project = Project.objects.filter(
        user=request.user,
        name=course.title
    ).first()
    
    if existing_project:
        # Get the first code file or create one
        first_file = File.objects.filter(project=existing_project).first()
        if first_file:
            return redirect('webprojects:file_detail', project_id=existing_project.id, file_id=first_file.id)
    
    # Create new project for this course
    project = Project.objects.create(
        user=request.user,
        name=course.title
    )
    
    # Create a default Python file
    is_python = 'python' in course.title.lower()
    is_rust = 'rust' in course.title.lower()
    
    if is_python:
        file_name = 'main.py'
        content = ''
    elif is_rust:
        file_name = 'main.rs'
        content = ''
    else:
        file_name = 'index.html'
        content = '<!DOCTYPE html>\n<html>\n<head>\n    <title>Project</title>\n</head>\n<body>\n\n</body>\n</html>'
    
    new_file = File.objects.create(
        project=project,
        name=file_name,
        content=content
    )
    
    return redirect('webprojects:file_detail', project_id=project.id, file_id=new_file.id)



@login_required
def update_leaderboard(request, course_id):
    """API endpoint to update leaderboard"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    course = get_object_or_404(Courses, id=course_id)
    
    # Update streak
    current_streak = update_streak(request.user, course)
    
    # Update entry
    entry = update_leaderboard_entry(request.user, course)
    
    if not entry:
        return JsonResponse({'error': 'No progress found'}, status=404)
    
    # Check badges
    progress = StudentProgress.objects.get(student=request.user, course=course)
    new_badges = check_badges(request.user, course, progress)
    
    # Motivation messages
    total_students = LeaderboardEntry.objects.filter(course=course).count()
    motivation = get_motivation_message(entry, progress, total_students)
    
    return JsonResponse({
        'status': 'success',
        'champion_xp': entry.champion_xp,
        'rank': entry.rank,
        'total_students': total_students,
        'average_score': entry.average_score,
        'modules_completed': entry.modules_completed,
        'total_modules': entry.total_modules,
        'coding_challenges_passed': entry.coding_challenges_passed,
        'incorrect_code_attempts': entry.incorrect_code_attempts,
        'learning_streak': entry.learning_streak,
        'completion_time_days': entry.completion_time_days,
        'new_badges': [b.get_name_display() for b in new_badges] if new_badges else [],
        'motivation_messages': motivation,
    })


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
                folder=folder,
                created_by=request.user
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
       

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
  # make sure this import is correct


@csrf_exempt
def run_python_code(request):

    xp_data = award_xp(request.user, 10) if request.user.is_authenticated else {}
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
        

    try:
        data = json.loads(request.body)
        code = data.get("code", "")
        inputs = data.get("inputs", [])  # 👈 IMPORTANT

        result = run_code(code, inputs)  # 👈 Pass inputs here

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "output": "",
            "error": str(e),
            "images": [],
            'xp': xp_data,
            "message": "Server error"
        }, status=500)
    

# views.py

from sms.models import CompletedTopics
from openai import OpenAI
import os, json
# Add these imports at the top of your views.py if not already present:
import re
import os
import sys
import subprocess
import tempfile

def get_student_courses(request):
    from sms.models import Courses, StudentProgress
    
    try:
        courses = Courses.objects.filter(is_programming=True)
        result = []
        
        for course in courses:
            total_topics = course.topics.count()
            
            try:
                progress = StudentProgress.objects.get(
                    student=request.user,
                    course=course
                )
                completed = progress.completed_topics.count()
            except StudentProgress.DoesNotExist:
                completed = 0
            
            pct = round((completed / total_topics) * 100) if total_topics > 0 else 0
            
            result.append({
                'id':           course.id,
                'title':        course.title,
                'total_topics': total_topics,
                'completed':    completed,
                'pct':          pct,
            })
        
        return JsonResponse({'status': 'success', 'courses': result})
    
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        })


def get_course_exam(request, course_id):
    from sms.models import Courses
    from quiz.models import Course as ExamCourse
    
    try:
        programming_course = Courses.objects.get(id=course_id)
        # Find the exam course linked to this programming course
        exam_course = ExamCourse.objects.filter(
            course_name=programming_course
        ).first()
        
        if exam_course:
            return JsonResponse({
                'status': 'success',
                'exam_course_id': exam_course.id
            })
        else:
            return JsonResponse({
                'status': 'none',
                'message': 'No exam found for this course'
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

        
# ✅ Clean up lesson code for display (remove ALL comments)
from bs4 import BeautifulSoup
import re

def _clean_lesson_code_for_display(desc):
    """Remove HTML tags and extract only Python code from lesson description."""
    
    if not desc:
        return ""
    
    # Try to parse as HTML
    try:
        soup = BeautifulSoup(desc, 'html.parser')
        
        # Find all code blocks (pre > code tags)
        code_blocks = soup.find_all('code', class_='language-python')
        
        if code_blocks:
            # Extract code from all Python code blocks
            code_lines = []
            for block in code_blocks:
                code_text = block.get_text().strip()
                # Remove comment lines
                for line in code_text.splitlines():
                    stripped = line.strip()
                    if stripped and not stripped.startswith('#'):
                        # Remove inline comments
                        if '#' in line:
                            code_part = line.split('#')[0].rstrip()
                            if code_part:
                                code_lines.append(code_part)
                        else:
                            code_lines.append(line.rstrip())
            
            return '\n'.join(code_lines)
        
        # Fallback: if no code blocks, try to find any <pre> or <code> tags
        pre_tags = soup.find_all('pre')
        if pre_tags:
            code_lines = []
            for pre in pre_tags:
                code_text = pre.get_text().strip()
                for line in code_text.splitlines():
                    stripped = line.strip()
                    if stripped and not stripped.startswith('#'):
                        if '#' in line:
                            code_part = line.split('#')[0].rstrip()
                            if code_part:
                                code_lines.append(code_part)
                        else:
                            code_lines.append(line.rstrip())
            return '\n'.join(code_lines)
        
        # Last resort: strip all HTML and look for Python patterns
        text = soup.get_text()
        lines = text.splitlines()
        code_lines = []
        for line in lines:
            stripped = line.strip()
            # Look for Python code patterns
            if stripped and (
                'print(' in stripped or
                stripped.startswith('import ') or
                '=' in stripped and not stripped.startswith('#')
            ):
                if not stripped.startswith('#'):
                    if '#' in line:
                        code_part = line.split('#')[0].rstrip()
                        if code_part:
                            code_lines.append(code_part)
                    else:
                        code_lines.append(line.rstrip())
        
        return '\n'.join(code_lines)
    
    except Exception as e:
        print(f'[clean_lesson_code] HTML parsing failed: {e}')
        # Fallback to simple text processing
        lines = desc.splitlines()
        code_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('<'):
                if '#' in line:
                    code_part = line.split('#')[0].rstrip()
                    if code_part:
                        code_lines.append(code_part)
                else:
                    code_lines.append(line.rstrip())
        
        return '\n'.join(code_lines)


@require_http_methods(["POST"])
def validate_topic_completion(request):
    try:
        data           = json.loads(request.body)
        topic_id       = data.get('topic_id')
        student_code   = data.get('code', '').strip()
        student_output = data.get('output', '').strip()

        topic = Topics.objects.select_related('courses').get(id=topic_id)

        print(f'[validate] topic={topic.title}')
        print(f'[validate] topic.desc={repr(topic.desc)}')
        print(f'[validate] student_code={repr(student_code[:120])}')
        print(f'[validate] student_output={repr(student_output)}')
        

        attempt_key = f'topic_{topic_id}_attempts'
        attempts = request.session.get(attempt_key, 0)

        if topic.validation_type == 'code':

            if not student_output:
                return JsonResponse({
                    'status': 'success', 'is_correct': False,
                    'message': '⚠️ Run your code first — no output detected.',
                })

            desc         = (topic.desc or '').replace('\r\n', '\n').replace('\r', '\n').strip()
            student_code = student_code.replace('\r\n', '\n').replace('\r', '\n').strip()
            has_print    = bool(re.search(r'print\s*\(', desc))
            has_input    = bool(re.search(r'input\s*\(', desc))

            print(f'[validate] desc normalized={repr(desc)}')
            print(f'[validate] has_print={has_print}  has_input={has_input}')

            # ── CASE A: lesson has input() → validate code structure ──
            if has_input:
                print(f'[validate] ▶️ CASE A — input() detected')

                # Check if student used input() at all
                if 'input(' not in student_code.lower():
                    attempts += 1
                    request.session[attempt_key] = attempts
                    hint = _get_progressive_hint(attempts, topic)
                    lesson_display = _clean_lesson_code_for_display(desc)
                    return JsonResponse({
                        'status': 'success', 'is_correct': False,
                        'message': '❌ Your code must use the input() function to get user input.',
                        'hint': hint,
                        'attempts': attempts,
                        'show_solution': attempts >= 4,
                        'lesson_code': lesson_display,
                    })

                # ── Fast path: normalize and compare directly ─────────
                def _normalize(code):
                    lines = []
                    for line in code.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            lines.append(line)
                    return '\n'.join(lines)

                lesson_normalized  = _normalize(desc)
                student_normalized = _normalize(student_code)

                print(f'[validate] lesson_normalized={repr(lesson_normalized)}')
                print(f'[validate] student_normalized={repr(student_normalized)}')

                if lesson_normalized == student_normalized:
                    print(f'[validate] ✅ Code matches exactly — auto-passing')
                    code_validation = {
                        'is_correct': True,
                        'feedback': '✅ Perfect! Your code matches the lesson exactly.'
                    }
                else:
                    print(f'[validate] Code differs — calling AI structure check')
                    code_validation = _validate_code_structure_with_ai_for_input(desc, student_code, attempts)

                if code_validation['is_correct']:
                    request.session[attempt_key] = 0
                    _mark_complete(request.user, topic)
                    xp_data = award_xp(request.user, 100)

                    from users.models import Profile
                    profile = Profile.objects.get(user=request.user)
                    total_topics = Topics.objects.filter(courses=topic.courses).count()
                    completed_topics = CompletedTopics.objects.filter(
                        user=profile,
                        topic__courses=topic.courses
                    ).count()
                    completion_pct = round((completed_topics / total_topics * 100)) if total_topics > 0 else 0

                    return JsonResponse({
                        'status': 'success', 'is_correct': True,
                        'message': code_validation['feedback'],
                        'xp': xp_data,
                        'completion_percentage': completion_pct,
                        'course_id': topic.courses.id if topic.courses else None,
                    })
                else:
                    attempts += 1
                    request.session[attempt_key] = attempts
                    hint = _get_progressive_hint(attempts, topic)
                    lesson_display = _clean_lesson_code_for_display(desc)
                    return JsonResponse({
                        'status': 'success', 'is_correct': False,
                        'message': code_validation['feedback'],
                        'hint': hint,
                        'attempts': attempts,
                        'show_solution': attempts >= 4,
                        'lesson_code': lesson_display,
                    })

            # ── CASE B: print() only → run and compare output ─────────
            elif has_print:
                print(f'[validate] ▶️ CASE B — print() only, running lesson code')
                expected_output = _extract_expected_output_with_ai(desc)
                print(f'[validate] expected_output from AI={repr(expected_output)}')

                if expected_output is None:
                    print(f'[validate] ⚠️ falling back to GPT compare')
                    result = _gpt_compare(desc, student_output)
                else:
                    output_matches = (student_output.strip() == expected_output.strip())
                    print(f'[validate] Comparing: student="{student_output.strip()}" vs expected="{expected_output.strip()}"')
                    print(f'[validate] output_matches={output_matches}')

                    if not output_matches:
                        attempts += 1
                        request.session[attempt_key] = attempts
                        hint = _get_progressive_hint(attempts, topic)
                        lesson_display = _clean_lesson_code_for_display(desc)
                        return JsonResponse({
                            'status': 'success', 'is_correct': False,
                            'message': f'❌ Expected output: "{expected_output}" but you got: "{student_output}". Try again.',
                            'hint': hint,
                            'attempts': attempts,
                            'show_solution': attempts >= 4,
                            'lesson_code': lesson_display,
                        })
                    else:
                        print(f'[validate] Output correct, now validating code structure with AI')
                        code_validation = _validate_code_structure_with_ai(desc, student_code, attempts)
                        print(f'[validate] code_validation={code_validation}')
                        result = code_validation

            # ── CASE C: no print/input → check assignments ─────────────
            else:
                assignments = re.findall(r'^\s*([a-zA-Z_]\w*)\s*=\s*([^=\n#][^\n#]*)', desc, re.MULTILINE)
                required    = [(var.strip(), val.strip()) for var, val in assignments]
                print(f'[validate] CASE C required={required}')

                missing = []
                for var, val in required:
                    pattern = rf'\b{re.escape(var)}\s*=\s*{re.escape(val)}'
                    if not re.search(pattern, student_code):
                        missing.append(f'{var} = {val}')

                if missing:
                    attempts += 1
                    request.session[attempt_key] = attempts
                    hint = _get_progressive_hint(attempts, topic, missing)
                    lesson_display = _clean_lesson_code_for_display(desc)
                    return JsonResponse({
                        'status': 'success', 'is_correct': False,
                        'message': f'❌ Missing required assignments: {", ".join(missing)}',
                        'hint': hint,
                        'attempts': attempts,
                        'lesson_code': lesson_display,
                    })

                result = {'is_correct': True, 'feedback': '✅ Well done! You completed all required assignments.'}

            print(f'[validate] result={result}')

            if result['is_correct']:
                request.session[attempt_key] = 0
                _mark_complete(request.user, topic)
                xp_data = award_xp(request.user, 100)

                from users.models import Profile
                profile = Profile.objects.get(user=request.user)
                total_topics = Topics.objects.filter(courses=topic.courses).count()
                completed_topics = CompletedTopics.objects.filter(
                    user=profile,
                    topic__courses=topic.courses
                ).count()
                completion_pct = round((completed_topics / total_topics * 100)) if total_topics > 0 else 0

                return JsonResponse({
                    'status': 'success', 'is_correct': True,
                    'message': result['feedback'],
                    'xp': xp_data,
                    'completion_percentage': completion_pct,
                    'course_id': topic.courses.id if topic.courses else None,
                })
            else:
                attempts += 1
                request.session[attempt_key] = attempts
                print(f'[validate] Attempt #{attempts} for topic {topic_id}')
                hint = _get_progressive_hint(attempts, topic)
                lesson_display = _clean_lesson_code_for_display(desc)
                return JsonResponse({
                    'status': 'success', 'is_correct': False,
                    'message': result['feedback'],
                    'hint': hint,
                    'attempts': attempts,
                    'show_solution': attempts >= 4,
                    'lesson_code': lesson_display,
                })

        elif topic.validation_type == 'quiz':
            student_answer = data.get('answer', '').strip()

            if not student_answer:
                return JsonResponse({
                    'status': 'success', 'is_correct': False,
                    'message': '⚠️ Please type an answer before submitting.',
                })

            prompt = f"""You are a strict teacher marking a quiz answer.
TOPIC: {topic.title}
QUESTION: {topic.quiz_question}
CORRECT ANSWER: {topic.quiz_correct_answer}
STUDENT ANSWER: {student_answer}
Be strict. Respond ONLY with JSON:
{{"is_correct": true, "feedback": "..."}}
or
{{"is_correct": false, "feedback": "..."}}"""

            result = _call_gpt(prompt, max_tokens=150)

            if result['is_correct']:
                request.session[attempt_key] = 0
                _mark_complete(request.user, topic)
                xp_data = award_xp(request.user, 100)
                return JsonResponse({
                    'status': 'success', 'is_correct': True,
                    'message': result['feedback'], 'xp': xp_data,
                })
            else:
                attempts += 1
                request.session[attempt_key] = attempts
                hint = _get_progressive_hint(attempts, topic)
                lesson_display = (topic.desc or '').replace('\r\n', '\n').replace('\r', '\n').strip()
                return JsonResponse({
                    'status': 'success', 'is_correct': False,
                    'message': result['feedback'],
                    'hint': hint,
                    'attempts': attempts,
                    'show_solution': attempts >= 3,
                    'lesson_code': lesson_display,
                })

        else:
            _mark_complete(request.user, topic)
            xp_data = award_xp(request.user, 100)
            return JsonResponse({
                'status': 'success', 'is_correct': True,
                'message': 'Topic completed!', 'xp': xp_data,
            })

    except Topics.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Topic not found'}, status=404)
    except Exception as e:
        import traceback; traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)    


def _get_progressive_hint(attempts, topic, missing=None):
    """Provide increasingly helpful hints based on attempt count."""
    
    if attempts == 1:
        return "💡 Take another look at the lesson code. What's different?"
    
    elif attempts == 2:
        if topic.validation_hints:
            return f"💡 Hint: {topic.validation_hints}"
        return "💡 Compare your code carefully with the example. Check variable names and syntax."
    
    elif attempts == 3:
        if missing:
            return f"💡 You're missing: {', '.join(missing)}. Try adding these exact lines."
        return "💡 Almost there! Review the lesson code line by line and match it exactly."
    
    elif attempts >= 4:
        return ""
    
    return None


# ✅ ADD THIS NEW FUNCTION
def _validate_code_structure_with_ai_for_input(lesson_code, student_code, attempts=0):
    """Validate code with input() - focus on structure, not output."""
    
    lesson_code = lesson_code.replace('\r\n', '\n').replace('\r', '\n').strip()
    student_code = student_code.replace('\r\n', '\n').replace('\r', '\n').strip()
    
    lesson_runnable = _clean_lesson_code_for_display(lesson_code)
    
    attempt_context = ""
    if attempts > 0:
        attempt_context = f"\nThis is the student's attempt #{attempts + 1}. "
        if attempts >= 2:
            attempt_context += "Provide more specific guidance since they're struggling."
    
    prompt = f"""You are a strict Python teacher checking if a student followed the lesson instructions.

LESSON CODE (what they should learn):
{lesson_runnable}

STUDENT CODE (what they wrote):
{student_code}
{attempt_context}

IMPORTANT: This lesson uses input() which requires user input, so we CANNOT compare output.
Instead, check:
1. Did the student use input() to get user input?
2. Did they store the input in a variable if required?
3. Did they print the result if required?
4. Is the overall structure and logic correct?

Be lenient about:
- Variable names (if lesson uses "name", student can use "user_name" or "n")
- Exact prompt text in input() (as long as it makes sense)
- Output formatting differences (f-strings vs concatenation)

Be strict about:
- Must use input() if lesson uses it
- Must use print() if lesson uses it
- Must follow the same basic logic flow

When providing example code in feedback, use actual newlines (\\n) to separate lines.

Respond ONLY with JSON:
{{"is_correct": true, "feedback": "✅ Great! You used input() correctly and followed the lesson structure."}}
or
{{"is_correct": false, "feedback": "❌ [specific issue]. Example:\\n[correct code]"}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strict Python teacher. Respond ONLY with valid JSON. Use \\n for line breaks in code examples."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=250,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content.strip())
        
        if 'feedback' in result:
            result['feedback'] = result['feedback'].replace('\\n', '\n')
        
        print(f'[validate] AI code validation result (input): {result}')
        return result
    except Exception as e:
        print(f'[validate] _validate_code_structure_with_ai_for_input failed: {e}')
        import traceback
        traceback.print_exc()
        return {
            'is_correct': True,
            'feedback': '✅ Good! You used input() and your code ran successfully.'
        }
        


@require_http_methods(["POST"])
def get_topic_solution(request):
    """Provide solution after multiple failed attempts."""
    try:
        data = json.loads(request.body)
        topic_id = data.get('topic_id')
        
        topic = Topics.objects.get(id=topic_id)
        
        # Check if student has attempted enough times
        attempt_key = f'topic_{topic_id}_attempts'
        attempts = request.session.get(attempt_key, 0)
        
        if attempts < 3:  # Require at least 3 attempts before showing solution
            return JsonResponse({
                'status': 'error',
                'message': 'Try a few more times before viewing the solution!'
            }, status=403)
        
        # Extract the solution from the lesson code
        desc = (topic.desc or '').replace('\r\n', '\n').replace('\r', '\n').strip()
        solution = '\n'.join(
            line for line in desc.splitlines()
            if not line.strip().startswith('#')
        ).strip()
        
        return JsonResponse({
            'status': 'success',
            'solution': solution,
            'explanation': 'Here is the correct solution. Study it carefully and try again!'
        })
        
    except Topics.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Topic not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def _validate_code_structure_with_ai(lesson_code, student_code, attempts=0):
    """Use AI to check if student code follows the lesson requirements, not just output."""
    
    # Normalize both codes
    lesson_code = lesson_code.replace('\r\n', '\n').replace('\r', '\n').strip()
    student_code = student_code.replace('\r\n', '\n').replace('\r', '\n').strip()
    
    # Remove comment-only lines for comparison
    lesson_runnable = '\n'.join(
        line for line in lesson_code.splitlines()
        if not line.strip().startswith('#')
    ).strip()
    
    prompt = f"""You are a strict Python teacher checking if a student followed the lesson instructions.

LESSON CODE (what they should learn):
{lesson_runnable}

STUDENT CODE (what they wrote):
{student_code}

Your task:
1. Check if the student used the SAME approach as the lesson (same variables, same logic)
2. The output might be correct, but did they write the code correctly?
3. If lesson has "age = 16" and "print(age)", student MUST use a variable, not just "print(16)"
4. If lesson has calculations like "print(2 + 3)", student should do the calculation, not hardcode "print(5)"
5. If lesson defines variables, student must define them too, not skip them

Be strict but fair. Minor differences in whitespace are okay if the logic is the same.

When providing example code in feedback, use actual newlines (\\n) to separate lines.

Respond ONLY with JSON:
{{"is_correct": true, "feedback": "✅ Perfect! You followed the lesson correctly."}}
or
{{"is_correct": false, "feedback": "❌ You got the right output, but [specific issue]. Example:\\nname = 'ahmed'\\nprint(name)"}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strict Python teacher. Respond ONLY with valid JSON. Use \\n for line breaks in code examples."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=250,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content.strip())
        
        # ✅ Convert \n in feedback to actual newlines for proper formatting
        if 'feedback' in result:
            result['feedback'] = result['feedback'].replace('\\n', '\n')
        
        print(f'[validate] AI code validation result: {result}')
        return result
    except Exception as e:
        print(f'[validate] _validate_code_structure_with_ai failed: {e}')
        import traceback
        traceback.print_exc()
        # If AI fails, be lenient and accept correct output
        return {
            'is_correct': True,
            'feedback': '✅ Correct output! (Code validation unavailable)'
        }
    

def _extract_expected_output_with_ai(desc):
    """Use GPT to determine what the code in desc should print."""
    prompt = f"""Look at this Python lesson code:
{desc}

What is the EXACT expected output when this code runs? 
If there are multiple print statements, include all outputs (each on a new line).
If there are no print statements, respond with "NO_OUTPUT".

Respond ONLY with the expected output text itself, nothing else. No explanations, no JSON, just the raw output."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Python interpreter. Return only the exact output, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=150,
        )
        output = response.choices[0].message.content.strip()
        return None if output == "NO_OUTPUT" else output
    except Exception as e:
        print(f'[validate] _extract_expected_output_with_ai failed: {e}')
        return None    


        
def _run_code_safely(code):
    """Run lesson code in subprocess and return its output."""
    fname = None
    try:
        code = code.replace('\r\n', '\n').replace('\r', '\n').strip()

        # Strip comment-only lines so they don't interfere with execution
        runnable = '\n'.join(
            line for line in code.splitlines()
            if not line.strip().startswith('#')
        ).strip()

        print(f'[validate] _run_code_safely runnable={repr(runnable)}')

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(runnable)
            fname = f.name

        print(f'[validate] _run_code_safely fname={fname}')

        result = subprocess.run(
            [sys.executable, fname],
            capture_output=True, text=True, timeout=5
        )

        print(f'[validate] _run_code_safely returncode={result.returncode}')
        print(f'[validate] _run_code_safely stdout={repr(result.stdout)}')
        print(f'[validate] _run_code_safely stderr={repr(result.stderr)}')

        expected_output = result.stdout.strip() if result.returncode == 0 else None
        print(f'[validate] _run_code_safely expected_output={repr(expected_output)}')

        if result.returncode != 0:
            print(f'[validate] lesson code error: {result.stderr}')

        return expected_output

    except Exception as e:
        print(f'[validate] _run_code_safely failed: {e}')
        import traceback; traceback.print_exc()
        return None
    finally:
        # Always clean up temp file
        if fname and os.path.exists(fname):
            try:
                os.unlink(fname)
            except Exception:
                pass

            
def _gpt_compare(desc, student_output):
    prompt = f"""The lesson code is:
{desc}

What does this code print when run? That is the expected output.
The student output was: {student_output}
Does it match exactly?

Respond ONLY with JSON:
{{"is_correct": true, "feedback": "Correct!"}}
or
{{"is_correct": false, "expected": "X", "feedback": "Expected X but got Y."}}"""
    return _call_gpt(prompt)


def _call_gpt(prompt, max_tokens=200):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict Python teacher. Respond ONLY with valid JSON."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content.strip())


def _mark_complete(user, topic):
    try:
        from users.models import Profile
        from webprojects.models import StudentProgress

        profile = Profile.objects.get(user=user)

        if not CompletedTopics.objects.filter(user=profile, topic=topic).exists():
            CompletedTopics.objects.create(user=profile, topic=topic)
            print(f'[validate] ✅ CompletedTopics saved: topic {topic.id} for {user}')

        progress, _ = StudentProgress.objects.get_or_create(
            student=user,
            defaults={'current_topic': topic}
        )
        if not progress.completed_topics.filter(id=topic.id).exists():
            progress.completed_topics.add(topic)
            print(f'[validate] ✅ StudentProgress updated: topic {topic.id}')

    except Exception as e:
        import traceback; traceback.print_exc()
        print(f'[validate] ❌ _mark_complete failed: {e}')


def topic_info(request, topic_id):
    try:
        topic = Topics.objects.get(id=topic_id)
        return JsonResponse({
            'status':          'success',
            'validation_type': topic.validation_type or 'code',
            'quiz_question':   topic.quiz_question   or '',
        })
    except Topics.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)
        
@require_http_methods(["GET"])
def recommend_next_course(request):
    """Recommend the next course based on current course completion."""
    try:
        course_id = request.GET.get('course_id')
        
        if not course_id:
            return JsonResponse({'status': 'error', 'message': 'No course ID provided'}, status=400)
        
        current_course = Courses.objects.get(id=course_id)
        
        # Get user's completed courses
        from users.models import Profile
        profile = Profile.objects.get(user=request.user)
        completed_course_ids = CompletedTopics.objects.filter(
            user=profile
        ).values_list('topic__courses_id', flat=True).distinct()
        
        # Find next course in sequence (same category, not completed)
        next_course = Courses.objects.filter(
            categories=current_course.categories,
            # ✅ REMOVED: is_published=True (field doesn't exist)
        ).exclude(
            id__in=completed_course_ids
        ).exclude(
            id=current_course.id
        ).order_by('created').first()
        
        if not next_course:
            # Try to find any course not completed
            next_course = Courses.objects.exclude(
                id__in=completed_course_ids
                # ✅ REMOVED: is_published=True
            ).order_by('-created').first()
        
        if next_course:
            topic_count = Topics.objects.filter(courses=next_course).count()
            
            return JsonResponse({
                'status': 'success',
                'recommended_course': {
                    'id': next_course.id,
                    'title': next_course.title,
                    'description': next_course.desc,
                    'topic_count': topic_count,
                },
                'current_course': {
                    'id': current_course.id,
                    'title': current_course.title,
                }
            })
        else:
            return JsonResponse({
                'status': 'success',
                'recommended_course': None,
                'current_course': {
                    'id': current_course.id,
                    'title': current_course.title,
                },
                'message': 'No more courses available. Great job!'
            })
        
    except Courses.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Course not found'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

import re

@login_required
@csrf_protect
@require_http_methods(["POST"])
def generate_topic_quiz(request, topic_id):
    topic = get_object_or_404(Topics, id=topic_id)
    plain_desc = re.sub('<[^<]+?>', '', topic.desc or '')

    system_prompt = """You are a strict quiz generator for a programming/learning platform.
Generate exactly 3 multiple-choice questions that test understanding of the given lesson content.

Return ONLY valid JSON, no markdown, no explanations, in this exact shape:
{"questions": [
  {"question": "...", "options": ["A", "B", "C", "D"], "correct_index": 0},
  {"question": "...", "options": ["A", "B", "C", "D"], "correct_index": 2},
  {"question": "...", "options": ["A", "B", "C", "D"], "correct_index": 1}
]}
Each question must have exactly 4 options. correct_index is 0-based."""

    user_prompt = f"""TOPIC: {topic.title}

LESSON CONTENT:
{plain_desc[:4000]}

Generate 3 multiple-choice questions testing understanding of this content."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=1000,
        )
        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = "\n".join(
                line for line in raw.splitlines()
                if not line.strip().startswith("```")
            ).strip()

        quiz_data = json.loads(raw)
        questions = quiz_data.get("questions", [])

        if len(questions) != 3:
            raise ValueError(f"Expected 3 questions, got {len(questions)}")
        for q in questions:
            if not all(k in q for k in ("question", "options", "correct_index")):
                raise ValueError("Malformed question object")
            if len(q["options"]) != 4:
                raise ValueError("Each question must have 4 options")

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": "Failed to generate quiz",
            "detail": str(e)
        }, status=500)

    # Correct answers never leave the server
    request.session[f'quiz_{topic_id}_answers'] = [q["correct_index"] for q in questions]
    request.session.modified = True

    client_questions = [{"question": q["question"], "options": q["options"]} for q in questions]

    return JsonResponse({"status": "success", "topic_id": topic_id, "questions": client_questions})


@login_required
@csrf_protect
@require_http_methods(["POST"])
def submit_topic_quiz(request, topic_id):
    try:
        data = json.loads(request.body)
        answers = data.get("answers", [])
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    topic = get_object_or_404(Topics.objects.select_related('courses'), id=topic_id)
    course = topic.courses  # ✅ derive from the topic itself — never trust the client for this

    correct_answers = request.session.get(f'quiz_{topic_id}_answers')
    if not correct_answers:
        return JsonResponse({
            "status": "error",
            "message": "No active quiz found for this topic. Please start the quiz again."
        }, status=400)

    if len(answers) != len(correct_answers):
        return JsonResponse({"status": "error", "message": "Answer count mismatch."}, status=400)

    score = sum(1 for a, c in zip(answers, correct_answers) if a == c)
    total = len(correct_answers)
    percent = round((score / total) * 100) if total else 0
    passed = percent >= 60

    del request.session[f'quiz_{topic_id}_answers']
    request.session.modified = True

    response_data = {
        "status": "success",
        "passed": passed,
        "score": score,
        "total": total,
        "percent": percent,
    }

    if passed:
        progress, _ = StudentProgress.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'current_topic': topic}
        )
        progress.completed_topics.add(topic)

        course_topics = list(
            Topics.objects.filter(courses=course).order_by('id')
        ) if course else []

        next_topic = None
        ids = [t.id for t in course_topics]
        try:
            pos = ids.index(topic.id)
            if pos + 1 < len(course_topics):
                next_topic = course_topics[pos + 1]
                progress.current_topic = next_topic
        except ValueError:
            pass

        progress.save()

        completed_ids = set(progress.completed_topics.values_list('id', flat=True))
        relevant_completed = completed_ids & set(ids)
        total_topics = len(course_topics)
        done = len(relevant_completed)
        overall_pct = round((done / total_topics) * 100) if total_topics else 0

        xp_data = award_xp(request.user, 100)

        response_data.update({
            "xp": xp_data,
            "completed_topic_ids": list(completed_ids),
            "completed_count": done,
            "total_count": total_topics,
            "overall_pct": overall_pct,
            "next_topic_id": next_topic.id if next_topic else None,
            "course_id": course.id if course else None,
        })

    return JsonResponse(response_data)

