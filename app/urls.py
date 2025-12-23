from django.contrib import admin
from django.urls import  path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('auto_diagnostico', autoDiagnostico, name="auto_diagnostico"),
    path('auto_diagnostico/<int:empresa_id>/', autoDiagnostico, name="auto_diagnostico_empresa"),
    #etapa extraccion materia prima
    path('extraccion_materiaPrima', extraccionMateriaPrima, name="extraccion_materiaPrima"),
    path('agregar_entrada_extraccion', agregarEntradaExtraccion, name="agregar_entrada_extraccion"),
    path('agregar_salida_extraccion', agregarSalidaExtraccion, name="agregar_salida_extraccion"),
    path('agregar_oportunidad_extraccion', agregarOportunidadExtraccion, name="agregar_oportunidad_extraccion"),
    path('eliminar_entrada_extraccion/<int:id>/', eliminarEntradaExtraccion, name='eliminar_entrada_extraccion'),
    path('eliminar_oportunidad_extraccion/<int:id>/', eliminarOportunidadExtraccion, name='eliminar_oportunidad_extraccion'),
    path('eliminar_salida_extraccion/<int:id>/', eliminarSalidaExtraccion, name='eliminar_salida_extraccion'),
    
    #etapa diseño y produccion
    path('diseño_Produccion', diseño_Produccion, name="diseño_Produccion"),
    path('agregar_entrada_diseño', agregarEntradaDiseño, name="agregar_entrada_diseño"),
    path('agregar_salida_diseño', agregarSalidaDiseño, name="agregar_salida_diseño"),
    path('agregar_oportunidad_diseño', agregarOportunidadDiseño, name="agregar_oportunidad_diseño"),
    path('eliminar_entrada_diseño/<int:id>/', eliminarEntradaDiseño, name='eliminar_entrada_diseño'),
    path('eliminar_oportunidad_diseño/<int:id>/', eliminarOportunidadDiseño, name='eliminar_oportunidad_diseño'),
    path('eliminar_salida_diseño/<int:id>/', eliminarSalidaDiseño, name='eliminar_salida_diseño'),

    #Etapa logistica
    path('logistica', logistica, name="logistica"),
    path('agregar_entrada_logistica', agregarEntradaLogistica, name="agregar_entrada_logistica"),
    path('agregar_salida_logistica', agregarSalidaLogistica, name="agregar_salida_logistica"),
    path('agregar_oportunidad_logistica', agregarOportunidadLogistica, name="agregar_oportunidad_logistica"),
    path('eliminar_entrada_logistica/<int:id>/', eliminarEntradaLogistica, name='eliminar_entrada_logistica'),
    path('eliminar_oportunidad_logistica/<int:id>/', eliminarOportunidadLogistica, name='eliminar_oportunidad_logistica'),
    path('eliminar_salida_logistica/<int:id>/', eliminarSalidaLogistica, name='eliminar_salida_logistica'),

    #Etapa compra
    path('compra', compra, name="compra"),
    path('agregar_entrada_compra', agregarEntradaCompra, name="agregar_entrada_compra"),
    path('agregar_salida_compra', agregarSalidaCompra, name="agregar_salida_compra"),
    path('agregar_oportunidad_compra', agregarOportunidadCompra, name="agregar_oportunidad_compra"),
    path('eliminar_entrada_compra/<int:id>/', eliminarEntradaCompra, name='eliminar_entrada_compra'),
    path('eliminar_oportunidad_compra/<int:id>/', eliminarOportunidadCompra, name='eliminar_oportunidad_compra'),
    path('eliminar_salida_compra/<int:id>/', eliminarSalidaCompra, name='eliminar_salida_compra'),

    #Etapa Uso Consumo
    path('uso_consumo', usoConsumo, name="uso_consumo"),
    path('agregar_entrada_uso', agregarEntradaUso, name="agregar_entrada_uso"),
    path('agregar_salida_uso', agregarSalidaUso, name="agregar_salida_uso"),
    path('agregar_oportunidad_uso', agregarOportunidadUso, name="agregar_oportunidad_uso"),
    path('eliminar_entrada_uso_consumo/<int:id>/', eliminarEntradaUsoConsumo, name='eliminar_entrada_uso_consumo'),
    path('eliminar_oportunidad_uso/<int:id>/', eliminarOportunidadUso, name='eliminar_oportunidad_uso'),
    path('eliminar_salida_uso_consumo/<int:id>/', eliminarSalidaUso, name='eliminar_salida_uso_consumo'),

    #Etapa fin de vida
    path('fin_vida', finVida, name="fin_vida"),
    path('agregar_entrada_fin', agregarEntradaFin, name="agregar_entrada_fin"),
    path('agregar_salida_fin', agregarSalidaFin, name="agregar_salida_fin"),
    path('agregar_oportunidad_fin', agregarOportunidadFin, name="agregar_oportunidad_fin"),
    path('eliminar_entrada_fin_vida/<int:id>/', eliminarEntradaFinVida, name='eliminar_entrada_fin_vida'),
    path('eliminar_oportunidad_fin_vida/<int:id>/', eliminarOportunidadFinVida, name='eliminar_oportunidad_fin_vida'),
    path('eliminar_salida_fin_vida/<int:id>/', eliminarSalidaFinVida, name='eliminar_salida_fin_vida'),

    #ideas
    path('ideas/', ingresar_ideas, name="ingresar_ideas"),
    path('ideas/<int:etapa_id>/', ingresar_ideas, name='ingresar_idea'),

    #datos de usuario
    path('mi_perfil', mi_perfil, name="mi_perfil"),
    path('mi-cv/', subir_cv, name='subir_cv'),
    path('perfil/oferta/', guardar_oferta, name='guardar_oferta'),
    path('perfil/necesidad/', guardar_necesidad, name='guardar_necesidad'),
]