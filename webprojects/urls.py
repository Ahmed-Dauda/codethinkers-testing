from django.urls import path
from webprojects.views import ai_python_completion,ai_suggest_code, auto_save_view, create_file, create_folder, create_project, explain_code_view, project_detail, file_detail, public_folder_view, run_python_code, share_preview_view, upload_image_ajax, view_rendered_file

urlpatterns = [
   
    # urls.py
    path('<int:project_id>/upload-image-ajax/',upload_image_ajax, name='upload_image_ajax'),

    path("autosave/", auto_save_view, name="file_autosave"),

    path('preview/share/<int:project_id>/<int:file_id>/', share_preview_view, name='share_preview'),
    path('create-project/', create_project, name='create_project'),

    path('view/<int:file_id>/', view_rendered_file, name='view_rendered_file'),

    path('folder/<int:folder_id>/', public_folder_view, name='public_folder_view'),

    path("ai-python-completion/", ai_python_completion, name="ai_python_completion"),

    path("run-python/", run_python_code, name="run_python_code"),
    path('explain-code/', explain_code_view, name='explain_code'),
    path('ai-suggest/', ai_suggest_code, name='ai_suggest_code'),

    path('<int:project_id>/create-file/', create_file, name='create_file'),
    path('<int:project_id>/create-folder/', create_folder, name='create_folder'),
    path('<int:project_id>/', project_detail, name='project_detail'),
    path('<int:project_id>/file/<int:file_id>/', file_detail, name='file_detail'),
]
