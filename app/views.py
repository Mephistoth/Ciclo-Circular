from email import message
from time import process_time_ns
from django.shortcuts import get_object_or_404, redirect, render
from .models import AreaEmpresa, Entrada, Etapa, RegistroTrabajador, Salida, Oportunidades, Empresa, Idea, CVUsuario, Oferta, Necesidad
from django.contrib import messages
from .forms import EntradaForm, SalidaForm, OportunidadForm
from user.models import Usuario
from wordcloud import WordCloud
from django.conf import settings
from openai import OpenAI
import matplotlib.pyplot as plt
from django.http import HttpResponse
import os
import io
import qrcode
import base64
import fitz  # PyMuPDF
import docx
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Create your views here.
def home(request):
    # obj_cliente = User.objects.only('rut').get(rut=rut)
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        return render(request, 'home.html', {'registros': registros})
    else:
        return render(request, 'home.html')

def autoDiagnostico(request, empresa_id=None):

    if not request.user.is_authenticated:
        return render(request, 'autodiagnostico/auto_diagnostico.html')

    empresas = Empresa.objects.all()  # Admin
    registros = RegistroTrabajador.objects.filter(usuario=request.user)

    empresa_seleccionada = None
    empresa_id_final = None

    # ADMIN: empresa seleccionada por URL
    if request.user.is_staff and empresa_id:
        empresa_seleccionada = Empresa.objects.filter(id_empresa=empresa_id).first()
        if empresa_seleccionada:
            empresa_id_final = empresa_seleccionada.id_empresa

    # USUARIO NORMAL: empresa desde su registro
    elif registros.exists():
        empresa_id_final = registros.first().id_area.id_empresa.id_empresa

    contexto = {
        'registros': registros,
        'empresas': empresas,
        'empresa_seleccionada': empresa_seleccionada,
        'empresa_id': empresa_id_final,
    }

    return render(request, 'autodiagnostico/auto_diagnostico.html', contexto)


def extraccionMateriaPrima(request):
    empresa_id = request.GET.get("empresa")
    empresa_seleccionada = None


    if empresa_id:
            empresa_seleccionada = Empresa.objects.get(id_empresa=empresa_id)

    empresas = Empresa.objects.all()

    if request.user.is_authenticated:

        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Extraccion materia prima")
        entradas = Entrada.objects.filter(usuario=request.user)
        # etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(activo=True)
        print("La id de la etapa es!!!!!!!!: ", etapa)

        # data = {

        #     'form' : EntradaForm(),
        #     'registros':registros,
        #     'entradas':entradas,
        #     'formSalida': SalidaForm()

        # }
        print(f"la id del usuario es!!!!!!!!:", request.user.id)
        formulario = EntradaForm()
        formularioSalida = SalidaForm()

        if request.method == 'POST':
            formulario = EntradaForm(request.POST)
            formularioSalida = SalidaForm(request.POST)

            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                formulario.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                formulario = EntradaForm()

            if formularioSalida.is_valid():
                post = formularioSalida.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                formularioSalida.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                formulario = SalidaForm()
        return render(request, 'autodiagnostico/extraccion/home_extraccion.html', {'form': formulario,
         'registros': registros, 'entradas': entradas, 'empresas': empresas, 'empresa_seleccionada': empresa_seleccionada})
    else:
        return render(request, 'autodiagnostico/extraccion/home_extraccion.html')


def agregarEntradaExtraccion(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.filter(nombre="Extraccion materia prima").first()
        areaTrabajador = RegistroTrabajador.objects.filter(usuario=request.user).values_list("id_area", flat=True).first()

        entradas = Entrada.objects.filter(usuario=request.user, etapa=etapa)

        data = {
            'form': EntradaForm(),
            'registros': registros,
            'entradas': entradas,
            'areaTrabajador': areaTrabajador,
        }

        # ======== AGREGAR ENTRADA ========
        if request.method == 'POST':
            formulario = EntradaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.usuario = request.user
                post.etapa = etapa
                post.id_area_id = areaTrabajador
                post.save()
                messages.success(request, "Entrada registrada con éxito.")
                return redirect('agregar_entrada_extraccion')
            else:
                data["form"] = formulario

        return render(request, 'autodiagnostico/extraccion/entrada/agregar_entrada.html', data)

    else:
        return render(request, 'autodiagnostico/extraccion/entrada/agregar_entrada.html')



def eliminarEntradaExtraccion(request, id):
    entrada = get_object_or_404(Entrada, id_entrada=id, usuario=request.user)
    entrada.delete()
    messages.success(request, "Entrada eliminada correctamente.")
    return redirect('agregar_entrada_extraccion')


def agregarSalidaExtraccion(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Extraccion materia prima")
        salidas = Salida.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': SalidaForm(),
            'registros': registros,
            'salidas': salidas

        }
        print(f"la id del usuario es!!!!!!!!:", request.user.id)

        if request.method == 'POST':
            formulario = SalidaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/extraccion/salida/agregar_salida.html', data)
    else:
        return render(request, 'autodiagnostico/extraccion/entrada/agregar_salida.html')

def eliminarSalidaExtraccion(request, id):
    salida = get_object_or_404(Salida, id_salida=id, usuario=request.user)
    salida.delete()
    messages.success(request, "Salida eliminada correctamente.")
    return redirect('agregar_salida_extraccion')


def agregarOportunidadExtraccion(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)

        # ← ARREGLO AQUÍ
        etapa = Etapa.objects.get(nombre="Extraccion materia prima").id_etapa
        areaTrabajador = RegistroTrabajador.objects.get(usuario=request.user).id_area_id

        oportunidades = Oportunidades.objects.filter(usuario=request.user)

        data = {
            'form': OportunidadForm(),
            'registros': registros,
            'oportunidad': oportunidades
        }

        if request.method == 'POST':
            formulario = OportunidadForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa              # ← AHORA SÍ ES UN ENTERO
                post.id_area_id = areaTrabajador   # ← AHORA SÍ ES UN ENTERO
                post.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                data["form"] = formulario

        return render(request,'autodiagnostico/extraccion/oportunidad/agregar_oportunidad.html', data)
    else:
        return render(request, 'autodiagnostico/extraccion/oportunidad/agregar_oportunidad.html')

def eliminarOportunidadExtraccion(request, id):
    oportunidad = get_object_or_404(Oportunidades, id_entrada=id, usuario=request.user)
    oportunidad.delete()
    messages.success(request, "Oportunidad eliminada correctamente.")
    return redirect('agregar_oportunidad_extraccion')




# Diseño y produccion

def diseño_Produccion(request):

    empresa_id = request.GET.get("empresa")
    empresa_seleccionada = None

    if empresa_id:
        empresa_seleccionada = Empresa.objects.filter(id_empresa=empresa_id).first()

    empresas = Empresa.objects.all()

    registros = RegistroTrabajador.objects.filter(usuario=request.user)

    data = {
        'registros': registros,
        'empresas': empresas,
        'empresa_seleccionada': empresa_seleccionada,
        'empresa_id': empresa_id,
    }

    return render(request, 'autodiagnostico/diseñoProduccion/home_diseño.html', data)



def agregarEntradaDiseño(request):
    if request.user.is_authenticated:

        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Diseño y produccion")
        entradas = Entrada.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)
        # etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(activo=True)
        data = {

            'form': EntradaForm(),
            'registros': registros,
            'entradas': entradas

        }
        if request.method == 'POST':
            formulario = EntradaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/diseñoProduccion/entrada/agregar_entrada.html', data)
    else:
        return render(request, 'autodiagnostico/diseñoProduccion/entrada/agregar_entrada.html')


def eliminarEntradaDiseño(request, id):
    entrada = get_object_or_404(Entrada, id_entrada=id, usuario=request.user)
    entrada.delete()
    messages.success(request, "Entrada eliminada correctamente.")
    return redirect('agregar_entrada_diseño')


def agregarSalidaDiseño(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Diseño y produccion")
        salidas = Salida.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': SalidaForm(),
            'registros': registros,
            'salidas': salidas

        }

        if request.method == 'POST':
            formulario = SalidaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/diseñoProduccion/salida/agregar_salida.html', data)
    else:
        return render(request, 'autodiagnostico/diseñoProduccion/entrada/agregar_salida.html')


def eliminarSalidaDiseño(request, id):
    salida = get_object_or_404(Salida, id_salida=id, usuario=request.user)
    salida.delete()
    messages.success(request, "Salida eliminada correctamente.")
    return redirect('agregar_salida_diseño')


def agregarOportunidadDiseño(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Diseño y produccion")
        oportunidades = Oportunidades.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': OportunidadForm(),
            'registros': registros,
            'oportunidad': oportunidades

        }

        if request.method == 'POST':
            formulario = OportunidadForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/diseñoProduccion/oportunidad/agregar_oportunidad.html', data)
    else:
        return render(request, 'autodiagnostico/diseñoProduccion/oportunidad/agregar_oportunidad.html')


def eliminarOportunidadDiseño(request, id):
    oportunidad = get_object_or_404(Oportunidades, id_entrada=id, usuario=request.user)
    oportunidad.delete()
    messages.success(request, "Oportunidad eliminada correctamente.")
    return redirect('agregar_oportunidad_diseño')



# logistica

def logistica(request):
    empresa_id = request.GET.get("empresa")
    empresa_seleccionada = None

    if empresa_id:
        empresa_seleccionada = Empresa.objects.filter(id_empresa=empresa_id).first()

    empresas = Empresa.objects.all()

    registros = RegistroTrabajador.objects.filter(usuario=request.user)

    data = {  
            'registros': registros, 
            'empresas': empresas,
            'empresa_seleccionada': empresa_seleccionada,
            'empresa_id': empresa_id,
    }

    return render(request,'autodiagnostico/logistica/home_logistica.html', data)


def agregarEntradaLogistica(request):
    if request.user.is_authenticated:

        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Logistica")
        entradas = Entrada.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)
        # etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(activo=True)
        data = {

            'form': EntradaForm(),
            'registros': registros,
            'entradas': entradas

        }
        if request.method == 'POST':
            formulario = EntradaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/logistica/entrada/agregar_entrada.html', data)
    else:
        return render(request, 'autodiagnostico/logistica/entrada/agregar_entrada.html')


def eliminarEntradaLogistica(request, id):
    entrada = get_object_or_404(Entrada, id_entrada=id, usuario=request.user)
    entrada.delete()
    messages.success(request, "Entrada eliminada correctamente.")
    return redirect('agregar_entrada_logistica')


def agregarSalidaLogistica(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Logistica")
        salidas = Salida.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': SalidaForm(),
            'registros': registros,
            'salidas': salidas

        }

        if request.method == 'POST':
            formulario = SalidaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/logistica/salida/agregar_salida.html', data)
    else:
        return render(request, 'autodiagnostico/logistica/entrada/agregar_salida.html')


def eliminarSalidaLogistica(request, id):
    salida = get_object_or_404(Salida, id_salida=id, usuario=request.user)
    salida.delete()
    messages.success(request, "Salida eliminada correctamente.")
    return redirect('agregar_salida_logistica')



def agregarOportunidadLogistica(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Logistica")
        oportunidades = Oportunidades.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': OportunidadForm(),
            'registros': registros,
            'oportunidad': oportunidades

        }

        if request.method == 'POST':
            formulario = OportunidadForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/logistica/oportunidad/agregar_oportunidad.html', data)
    else:
        return render(request, 'autodiagnostico/logistica/oportunidad/agregar_oportunidad.html')

def eliminarOportunidadLogistica(request, id):
    oportunidad = get_object_or_404(Oportunidades, id_entrada=id, usuario=request.user)
    oportunidad.delete()
    messages.success(request, "Oportunidad eliminada correctamente.")
    return redirect('agregar_oportunidad_logistica')



#compra

def compra(request):
    empresa_id = request.GET.get("empresa")
    empresa_seleccionada = None

    if empresa_id:
        empresa_seleccionada = Empresa.objects.filter(id_empresa=empresa_id).first()

    empresas = Empresa.objects.all()

    registros = RegistroTrabajador.objects.filter(usuario=request.user)

    data = {  
            'registros': registros, 
            'empresas': empresas,
            'empresa_seleccionada': empresa_seleccionada,
            'empresa_id': empresa_id,
    }

    return render(request,'autodiagnostico/compra/home_compra.html', data)


def agregarEntradaCompra(request):
    if request.user.is_authenticated:

        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Compra")
        entradas = Entrada.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)
        # etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(activo=True)
        data = {

            'form': EntradaForm(),
            'registros': registros,
            'entradas': entradas

        }
        if request.method == 'POST':
            formulario = EntradaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/compra/entrada/agregar_entrada.html', data)
    else:
        return render(request, 'autodiagnostico/compra/entrada/agregar_entrada.html')   

def eliminarEntradaCompra(request, id):
    entrada = get_object_or_404(Entrada, id_entrada=id, usuario=request.user)
    entrada.delete()
    messages.success(request, "Entrada eliminada correctamente.")
    return redirect('agregar_entrada_compra')


def agregarSalidaCompra(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Compra")
        salidas = Salida.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': SalidaForm(),
            'registros': registros,
            'salidas': salidas

        }

        if request.method == 'POST':
            formulario = SalidaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/compra/salida/agregar_salida.html', data)
    else:
        return render(request,'autodiagnostico/compra/salida/agregar_salida.html')  


def eliminarSalidaCompra(request, id):
    salida = get_object_or_404(Salida, id_salida=id, usuario=request.user)
    salida.delete()
    messages.success(request, "Salida eliminada correctamente.")
    return redirect('agregar_salida_compra')



def agregarOportunidadCompra(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Compra")
        oportunidades = Oportunidades.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': OportunidadForm(),
            'registros': registros,
            'oportunidad': oportunidades

        }

        if request.method == 'POST':
            formulario = OportunidadForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/compra/oportunidad/agregar_oportunidad.html', data)
    else:
        return render(request, 'autodiagnostico/compra/oportunidad/agregar_oportunidad.html') 

def eliminarOportunidadCompra(request, id):
    oportunidad = get_object_or_404(Oportunidades, id_entrada=id, usuario=request.user)
    oportunidad.delete()
    messages.success(request, "Oportunidad eliminada correctamente.")
    return redirect('agregar_oportunidad_compra')



#Uso consumo

def usoConsumo(request):
    empresa_id = request.GET.get("empresa")
    empresa_seleccionada = None

    if empresa_id:
        empresa_seleccionada = Empresa.objects.filter(id_empresa=empresa_id).first()

    empresas = Empresa.objects.all()

    registros = RegistroTrabajador.objects.filter(usuario=request.user)

    data = {  
            'registros': registros, 
            'empresas': empresas,
            'empresa_seleccionada': empresa_seleccionada,
            'empresa_id': empresa_id,
    }

    return render(request,'autodiagnostico/usoConsumo/home_usoConsumo.html', data)        


def agregarEntradaUso(request):
    if request.user.is_authenticated:

        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Uso consumo")
        entradas = Entrada.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)
        # etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(activo=True)
        data = {

            'form': EntradaForm(),
            'registros': registros,
            'entradas': entradas

        }
        if request.method == 'POST':
            formulario = EntradaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/usoConsumo/entrada/agregar_entrada.html', data)
    else:
        return render(request, 'autodiagnostico/usoConsumo/entrada/agregar_entrada.html')    


def eliminarEntradaUsoConsumo(request, id):
    entrada = get_object_or_404(Entrada, id_entrada=id, usuario=request.user)
    entrada.delete()
    messages.success(request, "Entrada eliminada correctamente.")
    return redirect('agregar_entrada_uso_consumo')


def agregarSalidaUso(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Uso consumo")
        salidas = Salida.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': SalidaForm(),
            'registros': registros,
            'salidas': salidas

        }

        if request.method == 'POST':
            formulario = SalidaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/usoConsumo/salida/agregar_salida.html', data)
    else:
        return render(request,'autodiagnostico/usoConsumo/salida/agregar_salida.html')       


def eliminarSalidaUso(request, id):
    salida = get_object_or_404(Salida, id_salida=id, usuario=request.user)
    salida.delete()
    messages.success(request, "Salida eliminada correctamente.")
    return redirect('agregar_salida_uso')



def agregarOportunidadUso(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Uso consumo")
        oportunidades = Oportunidades.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': OportunidadForm(),
            'registros': registros,
            'oportunidad': oportunidades

        }

        if request.method == 'POST':
            formulario = OportunidadForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/usoConsumo/oportunidad/agregar_oportunidad.html', data)
    else:
        return render(request, 'autodiagnostico/usoConsumo/oportunidad/agregar_oportunidad.html')   

def eliminarOportunidadUso(request, id):
    oportunidad = get_object_or_404(Oportunidades, id_entrada=id, usuario=request.user)
    oportunidad.delete()
    messages.success(request, "Oportunidad eliminada correctamente.")
    return redirect('agregar_oportunidad_uso')


# Fin de vida

def finVida(request):
    empresa_id = request.GET.get("empresa")
    empresa_seleccionada = None

    if empresa_id:
        empresa_seleccionada = Empresa.objects.filter(id_empresa=empresa_id).first()

    empresas = Empresa.objects.all()

    registros = RegistroTrabajador.objects.filter(usuario=request.user)

    data = {  
            'registros': registros, 
            'empresas': empresas,
            'empresa_seleccionada': empresa_seleccionada,
            'empresa_id': empresa_id,
    }

    return render(request,'autodiagnostico/finVida/home_finVida.html', data)


def agregarEntradaFin(request):
    if request.user.is_authenticated:

        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Fin de vida")
        entradas = Entrada.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)
        # etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(activo=True)
        data = {

            'form': EntradaForm(),
            'registros': registros,
            'entradas': entradas

        }
        if request.method == 'POST':
            formulario = EntradaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Entrada Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/finVida/entrada/agregar_entrada.html', data)
    else:
        return render(request, 'autodiagnostico/finVida/entrada/agregar_entrada.html')  


def eliminarEntradaFinVida(request, id):
    entrada = get_object_or_404(Entrada, id_entrada=id, usuario=request.user)
    entrada.delete()
    messages.success(request, "Entrada eliminada correctamente.")
    return redirect('agregar_entrada_fin_vida')


def agregarSalidaFin(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Fin de vida")
        salidas = Salida.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': SalidaForm(),
            'registros': registros,
            'salidas': salidas

        }

        if request.method == 'POST':
            formulario = SalidaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/finVida/salida/agregar_salida.html', data)
    else:
        return render(request,'autodiagnostico/finVida/salida/agregar_salida.html') 


def eliminarSalidaFinVida(request, id):
    salida = get_object_or_404(Salida, id_salida=id, usuario=request.user)
    salida.delete()
    messages.success(request, "Salida eliminada correctamente.")
    return redirect('agregar_salida_fin_vida')



def agregarOportunidadFin(request):
    if request.user.is_authenticated:
        registros = RegistroTrabajador.objects.filter(usuario=request.user)
        etapa = Etapa.objects.values_list("id_etapa", flat=True).filter(nombre="Fin de vida")
        oportunidades = Oportunidades.objects.filter(usuario=request.user)
        areaTrabajador = RegistroTrabajador.objects.values_list("id_area", flat=True).filter(usuario = request.user)

        data = {

            'form': OportunidadForm(),
            'registros': registros,
            'oportunidad': oportunidades

        }

        if request.method == 'POST':
            formulario = OportunidadForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                post = formulario.save(commit=False)
                post.nombre = request.POST["nombre"]
                post.usuario_id = request.user.id
                post.etapa_id = etapa
                post.id_area_id = areaTrabajador
                formulario.save()
                messages.success(request, "Salida Registrada con exito")
            else:
                data["form"] = formulario
        return render(request,'autodiagnostico/finVida/oportunidad/agregar_oportunidad.html', data)
    else:
        return render(request, 'autodiagnostico/finVida/oportunidad/agregar_oportunidad.html') 

def eliminarOportunidadFinVida(request, id):

    oportunidad = get_object_or_404(Oportunidades, id_entrada=id, usuario=request.user)
    oportunidad.delete()
    messages.success(request, "Oportunidad eliminada correctamente.")
    return redirect('agregar_oportunidad_fin_vida')


def ingresar_ideas(request, etapa_id=None):
    registros = RegistroTrabajador.objects.filter(usuario=request.user)
    registro = registros.first()

    etapas = Etapa.objects.filter(activo=True)
    etapa = None
    mensaje = None  # <-- para mostrar mensaje de éxito

    if etapa_id:
        etapa = get_object_or_404(Etapa, id_etapa=etapa_id)

        if request.method == "POST":
            texto = request.POST.get("texto")
            if not texto or texto.strip() == "":
                mensaje = "Debe ingresar una idea."
            else:
                Idea.objects.create(
                    usuario=request.user,
                    empresa=registro.id_area.id_empresa,
                    etapa=etapa,
                    texto=texto
                )
                mensaje = "Idea guardada correctamente."

    return render(request, 'ideas/ingresar_ideas.html', {
        'registros': registros,
        'etapas': etapas,
        'etapa': etapa,
        'mensaje': mensaje
    })


def mi_perfil(request):
    registros = RegistroTrabajador.objects.filter(usuario=request.user)

    # Obtener CV actual
    cv = CVUsuario.objects.filter(usuario=request.user).first()
    qr_base64 = None

    # --------------------------
    # PROCESAR FORMULARIOS POST
    # --------------------------
    if request.method == "POST":

        # --------------------------
        # 1. Actualizar URL de LinkedIn
        # --------------------------
        linkedin_url = request.POST.get("linkedin_url")
        if linkedin_url and cv:
            cv.linkedin_url = linkedin_url.strip()
            cv.save()
            messages.success(request, "URL de LinkedIn actualizada correctamente.")
            return redirect("mi_perfil")

        # --------------------------
        # 2. Guardar QR generado desde URL (nuevo botón)
        # action = save_qr
        # --------------------------
        if request.POST.get("action") == "save_qr" and cv and cv.linkedin_url:
            qr = qrcode.make(cv.linkedin_url)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            cv.linkedin_qr = buffer.getvalue()
            cv.save()

            messages.success(request, "QR de LinkedIn guardado correctamente.")
            return redirect("mi_perfil")

        # --------------------------
        # 3. Subir/Cambiar QR manualmente
        # --------------------------
        linkedin_qr_file = request.FILES.get("linkedin_qr")
        if linkedin_qr_file and cv:
            qr_bytes = linkedin_qr_file.read()
            cv.linkedin_qr = qr_bytes
            cv.save()
            messages.success(request, "QR de LinkedIn actualizado correctamente.")
            return redirect("mi_perfil")

        # --------------------------
        # 4. Subir/Cambiar CV completo
        # --------------------------
        archivo = request.FILES.get("archivo")
        if archivo:
            file_bytes = archivo.read()
            file_like = io.BytesIO(file_bytes)
            file_like.name = archivo.name

            # Extraer texto del CV
            texto = leer_archivo(file_like)

            # Generar palabras clave con ChatGPT
            try:
                palabras_generadas = generar_10_palabras_clave(texto)
            except Exception as e:
                print("ERROR al generar palabras clave:", e)
                palabras_generadas = [None] * 10

            # Eliminar CV anterior
            CVUsuario.objects.filter(usuario=request.user).delete()

            # Guardar nuevo CV
            cv = CVUsuario.objects.create(
                usuario=request.user,
                archivo=file_bytes,
                nombre_archivo=archivo.name,
                palabra1=palabras_generadas[0],
                palabra2=palabras_generadas[1],
                palabra3=palabras_generadas[2],
                palabra4=palabras_generadas[3],
                palabra5=palabras_generadas[4],
                palabra6=palabras_generadas[5],
                palabra7=palabras_generadas[6],
                palabra8=palabras_generadas[7],
                palabra9=palabras_generadas[8],
                palabra10=palabras_generadas[9],
            )

            messages.success(request, "CV actualizado correctamente.")
            return redirect("mi_perfil")

        # Si no llega nada válido
        messages.error(request, "Debe seleccionar un archivo o ingresar datos válidos.")
        return redirect("mi_perfil")

    # --------------------------
    # PREPARAR PALABRAS CLAVE Y QR
    # --------------------------
    palabras = []
    if cv:
        palabras = [
            cv.palabra1, cv.palabra2, cv.palabra3, cv.palabra4, cv.palabra5,
            cv.palabra6, cv.palabra7, cv.palabra8, cv.palabra9, cv.palabra10
        ]
        palabras = [p for p in palabras if p]

        # Convertir QR a Base64 para mostrarlo
        if cv.linkedin_qr:
            qr_base64 = base64.b64encode(cv.linkedin_qr).decode("utf-8")

    # --------------------------
    # Palabras última oferta
    # --------------------------
    ultima_oferta = Oferta.objects.filter(usuario=request.user).last()
    palabras_oferta = None
    if ultima_oferta:
        palabras_oferta = [
            ultima_oferta.palabra1,
            ultima_oferta.palabra2,
            ultima_oferta.palabra3
        ]
        palabras_oferta = [p for p in palabras_oferta if p]

    # --------------------------
    # Palabras última necesidad
    # --------------------------
    ultima_necesidad = Necesidad.objects.filter(usuario=request.user).last()
    palabras_necesidad = None
    if ultima_necesidad:
        palabras_necesidad = [
            ultima_necesidad.palabra1,
            ultima_necesidad.palabra2,
            ultima_necesidad.palabra3
        ]
        palabras_necesidad = [p for p in palabras_necesidad if p]

    # --------------------------
    # Renderizar template final
    # --------------------------
    return render(request, 'mi_perfil/mi_perfil.html', {
        "registros": registros,
        "cv": cv,
        "palabras": palabras,
        "palabras_oferta": palabras_oferta,
        "palabras_necesidad": palabras_necesidad,
        "ultima_oferta": ultima_oferta,
        "ultima_necesidad": ultima_necesidad,
        "qr_base64": qr_base64,
    })

def subir_cv(request):
    if not request.user.is_authenticated:
        return redirect("login")

    usuario = request.user

    if request.method == "POST":
        archivo = request.FILES.get("archivo")
        if not archivo:
            messages.error(request, "No se subió ningún archivo.")
            return redirect("subir_cv")

        # Leer archivo y convertir a Base64
        file_bytes = archivo.read()

        # Crear file-like para extraer texto
        file_like = io.BytesIO(file_bytes)
        file_like.name = archivo.name
        texto = leer_archivo(file_like)

        # Generar 10 palabras clave
        try:
            palabras = generar_10_palabras_clave(texto)
        except Exception as e:
            print(f"ERROR GENERANDO PALABRAS CLAVE: {e}")
            messages.error(request, f"Error al generar palabras clave: {e}")
            palabras = [None] * 10

        # Mantener solo 1 CV por usuario
        CVUsuario.objects.filter(usuario=usuario).delete()

        # Guardar en BD
        CVUsuario.objects.create(
            usuario=usuario,
            archivo=file_bytes,
            nombre_archivo=archivo.name,
            palabra1=palabras[0],
            palabra2=palabras[1],
            palabra3=palabras[2],
            palabra4=palabras[3],
            palabra5=palabras[4],
            palabra6=palabras[5],
            palabra7=palabras[6],
            palabra8=palabras[7],
            palabra9=palabras[8],
            palabra10=palabras[9],
        )

        messages.success(request, "CV subido y procesado correctamente.")
        return redirect("mi_perfil")

    return render(request, "mi_perfil/subir_cv.html")

def leer_archivo(file_like):
    ext = file_like.name.split(".")[-1].lower()

    try:
        if ext == "txt":
            return file_like.read().decode("utf-8", errors="ignore")

        elif ext == "docx":
            doc = docx.Document(file_like)
            return "\n".join([p.text for p in doc.paragraphs])

        elif ext == "pdf":
            file_like.seek(0)
            texto = ""
            with fitz.open(stream=file_like.read(), filetype="pdf") as pdf:
                for pagina in pdf:
                    texto += pagina.get_text()
            return texto

    except Exception as e:
        return f"Error al leer archivo: {e}"

    return ""

def generar_10_palabras_clave(texto):

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Devuelve SOLO una lista de 10 palabras clave, separadas por comas."
            },
            {
                "role": "user",
                "content": f"Extrae exactamente 10 palabras clave del siguiente texto. Respóndelas separadas por comas.\n\n{texto[:3500]}"
            }
        ]
    )

    # IMPORTANTE: acceso correcto al mensaje
    content = completion.choices[0].message.content

    # Procesar palabras
    palabras = [p.strip() for p in content.replace("\n", ",").split(",") if p.strip()]

    # asegurar 10
    palabras = palabras[:10]
    while len(palabras) < 10:
        palabras.append(None)

    return palabras

def generar_3_palabras_clave(texto):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Devuelve SOLO una lista de 3 palabras clave separadas por comas."
            },
            {
                "role": "user",
                "content": f"Extrae exactamente 3 palabras clave del siguiente texto. Respóndelas separadas por comas.\n\n{texto[:3000]}"
            }
        ]
    )

    content = completion.choices[0].message.content
    palabras = [p.strip() for p in content.replace("\n", ",").split(",") if p.strip()]

    # asegurar 3
    palabras = palabras[:3]
    while len(palabras) < 3:
        palabras.append(None)

    return palabras

def guardar_oferta(request):
    if request.method != "POST":
        return redirect("mi_perfil")

    texto = request.POST.get("texto_oferta")

    if not texto or texto.strip() == "":
        messages.error(request, "Debe ingresar un texto para la oferta.")
        return redirect("mi_perfil")

    # Generar palabras clave
    try:
        palabras = generar_3_palabras_clave(texto)
    except Exception as e:
        print("ERROR al generar palabras clave:", e)
        palabras = [None, None, None]

    # Obtener o crear la oferta del usuario
    oferta, created = Oferta.objects.get_or_create(usuario=request.user)

    # Sobrescribir datos
    oferta.texto_oferta = texto
    oferta.palabra1 = palabras[0]
    oferta.palabra2 = palabras[1]
    oferta.palabra3 = palabras[2]
    oferta.save()

    messages.success(request, "Oferta guardada correctamente.")
    return redirect("mi_perfil")


def guardar_necesidad(request):
    if request.method != "POST":
        return redirect("mi_perfil")

    texto = request.POST.get("texto_necesita")

    if not texto or texto.strip() == "":
        messages.error(request, "Debe ingresar un texto para la necesidad.")
        return redirect("mi_perfil")

    # Generar palabras clave
    try:
        palabras = generar_3_palabras_clave(texto)
    except Exception as e:
        print("ERROR al generar palabras clave:", e)
        palabras = [None, None, None]

    # Obtener o crear la necesidad del usuario
    necesidad, created = Necesidad.objects.get_or_create(usuario=request.user)

    # Sobrescribir datos
    necesidad.texto_necesita = texto
    necesidad.palabra1 = palabras[0]
    necesidad.palabra2 = palabras[1]
    necesidad.palabra3 = palabras[2]
    necesidad.save()

    messages.success(request, "Necesidad guardada correctamente.")
    return redirect("mi_perfil")

def editar_palabras_clave(request):
    if request.method == "POST":
        usuario = request.user

        # Obtener CV
        cv = get_object_or_404(CVUsuario, usuario=usuario)

        # Recibir palabras separadas por coma
        texto = request.POST.get("palabras", "")
        lista_palabras = [p.strip() for p in texto.split(",") if p.strip()]

        # Limitar a máximo 10
        lista_palabras = lista_palabras[:10]

        # Rellenar con None hasta 10
        while len(lista_palabras) < 10:
            lista_palabras.append(None)

        # Asignar una por una
        cv.palabra1 = lista_palabras[0]
        cv.palabra2 = lista_palabras[1]
        cv.palabra3 = lista_palabras[2]
        cv.palabra4 = lista_palabras[3]
        cv.palabra5 = lista_palabras[4]
        cv.palabra6 = lista_palabras[5]
        cv.palabra7 = lista_palabras[6]
        cv.palabra8 = lista_palabras[7]
        cv.palabra9 = lista_palabras[8]
        cv.palabra10 = lista_palabras[9]

        cv.save()

        messages.success(request, "Palabras clave actualizadas correctamente.")
        return redirect("mi_perfil")

    return redirect("mi_perfil")