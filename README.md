# Streamlit Autenticación

En el proyecto se desarrolla un sistema de autenticación de usuarios, en donde las personas se pueden registrar e iniciar sesión según diferentes roles.

Existen tres tipos de roles:

- Administradores
- Editores
- Invitados

## Módulo de Inicio de Sesión

Para la creación del módulo se utiliza:

- El session_state de Streamlit, para manejar el flujo de los datos de los usuarios.

- PyJWT, la librería permite codificar y decodificar JSON Web Tokens (JWT). De manera que permite guardar la información de la sesión de un usuario, así cada vez que ingrese a la web, no es necesario la autenticación.

- bcrypt: librería pra encriptar los datos que ingrese el usuario.

- SQLite: se crea una conexión con la base de datos, esta solo almacena datos de los usuarios.

### Funcionalidades

- Registrar Usuario: cualquier persona que ingrese se puede crear un usuaruio nuevo y define el rol que quiere tener. 

- Iniciar Sesión: una vez se tiene un usuario se puede acceder a los proyectos, estos según sea el rol. 

- Cerrar Sesión: un botón que permite cerrar la sesión del usuario cuando guste.

- Cambiar contraseña: el usuario desea actualizar su contraseña.


## Módulo de Administrador

Para la creación del módulo se utiliza:

- Pyshorteners: librería que permite acortar los enlaces según diferentes servicios, en este caso se utilizó tinyurl.

- Matplotlib: librería que permite hacer gráficos y poder interactuar con ellos. Para este caso, se hace uso de un dataset de películas.

### Funcionalidades

- Acortador URL: proyecto donde se introduce un enlace y lo acorta. Realizado con Pyshorteners

- Películas: proyecto para buscar, filtrar, ver puntuciones y demás características. 
    - Se utiliza el dataset disponible en este enlace: https://tinyurl.com/2nej9f8a 
    - Los gráficos son construidos con Matplotlib



## Módulo de Editores
Para la creación del módulo se utiliza:

-Plotly: crear gráficos que permite la interacción con una web de Streamlit.

### Funcionalidades

- Visualizador: ver diferentes gráficos realizado en Plotly

- Acortador URL: se reutiliza la parte del módulo de Administrador, aquí pueden acceder tanto los administradores como los editores

## Módulo de Invitados

En esta parte solo aparece un mensaje de "sitio en construcción"





## Archivos

1. **app.py**: Este es el archivo principal del proyecto. Contiene la lógica principal y es el punto de entrada para la ejecución del programa.

2. **authenticate.py**: contiene toda la lógica relacionada con el inicio de sesión y registro de usuarios. 

3. **inicio_admin.py**: interfaz que conecta a los usuarios administradores con los proyectos que tiene acceso

4. **inicio_editor.py**:interfaz que conecta a los usuarios editores con los proyectos que tiene acceso

5. **database.db**: archivo de la base de datos SQLite que guarda los datos. 

**Apps**: es una carpeta que contiene los proyectos a los que acceden los usuarios, estos son:

- **acortador_url.py**: lógica del proyecto para acortar enlaces.

- **peliculas.py**: lógica del proyecto para buscar y filtrar películas.

- **visualizador.py**: ver gráficos de la librería plotly.

## Instalar
```
pip install -r requirements.txt
```
Se recomienda usar un entorno virtual de python.

## Uso

1. Ejecutar: 
```
streamlit run app.py
```

2. Abrir el navegador en:
```
http://localhost:8501/
```


## Desplegar

1. Ingresar a Streamlit Community Cloud

2. Crear una cuenta

3. Sincronizar con la cuenta de GitHub

4. Seleccionar el proyecto a desplegar

