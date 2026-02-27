import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project, File, StudentProgress, StudentXP
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
            course = Courses.objects.filter(title=name).first()

            print("CREATE PROJECT COURSE:", course)
            # ---------------------------------------------------

            # Get or create DEFAULT topic FOR THIS COURSE
            default_topic, _ = Topics.objects.get_or_create(
                title="General",
                courses=course
            )
            print('topic',default_topic)

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
                created_by=request.user,
                content=default_content,
                topic=default_topic
            )

            course_name = file.project.name
            print("Created project:", course_name, "with file:", file.name, "and topic:", default_topic.title)

           
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



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def file_autosave(request):
    try:
        print("=== AUTOSAVE BACKEND DEBUG ===")
        print("Request method:", request.method)
        print("Request body:", request.body[:200])  # First 200 chars
        
        data = json.loads(request.body)
        file_id = data.get("file_id")
        content = data.get("content", "")
        
        print(f"File ID: {file_id}")
        print(f"Content length: {len(content)}")
        
        # Get the file
        file_obj = File.objects.get(id=file_id)
        print(f"Found file: {file_obj.name}")
        
        # Save the content
        file_obj.content = content
        file_obj.save()
        
        print("✅ File saved successfully")
        
        return JsonResponse({
            "status": "success",
            "message": "File saved successfully",
            "file_id": file_id,
            "content_length": len(content)
        })
        
    except File.DoesNotExist:
        print(f"❌ File not found: {file_id}")
        return JsonResponse({
            "status": "error",
            "message": f"File with ID {file_id} not found"
        }, status=404)
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return JsonResponse({
            "status": "error",
            "message": "Invalid JSON data"
        }, status=400)
        
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }, status=500)
        

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

        # ✅ FIX: no course=None filter
        progress = StudentProgress.objects.filter(
            student=request.user
        ).prefetch_related('completed_topics').order_by('-last_updated').first()

        current_topic = progress.current_topic if progress else None
        completed_ids = set(
            progress.completed_topics.values_list('id', flat=True)
        ) if progress else set()

        sidebar_ids        = {t.id for t in all_topics}
        relevant_completed = completed_ids & sidebar_ids

        total = len(all_topics)
        done  = len(relevant_completed)
        pct   = round((done / total) * 100) if total else 0

        topics_data = [
            {
                'id':         t.id,
                'title':      t.title,
                'completed':  t.id in completed_ids,
                'is_current': bool(current_topic and t.id == current_topic.id),
            }
            for t in all_topics
        ]

        return JsonResponse({
            'status':               'success',
            'current_topic_id':     current_topic.id    if current_topic else None,
            'current_topic_title':  current_topic.title if current_topic else 'None selected',
            'completed_topic_ids':  list(completed_ids),
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

        from sms.models import Topics
        topic = Topics.objects.get(id=topic_id)

        # ✅ FIX: get existing record regardless of course
        progress = StudentProgress.objects.filter(
            student=request.user
        ).order_by('-last_updated').first()

        if not progress:
            progress = StudentProgress.objects.create(
                student=request.user,
                current_topic=topic
            )

        # Mark complete
        progress.completed_topics.add(topic)

        # Advance to next topic within same course
        course_topics = list(
            Topics.objects.filter(courses_id=course_id).order_by('id')
        ) if course_id else list(Topics.objects.all().order_by('id'))

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

        # Return counts scoped to course
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
            'xp': xp_data,
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
    # ADD THESE 3 LINES:
    from .models import StudentProgress
    # ✅ FIX: get progress without course=None filter
    from .models import StudentProgress
    progress = StudentProgress.objects.filter(
        student=request.user
    ).prefetch_related('completed_topics').order_by('-last_updated').first()

    completed_topic_ids = list(
        progress.completed_topics.values_list('id', flat=True)
    ) if progress else []

    current_topic_id = (
        progress.current_topic.id
        if progress and progress.current_topic
        else None
    )

    print("CURRENT TOPIC ID:", current_topic_id)
    print("COMPLETED TOPIC IDS:", completed_topic_ids)
    print("PROGRESS OBJECT:", progress)

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
    print('completed_topic_ids:', completed_topic_ids)
    return render(request, "webprojects/file_detail.html", {
        "file": file,
        "files": files,
        "folders": folders,
        "exts": exts,
        "project": project,
        "is_image": is_image,
        'completed_topic_ids': completed_topic_ids,      # ← ADD
        'current_topic_id': current_topic_id,            # ← ADD
        "topics": topics,
        'course_id': course.id if course else None,  # ← ADD THIS ONE LINE
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


# @csrf_exempt
# def explain_code_view(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             code = data.get("code", "").strip()
#             if not code:
#                 return JsonResponse({"error": "Code is empty"}, status=400)

#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are an expert coding teacher. Explain code clearly."},
#                     {"role": "user", "content": f"Explain this code:\n{code}"}
#                 ],
#                 max_tokens=2000,
#                 temperature=0
#             )
#             explanation = response.choices[0].message.content.strip()
#             return JsonResponse({"explanation": explanation})
#         except Exception as e:
#             print("OpenAI error:", e)
#             return JsonResponse({"error": str(e)}, status=500)
#     return JsonResponse({"error": "Invalid method"}, status=405)


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

        # ✅ Track attempt count for progressive hints
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
            has_input    = bool(re.search(r'input\s*\(', desc))  # ✅ ADD THIS

            print(f'[validate] desc normalized={repr(desc)}')
            print(f'[validate] has_print={has_print}')
            print(f'[validate] has_input={has_input}')  # ✅ ADD THIS

            # ✅ NEW: Special handling for input() lessons
            if has_input:
                print(f'[validate] Lesson has input() - using code structure validation only')
                
                # Check if student used input()
                if 'input(' not in student_code.lower():
                    attempts += 1
                    request.session[attempt_key] = attempts
                    hint = _get_progressive_hint(attempts, topic)
                    lesson_display = _clean_lesson_code_for_display(desc)
                    
                    return JsonResponse({
                        'status': 'success',
                        'is_correct': False,
                        'message': '❌ Your code must use the input() function to get user input.',
                        'hint': hint,
                        'attempts': attempts,
                        'show_solution': attempts >= 4,
                        'lesson_code': lesson_display,
                    })
                
                # Validate code structure with AI (lenient for input)
                code_validation = _validate_code_structure_with_ai_for_input(desc, student_code, attempts)
                
                if code_validation['is_correct']:
                    # ✅ Reset attempts on success
                    request.session[attempt_key] = 0
                    
                    _mark_complete(request.user, topic)
                    xp_data = award_xp(request.user, 100)
                    
                    # Calculate completion percentage
                    from users.models import Profile
                    profile = Profile.objects.get(user=request.user)
                    total_topics = Topics.objects.filter(courses=topic.courses).count()
                    completed_topics = CompletedTopics.objects.filter(
                        user=profile,
                        topic__courses=topic.courses
                    ).count()
                    completion_pct = round((completed_topics / total_topics * 100)) if total_topics > 0 else 0
                    
                    return JsonResponse({
                        'status': 'success', 
                        'is_correct': True,
                        'message': code_validation['feedback'], 
                        'xp': xp_data,
                        'completion_percentage': completion_pct,
                        'course_id': topic.courses.id if topic.courses else None,
                    })
                else:
                    # ✅ Increment attempts on failure
                    attempts += 1
                    request.session[attempt_key] = attempts
                    hint = _get_progressive_hint(attempts, topic)
                    lesson_display = _clean_lesson_code_for_display(desc)
                    
                    return JsonResponse({
                        'status': 'success', 
                        'is_correct': False,
                        'message': code_validation['feedback'],
                        'hint': hint,
                        'attempts': attempts,
                        'show_solution': attempts >= 4,
                        'lesson_code': lesson_display,
                    })

            # ✅ Continue with normal validation for non-input lessons
            if has_print:
                print(f'[validate] ▶️ trying to extract expected output with AI')
                expected_output = _extract_expected_output_with_ai(desc)
                print(f'[validate] expected_output from AI={repr(expected_output)}')
                
                # Fallback to running code if AI fails
                if expected_output is None:
                    print(f'[validate] ⚠️ falling back to GPT compare')
                    result = _gpt_compare(desc, student_output)
                else:
                    # ✅ Step 1: Check if output matches
                    output_matches = (student_output.strip() == expected_output.strip())
                    print(f'[validate] Comparing: student="{student_output.strip()}" vs expected="{expected_output.strip()}"')
                    print(f'[validate] output_matches={output_matches}')
                    
                    if not output_matches:
                        # Output is wrong - fail immediately WITH progressive hints
                        attempts += 1
                        request.session[attempt_key] = attempts
                        print(f'[validate] Attempt #{attempts} for topic {topic_id}')
                        
                        hint = _get_progressive_hint(attempts, topic)
                        lesson_display = _clean_lesson_code_for_display(desc)
                        
                        return JsonResponse({
                            'status': 'success',
                            'is_correct': False,
                            'message': f'❌ Expected output: "{expected_output}" but you got: "{student_output}". Try again.',
                            'hint': hint,
                            'attempts': attempts,
                            'show_solution': attempts >= 4,
                            'lesson_code': lesson_display,
                        })
                    else:
                        # ✅ Step 2: Output is correct, now validate code structure
                        print(f'[validate] Output correct, now validating code structure with AI')
                        code_validation = _validate_code_structure_with_ai(desc, student_code, attempts)
                        print(f'[validate] code_validation={code_validation}')
                        
                        result = code_validation

            else:
                assignments = re.findall(r'^\s*([a-zA-Z_]\w*)\s*=\s*([^=\n#][^\n#]*)', desc, re.MULTILINE)
                required    = [(var.strip(), val.strip()) for var, val in assignments]
                print(f'[validate] CASE B required={required}')

                missing = []
                for var, val in required:
                    pattern = rf'\b{re.escape(var)}\s*=\s*{re.escape(val)}'
                    if not re.search(pattern, student_code):
                        missing.append(f'{var} = {val}')

                if missing:
                    # ✅ Increment attempts on failure
                    attempts += 1
                    request.session[attempt_key] = attempts
                    
                    # ✅ Progressive hints
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
                # ✅ Reset attempts on success
                request.session[attempt_key] = 0
                
                _mark_complete(request.user, topic)
                xp_data = award_xp(request.user, 100)
                
                # Calculate completion percentage
                from users.models import Profile
                profile = Profile.objects.get(user=request.user)
                total_topics = Topics.objects.filter(courses=topic.courses).count()
                completed_topics = CompletedTopics.objects.filter(
                    user=profile,
                    topic__courses=topic.courses
                ).count()
                completion_pct = round((completed_topics / total_topics * 100)) if total_topics > 0 else 0
                
                return JsonResponse({
                    'status': 'success', 
                    'is_correct': True,
                    'message': result['feedback'], 
                    'xp': xp_data,
                    'completion_percentage': completion_pct,
                    'course_id': topic.courses.id if topic.courses else None,
                })
            else:
                # ✅ Increment attempts on failure
                attempts += 1
                request.session[attempt_key] = attempts
                print(f'[validate] Attempt #{attempts} for topic {topic_id}')
                
                # ✅ Progressive hints
                hint = _get_progressive_hint(attempts, topic)
                lesson_display = _clean_lesson_code_for_display(desc)
                
                return JsonResponse({
                    'status': 'success', 
                    'is_correct': False,
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
                # ✅ Reset attempts on success
                request.session[attempt_key] = 0
                
                _mark_complete(request.user, topic)
                xp_data = award_xp(request.user, 100)
                return JsonResponse({
                    'status': 'success', 'is_correct': True,
                    'message': result['feedback'], 'xp': xp_data,
                })
            else:
                # ✅ Increment attempts and provide hints
                attempts += 1
                request.session[attempt_key] = attempts
                hint = _get_progressive_hint(attempts, topic)
                lesson_display = (topic.desc or '').replace('\r\n', '\n').replace('\r', '\n').strip()
                
                return JsonResponse({
                    'status': 'success', 
                    'is_correct': False,
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
        return "💡 Having trouble? Click 'Show Solution' below to see the correct answer."
    
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
    