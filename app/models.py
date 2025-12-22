from lib2to3.pgen2.token import OP
from pyexpat import model
from tkinter import CASCADE
from django.db import models

from user.models import Usuario


# Create your models here.

class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=20)
    calle = models.CharField(max_length=250)
    comuna = models.CharField(max_length=150) 
    lat = models.IntegerField()
    long = models.IntegerField()

    def __str__(self):
        return self.nombre


class AreaEmpresa(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=20)   
    productos = models.CharField(max_length=50)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    calle = models.CharField(max_length=250)
    comuna = models.CharField(max_length=150)
    lat = models.IntegerField()
    long = models.IntegerField()  

    def nombre_area(self):
        return "{}, {}". format(self.nombre, self.id_empresa)

    def __str__(self):
        return self.nombre_area()    


class Etapa(models.Model):
    id_etapa = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=50)
    fecha_inicio  = models.DateField() 
    fecha_termino  = models.DateField()
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre    


class RegistroTrabajador(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=160)                
    id_area = models.ForeignKey(AreaEmpresa, on_delete=models.CASCADE)

    def nombre_registro(self):
        return "{}, {}". format(self.usuario, self.id_area) 

    def __str__(self):
        return self.nombre_registro()  


        

class Entrada(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=50) 
    fecha =  models.DateField(auto_now_add=True)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    usuario =models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_area = models.ForeignKey(AreaEmpresa, on_delete=models.CASCADE)
    #cicloArea = models.ForeignKey(CicloArea, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Salida(models.Model):
    id_salida = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=50) 
    fecha =  models.DateField(auto_now_add=True)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    usuario =models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_area = models.ForeignKey(AreaEmpresa, on_delete=models.CASCADE)
   

    def __str__(self):
        return self.nombre

class Oportunidades(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=50) 
    fecha =  models.DateField(auto_now_add=True)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    usuario =models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_area = models.ForeignKey(AreaEmpresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Idea(models.Model):
    id_idea = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Idea de {self.usuario} en {self.empresa.nombre} (Etapa: {self.etapa.nombre})"


class CVUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    # Archivo almacenado en la BD como BLOB
    archivo = models.BinaryField()
    nombre_archivo = models.CharField(max_length=255)

    # 10 palabras clave generadas por ChatGPT
    palabra1 = models.CharField(max_length=200, null=True, blank=True)
    palabra2 = models.CharField(max_length=200, null=True, blank=True)
    palabra3 = models.CharField(max_length=200, null=True, blank=True)
    palabra4 = models.CharField(max_length=200, null=True, blank=True)
    palabra5 = models.CharField(max_length=200, null=True, blank=True)
    palabra6 = models.CharField(max_length=200, null=True, blank=True)
    palabra7 = models.CharField(max_length=200, null=True, blank=True)
    palabra8 = models.CharField(max_length=200, null=True, blank=True)
    palabra9 = models.CharField(max_length=200, null=True, blank=True)
    palabra10 = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CV de {self.usuario.username} ({self.timestamp})"


# class CicloArea(models.Model):
#     id_ciclo = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=40)
#     descripcion = models.CharField(max_length=40)
#     fecha = models.DateField()
#     area = models.ForeignKey(AreaEmpresa, on_delete=models.CASCADE)
#     activo = models.BooleanField()

#     def __str__(self):
#         return self.nombre



