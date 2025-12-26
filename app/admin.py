from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    AreaEmpresa, Empresa, Entrada, Etapa, 
    Oportunidades, Salida, RegistroTrabajador,
    Idea, CVUsuario, Oferta, Necesidad
)


# -------------------------
# REGISTRO TRABAJADOR IMPORT/EXPORT
# -------------------------

class RegistroTrabajadorResource(resources.ModelResource):
    class Meta:
        model = RegistroTrabajador
        fields = ('id', 'usuario', 'descripcion', 'id_area')


class RegistroTrabajadorAdmin(ImportExportModelAdmin):
    resource_class = RegistroTrabajadorResource
    list_display = ("id", "usuario", "descripcion", "id_area")


# -------------------------
# EMPRESA
# -------------------------

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("id_empresa", "nombre", "calle", "comuna", "lat", "long")


# -------------------------
# AREA EMPRESA
# -------------------------

@admin.register(AreaEmpresa)
class AreaEmpresaAdmin(admin.ModelAdmin):
    list_display = ("id_area", "nombre", "productos", "id_empresa", "calle", "comuna", "lat", "long")


# -------------------------
# ETAPA
# -------------------------

@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ("id_etapa", "nombre", "fecha_inicio", "fecha_termino", "activo")


# -------------------------
# ENTRADA
# -------------------------

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ("id_entrada", "nombre", "fecha", "etapa", "usuario", "id_area")


# -------------------------
# SALIDA
# -------------------------

@admin.register(Salida)
class SalidaAdmin(admin.ModelAdmin):
    list_display = ("id_salida", "nombre", "fecha", "etapa", "usuario", "id_area")


# -------------------------
# OPORTUNIDADES
# -------------------------

@admin.register(Oportunidades)
class OportunidadesAdmin(admin.ModelAdmin):
    list_display = ("id_entrada", "nombre", "fecha", "etapa", "usuario", "id_area")


# -------------------------
# IDEA
# -------------------------

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("id_idea", "usuario", "empresa", "etapa", "texto", "fecha_creacion")


# -------------------------
# CV USUARIO
# -------------------------

@admin.register(CVUsuario)
class CVUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id", "usuario", "nombre_archivo",
        "palabra1", "palabra2", "palabra3", "palabra4", "palabra5",
        "palabra6", "palabra7", "palabra8", "palabra9", "palabra10",
        "linkedin_url", "timestamp"
    )


# -------------------------
# OFERTA
# -------------------------

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ("id_oferta", "usuario", "texto_oferta", "palabra1", "palabra2", "palabra3", "creado")


# -------------------------
# NECESIDAD
# -------------------------

@admin.register(Necesidad)
class NecesidadAdmin(admin.ModelAdmin):
    list_display = ("id_necesidad", "usuario", "texto_necesita", "palabra1", "palabra2", "palabra3", "creado")


# -------------------------
# REGISTRO TRABAJADOR
# -------------------------

admin.site.register(RegistroTrabajador, RegistroTrabajadorAdmin)
