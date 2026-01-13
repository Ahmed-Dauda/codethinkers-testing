from django.urls import path
from webprojects.views import (ai_python_completion,ai_suggest_code, auto_save_view, create_file, create_folder, 
create_project, explain_code_view, 
file_delete, file_preview, project_detail,
file_detail, project_files_json, public_folder_view, 
run_python_code, share_preview_view, file_chat,
upload_file_ajax, view_rendered_file)

app_name = 'webprojects'

urlpatterns = [
    
    path('project/<int:project_id>/file/<int:file_id>/chat/', file_chat, name='file_chat'),
    path('<int:project_id>/files-json/', project_files_json, name='project_files_json'),

    path('projects/<int:project_id>/file/<int:file_id>/delete/', file_delete, name='file_delete'),
    path('projects/<int:project_id>/file/<int:file_id>/preview/', file_preview, name='file_preview'),
    path('projects/<int:project_id>/upload-file-ajax/', upload_file_ajax, name='upload_file_ajax'),
    path('<int:project_id>/file/<int:file_id>/', file_detail, name='file_detail'),

    path('<int:project_id>/create-file/', create_file, name='create_file'),
    path('projects/<int:project_id>/create-folder/', create_folder, name='create_folder'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),

    path("autosave/", auto_save_view, name="file_autosave"),
    path('preview/share/<int:project_id>/<int:file_id>/', share_preview_view, name='share_preview'),
    path('create-project/', create_project, name='create_project'),

    path('view/<int:file_id>/', view_rendered_file, name='view_rendered_file'),
    path('folder/<int:folder_id>/', public_folder_view, name='public_folder_view'),

    path("ai-python-completion/", ai_python_completion, name="ai_python_completion"),
    path("run-python/", run_python_code, name="run_python_code"),
    path('explain-code/', explain_code_view, name='explain_code'),
    path('ai-suggest/', ai_suggest_code, name='ai_suggest_code'),
]

