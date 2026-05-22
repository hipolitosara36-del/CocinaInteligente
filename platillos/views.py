from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Platillo, Categoria
from .forms import PlatilloForm


# ========== CRUD PLATILLOS ==========

def lista_platillos(request):
    """Listar todos los platillos"""
    platillos = Platillo.objects.all().order_by('categoria', 'nombre')
    return render(request, 'platillos/lista.html', {'platillos': platillos})


def detalle_platillo(request, id):
    """Ver detalle de un platillo"""
    platillo = get_object_or_404(Platillo, id=id)
    return render(request, 'platillos/detalle.html', {'platillo': platillo})


def crear_platillo(request):
    """Crear nuevo platillo"""
    if request.method == 'POST':
        form = PlatilloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Platillo creado exitosamente!')
            return redirect('lista_platillos')
    else:
        form = PlatilloForm()
    return render(request, 'platillos/form.html', {'form': form, 'titulo': 'Crear Platillo'})


def editar_platillo(request, id):
    """Editar platillo existente"""
    platillo = get_object_or_404(Platillo, id=id)
    if request.method == 'POST':
        form = PlatilloForm(request.POST, request.FILES, instance=platillo)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Platillo actualizado exitosamente!')
            return redirect('lista_platillos')
    else:
        form = PlatilloForm(instance=platillo)
    return render(request, 'platillos/form.html', {'form': form, 'titulo': 'Editar Platillo', 'platillo': platillo})


def eliminar_platillo(request, id):
    """Eliminar platillo"""
    platillo = get_object_or_404(Platillo, id=id)
    if request.method == 'POST':
        platillo.delete()
        messages.success(request, '¡Platillo eliminado exitosamente!')
        return redirect('lista_platillos')
    return render(request, 'platillos/confirm_delete.html', {'platillo': platillo})


# ========== CONSULTAS DE PLATILLOS ==========

def buscar_platillos(request):
    """Buscar platillos por nombre o palabra clave"""
    query = request.GET.get('q', '')
    if query:
        platillos = Platillo.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        platillos = Platillo.objects.none()

    context = {
        'platillos': platillos,
        'query': query,
        'titulo': 'Buscar Platillos',
        'descripcion': f'Resultados para: "{query}"' if query else 'Ingresa un término de búsqueda'
    }
    return render(request, 'platillos/buscar.html', context)


def filtrar_por_categoria(request):
    """Filtrar platillos por categoría"""
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')

    if categoria_id:
        platillos = Platillo.objects.filter(categoria_id=categoria_id)
        categoria_seleccionada = Categoria.objects.get(id=categoria_id)
    else:
        platillos = Platillo.objects.all()
        categoria_seleccionada = None

    context = {
        'platillos': platillos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'titulo': 'Filtrar por Categoría'
    }
    return render(request, 'platillos/filtrar.html', context)


def filtrar_por_disponibilidad(request):
    """Filtrar platillos por disponibilidad"""
    disponibilidad = request.GET.get('disponible', 'todos')

    if disponibilidad == 'disponible':
        platillos = Platillo.objects.filter(disponible=True)
        titulo = 'Platillos Disponibles'
    elif disponibilidad == 'no_disponible':
        platillos = Platillo.objects.filter(disponible=False)
        titulo = 'Platillos No Disponibles'
    else:
        platillos = Platillo.objects.all()
        titulo = 'Todos los Platillos'

    context = {
        'platillos': platillos,
        'disponibilidad_actual': disponibilidad,
        'titulo': titulo
    }
    return render(request, 'platillos/filtrar_disponibilidad.html', context)