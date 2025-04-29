from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .utils.conectar import conectar_db

# esto es nuevo
from .models import Post
from .forms import PosteoForm  # lo creamos abajo
from bson import ObjectId


# inicio vista actualizar
def listar_posteos(request):
    coleccion_trabajos = conectar_db()
    posteos = list(coleccion_trabajos.find().sort("fecha", -1))
    for post in posteos:
        post["id"] = str(post["_id"])
    return render(request, "principal/listar_posteos.html", {"posteos": posteos})


# fin vista actualizar

# inicio vista editar
from bson import ObjectId


def editar_posteo(request, id):
    coleccion_trabajos = conectar_db()
    posteo = coleccion_trabajos.find_one({"_id": ObjectId(id)})

    if not posteo:
        return redirect("listar_posteos")

    if request.method == "POST":
        titulo = request.POST["titulo"]
        descripcion = request.POST["descripcion"]
        categoria = request.POST["categoria"]
        fecha = request.POST["fecha"]

        coleccion_trabajos.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "categoria": categoria,
                    "fecha": fecha,
                }
            },
        )
        return redirect("listar_posteos")

    return render(request, "editar_posteo.html", {"posteo": posteo})


# fin vista editar


# inicio eliminar
def eliminar_posteo(request, id):
    coleccion_trabajos = conectar_db()
    posteo = coleccion_trabajos.find_one({"_id": ObjectId(id)})

    if not posteo:
        return redirect("listar_posteos")

    if request.method == "POST":
        coleccion_trabajos.delete_one({"_id": ObjectId(id)})
        return redirect("listar_posteos")

    return render(request, "confirmar_eliminar.html", {"posteo": posteo})


# fin eliminar

# fin de nuevo


# Create your views here.
def inicio(request):
    coleccion_trabajos = conectar_db()
    trabajos = list(coleccion_trabajos.find().sort("fecha", -1))

    categorias = coleccion_trabajos.find({}, {"_id": 0, "categoria": 1})
    categorias_unicas = {doc["categoria"] for doc in categorias if "categoria" in doc}
    categorias_unicas = sorted(categorias_unicas)

    return render(
        request, "index.html", {"trabajos": trabajos, "categorias": categorias_unicas}
    )


def portfolio(request):
    return render(request, "portfolio-details.html")


def service(request):
    return render(request, "service-details.html")


def starter(request):
    return render(request, "starter-page.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def panel_administracion(request):
    if request.method == "POST":
        titulo = request.POST["titulo"]
        descripcion = request.POST["descripcion"]
        categoria = request.POST["categoria"]
        imagenes = request.FILES.getlist("imagenes")
        fecha = request.POST["fecha"]

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        rutas_imagenes = []

        for imagen in imagenes:
            nombre_imagen = fs.save(imagen.name, imagen)

            ruta_completa = os.path.join(settings.MEDIA_URL, nombre_imagen)
            rutas_imagenes.append(ruta_completa)

            trabajo = {
                "titulo": titulo,
                "descripcion": descripcion,
                "categoria": categoria,
                "imagenes": rutas_imagenes,
                "fecha": fecha,
            }

            # Establecer conexion
            trabajos_coleccion = conectar_db()
            trabajos_coleccion.insert_one(trabajo)
            return redirect("inicio")

    return render(request, "panel-administracion.html")
