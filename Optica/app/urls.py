from django.urls import path
from .views import *

urlpatterns = [
    path('', optica, name="optica"),
    path('editar/', editar, name="editar"),
    path('eliminar_sede/<int:id>/', eliminar_sede, name='eliminar_sede'),
    path('editar_sede/<int:id>/', editar_sede, name='editar_sede'),
    path('eliminar_imagen/<int:id>/', eliminar_imagen, name='eliminar_imagen'),
    path('editar_imagen/<int:id>/', editar_imagen, name='editar_imagen'),
    path('eliminar_red/<int:id>/', eliminar_red, name='eliminar_red'),
    path('editar_red/<int:id>/', editar_red, name='editar_red'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
