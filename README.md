

# Sistema de Control de EPP

Este es un sistema desarrollado en Django para gestionar el retiro de Elementos de Protección Personal (EPP) en distintas faenas.

## 🔐 Funcionalidades principales

- **Login con roles**: Bodega Mantos Cobrizos, Tigresa, Revoltosa, y Prevención.
- **Validación de identidad**: Escaneo de QR para validar trabajadores.
- **Autorizaciones**: 
  - Registro de autorizaciones por parte de usuarios autorizados.
  - Visualización de nombre completo y cargo automáticamente.
- **Subida de documentos firmados**:
  - Verificación de que el archivo corresponda al ID de la autorización.
  - Renombrado automático del archivo al subirlo.

## 🧑‍💼 Roles de Usuario

- **Bodeguero**: Valida el retiro de EPP por faena.
- **Prevención**: Puede ver todas las autorizaciones por faena.

## 📁 Estructura del Proyecto

controlepp/
├── autorizaciones/
├── usuarios/
├── core/
├── static/
├── media/
└── templates/

bash
Copiar
Editar

## ⚙️ Instalación local

1. Clona el proyecto:
   ```bash
   git clone https://github.com/Sebasfelipe1/controlepp.git
Crea un entorno virtual e instálalo:

bash
Copiar
Editar
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
Ejecuta el servidor:

bash
Copiar
Editar
python manage.py runserver
🚀 Despliegue
Este sistema fue desarrollado y probado en entorno local con XAMPP y Django.