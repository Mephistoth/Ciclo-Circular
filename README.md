# Ciclo Circular - Sistema de Gestión Industrial Full-Stack 🔄
### 💼 Proyecto Desarrollado en Práctica Profesional

### 📝 Descripción
Plataforma web Full-Stack desarrollada con el framework robusto **Django (Python)** para la automatización, simulación y optimización de ciclos de producción industriales. Este software fue diseñado e implementado como proyecto de finalización de **Práctica Profesional**, resolviendo requerimientos reales de modularidad, manejo de API REST y automatización de procesos internos. El sistema cuenta con una arquitectura modular avanzada que incluye un panel de administración, gestión de usuarios, módulos de automatización (`bot`) y una API REST integrada para futuras conexiones móviles o externas.

---

### 🚀 Stack Tecnológico
* ⚙️ **Backend:** Python 3.x (Django Framework)
* 🎨 **Frontend:** JavaScript, HTML5, CSS3, SCSS, Bootstrap
* 🤖 **Automatización:** Módulo de tareas automatizadas (`bot`)
* 🌐 **Integración:** API REST nativa incorporada

---

### ⚙️ Arquitectura del Sistema
El proyecto sigue el patrón MVT (Model-View-Template) de Django, dividiendo las responsabilidades lógicas en módulos limpios y escalables:
* `administrador`: Panel de control técnico y métricas del sistema.
* `user`: Módulo de autenticación segura, manejo de sesiones y perfiles.
* `api`: Capa de servicios para la exposición y consumo de datos.
* `bot`: Scripts lógicos orientados a la automatización de procesos.

---

### 🛠️ Guía de Instalación y Ejecución Local

Sigue estos pasos para desplegar el entorno de desarrollo en tu máquina:

**1. Clonar el repositorio e ingresar al directorio:**
```bash
git clone https://github.com
cd Ciclo-Circular
```

**2. Crear el entorno virtual de Python:**
```bash
python -m venv venv
```

**3. Activar el entorno virtual:**
* *En Windows (CMD):*
  ```bash
  .\venv\Scripts\activate.bat
  ```
* *En Linux/Mac o Git Bash:*
  ```bash
  source venv/bin/activate
  ```

**4. Instalar las dependencias y librerías del proyecto:**
```bash
pip install -r requirements.txt
```

**5. Ejecutar las migraciones de la Base de Datos:**
```bash
python manage.py migrate
```

**6. Levantar el servidor de desarrollo:**
```bash
python manage.py runserver
```
*Abra [http://127.0.0.1:8000](http://127.0.0.1:8000) en su navegador para ver la aplicación ejecutándose.*

---

### 📬 Contacto
* 💼 **LinkedIn:** [Felipe Soto](https://linkedin.com)
* 📧 **Email:** felipeignacio28soto@gmail.com
