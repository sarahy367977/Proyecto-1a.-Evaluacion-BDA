# Sistema de Gestión de Blog

El proyecto es una aplicación web que permite gestionar un blog completo con funcionalidades de creación, edición, eliminación y visualización de artículos, usuarios, comentarios, tags y categorías.

## Guía de inicio

Las siguinetes instrucciones ayudarán en la ejecución del proyecto en tú máquina local.

### Requisitos

Tener instalado lo siguiente:

- Python 3.8 o superior
- Oracle Database
- Oracle SQL Developer (opcional)

### Instalacion

Para ejecutar el proyecto, sigue los siguientes pasos:

1. **Clonar el repositorio**
```
git clone https://github.com/sarahy367977/Proyecto-1a.-Evaluacion-BDA.git
cd Proyecto-1a.-Evaluacion-BDA
```

2. **Configurar Base de Dtos Oracle **

```
Crear usuario
CREATE USER blog1 IDENTIFIED BY blog1;
GRANT CONNECT, RESOURCE TO blog1;
GRANT UNLIMITED TABLESPACE TO blog1;

grant resource, DBA to blog1;
```

3. **Ejecuta los script en orden correspondiente**

```
BLOG1 - Creación de tablas, funciones y procedimeintos
BLOG~2 - Datos de prueba

```
4. **Configuarar conexión en app.py**

```
dsn = oracledb.makedsn("localhost", 1521, service_name="xepdb1")
conn = oracledb.connect(user="BLOG1", password="blog1", dsn=dsn)

```
5. **Instalar dependencias**

```
pip install flask oracledb flask-cors

```
6. **Ejecutar la aplicación backend**
```
python app.py

Servidor backend en: http://localhost:5000
```
7. **Ejecutar la frontend**
```
cd blog-fronten(direccion donde se guardo el archivo HTML)
python -m http.server 8000

Interfaz web en: http://localhost:8000
```

## Construido con

* [Python ](https://www.python.org/) - Lenguaje de programación utilizado para desarrollar el backend y la API RESTful
* [Flask ](https://flask.palletsprojects.com/en/stable/) - Framework web utilizado para crear la aplicación backend y los endpoints API.
* [PL/SQL ](https://www.oracle.com/database/technologies/appdev/plsql.html) - Lenguaje de programación utilizado para implementar la lógica de negocio en procedimientos almacenados.
* [oracledb](https://python-oracledb.readthedocs.io/en/latest/) - Driver Python utilizado para la conexión entre la aplicación Flask y la base de datos Oracle.
* [HTML5](https://developer.mozilla.org/es/docs/Web/HTML) - Lenguaje de marcado utilizado para la estructura de la interfaz web.
* [CSS3](https://developer.mozilla.org/es/docs/Web/CSS) - Lenguaje de estilos utilizado para el diseño y presentación visual del frontend.
* [JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript) - Lenguaje de programación utilizado para la interactividad y consumo de API en el frontend.
* [Oracle SQL](https://www.oracle.com/database/sqldeveloper/) Developer - Herramienta utilizada para la gestión y administración de la base de datos Oracle.\
* [Flask-CORS]() - Extensión de Flask utilizada para habilitar el intercambio de recursos de origen cruzado (CORS).
* [Python http.server](https://docs.python.org/3/library/http.server.html) - Módulo utilizado para ejecutar el servidor web local del frontend.

  
## Autores
* **Sarahy Chaparro Ramírez - * 367977* - [sarahy367977](https://github.com/sarahy367977)
* **Jazmin  Cruz González** - *367770* - [JazCrz194](https://github.com/JazminCrz194)
