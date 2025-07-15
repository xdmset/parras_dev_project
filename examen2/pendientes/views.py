import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo
from .serializers import TodoSerializer
from .forms import TodoForm

def sync_todos_from_api(request):
    """
    Obtiene los datos de la API, los valida y actualiza o crea los registros 
    en la base de datos local.
    """
    API_URL = "https://jsonplaceholder.typicode.com/todos"
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lanza un error si la petición no fue exitosa
        data = response.json()
        
        todos_actualizados, todos_creados = 0, 0
        
        for item in data:
            serializer = TodoSerializer(data=item)
            if serializer.is_valid():
                # Copiamos los datos validados
                validated_data = serializer.validated_data
                
                # Extraemos el 'api_id' para usarlo en la búsqueda y lo eliminamos del diccionario
                api_id_lookup = validated_data.pop('api_id')
                
                # Ahora 'validated_data' solo contiene la información a guardar/actualizar
                obj, created = Todo.objects.update_or_create(
                    api_id=api_id_lookup,
                    defaults=validated_data
                )

                if created: 
                    todos_creados += 1
                else: 
                    todos_actualizados += 1
            else:
                # Si esto se imprime, puedes verlo en la consola donde ejecutas 'runserver'
                print(f"Error de validación para item ID {item.get('id')}: {serializer.errors}")

        mensaje = f"Sincronización completa. Pendientes creados: {todos_creados}, actualizados: {todos_actualizados}."
        # Pasamos el mensaje como un parámetro en la URL
        return redirect(f"{reverse_lazy('todo-list')}?message={mensaje}")

    except requests.RequestException as e:
        return HttpResponse(f"Error al conectar con la API: {e}", status=500)


def render_specific_list(request, title, data_type, queryset):
    """Función de ayuda para renderizar las listas específicas."""
    return render(request, 'pendientes/specific_list.html', {
        'title': title,
        'data_type': data_type,
        'items': queryset
    })

def todo_list_ids(request):
    """Lista de todos los pendientes (solo IDs de la base de datos local)."""
    return render_specific_list(request, 'Lista de Todos los Pendientes (IDs)', 'ID', Todo.objects.values_list('id', flat=True))

def todo_list_id_title(request):
    """Lista de todos los pendientes (IDs y Titles)."""
    return render_specific_list(request, 'Lista de Todos los Pendientes (ID y Título)', 'ID y Título', Todo.objects.values('id', 'title'))

def todo_list_unresolved(request):
    """Lista de todos los pendientes sin resolver (ID y Title)."""
    return render_specific_list(request, 'Pendientes sin Resolver (ID y Título)', 'ID y Título', Todo.objects.filter(completed=False).values('id', 'title'))

def todo_list_resolved(request):
    """Lista de todos los pendientes resueltos (ID y Title)."""
    return render_specific_list(request, 'Pendientes Resueltos (ID y Título)', 'ID y Título', Todo.objects.filter(completed=True).values('id', 'title'))

def todo_list_id_userid(request):
    """Lista de todos los pendientes (IDs y userID)."""
    return render_specific_list(request, 'Lista de Todos los Pendientes (ID y UserID)', 'ID y UserID', Todo.objects.values('id', 'user_id'))

def todo_list_resolved_id_userid(request):
    """Lista de todos los pendientes resueltos (ID y userID)."""
    return render_specific_list(request, 'Pendientes Resueltos (ID y UserID)', 'ID y UserID', Todo.objects.filter(completed=True).values('id', 'user_id'))
    
def todo_list_unresolved_id_userid(request):
    """Lista de todos los pendientes sin resolver (ID y userID)."""
    return render_specific_list(request, 'Pendientes sin Resolver (ID y UserID)', 'ID y UserID', Todo.objects.filter(completed=False).values('id', 'user_id'))


class TodoListView(ListView):
    """Vista para mostrar la lista completa de pendientes (CRUD)."""
    model = Todo
    template_name = 'pendientes/todo_list.html'
    context_object_name = 'todos'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message')
        return context

class TodoDetailView(DetailView):
    """Vista para ver el detalle de un pendiente."""
    model = Todo
    template_name = 'pendientes/todo_detail.html'

class TodoCreateView(CreateView):
    """Vista para crear un nuevo pendiente."""
    model = Todo
    form_class = TodoForm
    template_name = 'pendientes/todo_form.html'
    success_url = reverse_lazy('todo-list')

class TodoUpdateView(UpdateView):
    """Vista para actualizar un pendiente existente."""
    model = Todo
    form_class = TodoForm
    template_name = 'pendientes/todo_form.html'
    success_url = reverse_lazy('todo-list')

class TodoDeleteView(DeleteView):
    """Vista para eliminar un pendiente."""
    model = Todo
    template_name = 'pendientes/todo_confirm_delete.html'
    success_url = reverse_lazy('todo-list')