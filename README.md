Sistema de Ventas - Django
📋 Descripción
Sistema web completo de gestión de ventas desarrollado en Django con Tailwind CSS para la evaluación de Programación BackEnd (TI2041).

🚀 Características
✅ CRUD completo de Clientes, Productos y Ventas
✅ Informes con gráficos de productos más vendidos y clientes destacados
✅ Interfaz moderna con Tailwind CSS
✅ Base de datos SQLite integrada
✅ Diseño responsive para todos los dispositivos
✅ Sistema de ventas con múltiples productos por venta
🛠 Tecnologías Utilizadas
Backend: Django 5.2.7
Frontend: Tailwind CSS (CDN)
Base de datos: SQLite
Lenguaje: Python 3.11+
Templates: Django Templates + HTML5 + JavaScript
📦 Requisitos del Sistema
Python 3.8 o superior
pip (gestor de paquetes de Python)
Navegador web moderno
⚡ Instalación Rápida
1. Clonar o descargar el proyecto
# Si tienes el código fuente, navega a la carpeta
cd backend
2. Crear y activar entorno virtual
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
3. Instalar dependencias
pip install -r requirements.txt
4. Configurar la base de datos
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
5. Crear usuario administrador (opcional)
python manage.py createsuperuser
6. Ejecutar el servidor
python manage.py runserver
7. Acceder a la aplicación
Abre tu navegador y ve a:

http://127.0.0.1:8000/
📁 Estructura del Proyecto
backend/
├── config/                 # Configuración de Django
│   ├── settings.py        # Configuración principal
│   ├── urls.py           # URLs del proyecto
│   └── wsgi.py           # Configuración WSGI
├── ventas/                # Aplicación principal
│   ├── models.py         # Modelos de base de datos
│   ├── views.py          # Lógica de vistas
│   ├── urls.py           # URLs de la app
│   ├── admin.py          # Configuración admin
│   └── templates/        # Templates específicos
├── theme/                 # Theme y estilos
│   └── templates/        # Templates base
├── db.sqlite3            # Base de datos
├── manage.py             # Script de gestión
└── requirements.txt      # Dependencias
🎯 Funcionalidades Implementadas
👥 Gestión de Clientes
Listar clientes - Vista tabular con información completa
Crear cliente - Formulario con validaciones
Editar cliente - Modificación de datos existentes
Eliminar cliente - Con confirmación
📦 Gestión de Productos
Listar productos - Con información de precio y stock
Crear producto - Formulario completo
Editar producto - Actualización de datos
Eliminar producto - Con confirmación
Control de stock - Seguimiento de inventario
💰 Gestión de Ventas
Listar ventas - Historial completo
Crear venta - Sistema con múltiples productos
Ver detalle - Información completa de venta
Eliminar venta - Con confirmación
Cálculo automático de totales y subtotales
📊 Informes y Estadísticas
Productos más vendidos - Ranking con gráfico
Clientes destacados - Por monto total gastado
Estadísticas generales - Resumen del sistema
Gráficos visuales - Representación de datos
🎨 Interfaz de Usuario
Diseño moderno con Tailwind CSS
Navegación intuitiva entre secciones
Responsive design para móviles y tablets
Mensajes de feedback para acciones del usuario
Formularios validados con mejor UX
🔧 Comandos Útiles
Desarrollo
# Ejecutar servidor de desarrollo
python manage.py runserver

# Crear migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Acceder al shell de Django
python manage.py shell
Administración
# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Verificar el proyecto
python manage.py check
📝 Características Técnicas
Base de Datos
SQLite para desarrollo
Modelos relacionales bien definidos
Claves foráneas y relaciones
Métodos personalizados en modelos
Seguridad
CSRF Protection habilitado
Validación de formularios
Protección contra inyecciones SQL
Performance
Consultas optimizadas con ORM de Django
Template caching implícito
Assets via CDN (Tailwind CSS)
🚀 Despliegue
Para producción se recomienda:
Configurar DEBUG = False
Usar base de datos PostgreSQL
Configurar servidor web (Nginx + Gunicorn)
Configurar dominio y SSL
Configurar variables de entorno
🤝 Contribución
Este proyecto fue desarrollado como parte de una evaluación académica. Para contribuir:

Fork el proyecto
Crea una rama para tu feature
Commit tus cambios
Push a la rama
Abre un Pull Request
📄 Licencia
Este proyecto es para fines educativos como parte de la evaluación de Programación BackEnd.

👨‍💻 Autor
Estudiante - Evaluación Sumativa N°2
Curso: Programación BackEnd (TI2041)
Institución: [Nombre de la institución]

📞 Soporte
Para soporte técnico o preguntas sobre el proyecto, contactar al docente del curso.

¡Listo para usar! 🎉
