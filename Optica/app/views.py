from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import ImagenCarrusel, RedSocial, Sede


def es_admin(user):
    return user.is_authenticated and user.is_staff

def optica(request):
    imagenes = ImagenCarrusel.objects.all()
    redes = RedSocial.objects.all()
    sedes = Sede.objects.all().order_by('fecha', 'hora')

    return render(request, 'app/Optica.html', {
        'imagenes': imagenes,
        'redes': redes,
        'sedes': sedes
    })

@login_required(login_url='login')
def editar(request):

    if request.method == 'POST':

        # ===== IMAGEN =====
        if request.FILES.get('imagen'):
            if request.POST.get('imagen_id'):
                img = ImagenCarrusel.objects.get(id=request.POST.get('imagen_id'))
                img.imagen = request.FILES['imagen']
                img.save()
            else:
                ImagenCarrusel.objects.create(imagen=request.FILES['imagen'])

        # ===== RED SOCIAL =====
        if request.POST.get('nombre_red'):
            nombre = request.POST.get('nombre_red')
            link = request.POST.get('link_red')

            if "whatsapp" in nombre.lower() or "ws" in nombre.lower():
                link = f"https://wa.me/{link}"

            if request.POST.get('red_id'):
                red = RedSocial.objects.get(id=request.POST.get('red_id'))
                red.nombre = nombre
                red.link = link
                red.save()
            else:
                RedSocial.objects.create(nombre=nombre, link=link)

        # ===== SEDE =====
        if request.POST.get('ubicacion'):
            if request.POST.get('sede_id'):
                sede = Sede.objects.get(id=request.POST.get('sede_id'))
                sede.ubicacion = request.POST.get('ubicacion')
                sede.fecha = request.POST.get('fecha')
                sede.hora = request.POST.get('hora')
                sede.horatermino = request.POST.get('horatermino')
                sede.save()
            else:
                Sede.objects.create(
                    ubicacion=request.POST.get('ubicacion'),
                    fecha=request.POST.get('fecha'),
                    hora=request.POST.get('hora'),
                    horatermino=request.POST.get('horatermino')
                )

        return redirect('editar')

    return render(request, 'app/editar_vista.html', {
        'sedes': Sede.objects.all(),
        'imagenes': ImagenCarrusel.objects.all(),
        'redes': RedSocial.objects.all()
    })

@user_passes_test(es_admin, login_url='login')
def eliminar_sede(request, id):
    sede = get_object_or_404(Sede, id=id)
    sede.delete()
    return redirect('editar')

@user_passes_test(es_admin, login_url='login')
def editar_sede(request, id):
    sede = get_object_or_404(Sede, id=id)

    if request.method == "POST":
        sede.ubicacion = request.POST.get('ubicacion')
        sede.fecha = request.POST.get('fecha')
        sede.hora = request.POST.get('hora')
        sede.horatermino = request.POST.get('horatermino')
        sede.save()
        return redirect('editar')

    return render(request, 'app/editar_sede.html', {'sede': sede})

@user_passes_test(es_admin, login_url='login')
def eliminar_imagen(request, id):
    img = get_object_or_404(ImagenCarrusel, id=id)
    img.delete()
    return redirect('editar')


@user_passes_test(es_admin, login_url='login')
def editar_imagen(request, id):
    img = get_object_or_404(ImagenCarrusel, id=id)

    if request.method == "POST":
        if request.FILES.get('imagen'):
            img.imagen = request.FILES['imagen']
            img.save()
        return redirect('editar')

    return render(request, 'app/editar_imagen.html', {'img': img})


# ===== RED SOCIAL =====
@user_passes_test(es_admin, login_url='login')
def eliminar_red(request, id):
    red = get_object_or_404(RedSocial, id=id)
    red.delete()
    return redirect('editar')


@user_passes_test(es_admin, login_url='login')
def editar_red(request, id):
    red = get_object_or_404(RedSocial, id=id)

    if request.method == "POST":
        red.nombre = request.POST.get('nombre_red')
        link = request.POST.get('link_red')

        if "whatsapp" in red.nombre.lower() or "ws" in red.nombre.lower():
            link = f"https://wa.me/{link}"

        red.link = link
        red.save()

        return redirect('editar')

    return render(request, 'app/editar_red.html', {'red': red})

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('optica')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('optica')