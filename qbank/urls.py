from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    # Questions
    path('questions/', login_required(views.question_list), name='question_list'),
    path('questions/add/', login_required(views.add_question), name='add_question'),
    path('questions/<int:pk>/edit/', login_required(views.edit_question), name='edit_question'),
    path('questions/<int:pk>/view/', login_required(views.view_question), name='view_question'),
    path('questions/<int:pk>/delete/', login_required(views.delete_question), name='delete_question'),
    path('questions/<int:pk>/approve/', login_required(views.approve_question), name='approve_question'),

    # Chapters
    path('chapters/', login_required(views.chapter_list), name='chapter_list'),
    path('chapters/add/', login_required(views.add_chapter), name='add_chapter'),
    path('chapters/<int:pk>/delete/', login_required(views.delete_chapter), name='delete_chapter'),

    # Import / Export
    path('questions/import/', login_required(views.bulk_import_questions), name='bulk_import_questions'),
    path('questions/import/template/', login_required(views.download_import_template), name='download_import_template'),
    path('questions/export/', login_required(views.export_bank_excel), name='export_bank_excel'),

    # AJAX
    path('ajax/subjects/', login_required(views.ajax_load_subjects), name='qbank_ajax_subjects'),
    path('ajax/chapters/', login_required(views.ajax_load_chapters), name='qbank_ajax_chapters'),

    # Blueprints
    path('blueprints/', login_required(views.blueprint_list), name='blueprint_list'),
    path('blueprints/create/', login_required(views.create_blueprint), name='create_blueprint'),
    path('blueprints/<int:pk>/delete/', login_required(views.delete_blueprint), name='delete_blueprint'),

    # Papers
    path('papers/', login_required(views.paper_list), name='paper_list'),
    path('papers/create/', login_required(views.create_paper), name='create_paper'),
    path('papers/<int:pk>/builder/', login_required(views.paper_builder), name='paper_builder'),
    path('papers/<int:pk>/builder/add-section/', login_required(views.add_section), name='add_section'),
    path('papers/<int:pk>/builder/delete-section/<int:sec_pk>/', login_required(views.delete_section), name='delete_section'),
    path('papers/<int:pk>/builder/add-question/', login_required(views.add_question_to_paper), name='add_question_to_paper'),
    path('papers/<int:pk>/builder/remove-question/', login_required(views.remove_question_from_paper), name='remove_question_from_paper'),
    path('papers/<int:pk>/builder/auto-generate/', login_required(views.auto_generate_paper), name='auto_generate_paper'),
    path('papers/<int:pk>/preview/', login_required(views.paper_preview), name='paper_preview'),
    path('papers/<int:pk>/pdf/', login_required(views.export_paper_pdf), name='export_paper_pdf'),
    path('papers/<int:pk>/answer-key/', login_required(views.export_answer_key_pdf), name='export_answer_key_pdf'),
    path('papers/<int:pk>/delete/', login_required(views.delete_paper), name='delete_paper'),
    path('papers/<int:pk>/publish/', login_required(views.publish_paper), name='publish_paper'),
]
