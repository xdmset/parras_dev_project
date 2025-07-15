# pendientes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL para la sincronización
    path('sync/', views.sync_todos_from_api, name='sync-todos'),

    # URLs para las vistas CRUD
    path('', views.TodoListView.as_view(), name='todo-list'),
    path('todo/<int:pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
    path('todo/new/', views.TodoCreateView.as_view(), name='todo-create'),
    path('todo/<int:pk>/edit/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('todo/<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),

    # URLs para las listas específicas solicitadas
    path('list/ids/', views.todo_list_ids, name='todo-list-ids'),
    path('list/id-title/', views.todo_list_id_title, name='todo-list-id-title'),
    path('list/unresolved/', views.todo_list_unresolved, name='todo-list-unresolved'),
    path('list/resolved/', views.todo_list_resolved, name='todo-list-resolved'),
    path('list/id-userid/', views.todo_list_id_userid, name='todo-list-id-userid'),
    path('list/resolved/id-userid/', views.todo_list_resolved_id_userid, name='todo-list-resolved-id-userid'),
    path('list/unresolved/id-userid/', views.todo_list_unresolved_id_userid, name='todo-list-unresolved-id-userid'),
]