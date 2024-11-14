# Proyecto Lambda

`El epicentro de tu tecnología`

`Fácil de instalar y fácil de mantener`

`Altamente personalizable`

`Simple, rápido y eficinete`

explorar la posibilidad de multiples bots dentro de la misma api

DADO EL NUEVO MODELO DE NEGOCIOS, EL PATCH DE LA USERLIST SE VA A DESCTIVAR

crear diversos alias de Lambda, como sigma, beta … que sirvan para diferentes cosas como IoT, Trading y minería de datos, y más y quizá `que estos bots tengan diferentes cerebros` que funcionen de manera diferente a Lambda

Crear una manera de poder leer mi mail mediante lambda

[Desarrollo de Software](https://www.notion.so/Desarrollo-de-Software-b0480ffdfca142cdaff3fefe705573df?pvs=21)

[Documentaciones](https://www.notion.so/Documentaciones-620e0b2fb78e4e0c8895aeec83176d1f?pvs=21)

[Ecosistema IoT](https://www.notion.so/Ecosistema-IoT-7dd1dfd0e24446359a9f30534e020cdc?pvs=21)

[Empresa](https://www.notion.so/Empresa-19c5cdcd006c4c3ab8598b1385ca3bb2?pvs=21)

[Museo](https://www.notion.so/Museo-fc47c6b2a57349848c55ef0ef12e9182?pvs=21)

[Server NGINX](https://www.notion.so/Server-NGINX-102aed79155180398ce3e6062fd8e708?pvs=21)

Nuevas DBs

- para iot: devices y mensajes entrantes
- una de autenticación
- Para archivos de usuarios

# Agenda

- [ ]  Crear una DB de api keys
    
    id de usuario
    
    api key
    
    `las ids serán generadas en el web server`
    
- [ ]  Terminar Lambda para chat general, las skills después
- [ ]  Meter Lambda en un Server de NGINX que acepte solo requests con API KEY
- [ ]  Crear la autenticación por SMS en el server web y la generación de Tokens
    - [ ]  Al crear un nuevo usuario
        - [ ]  se manda una confirmación a Lambda bajo una API KEY del web server
        - [ ]  Se genera la API-KEY para el usuario
        - [ ]  Y se recibe y guarda como datos de la sesión del usuario
        - [ ]  Entonces el usuario ya puede chatear
- [ ]  Demo de la página web con chat

# Curiosidades de experimentación

Mientras que las imágenes con gpt4o-mini costaban 8000 tokens mas o menos, con claude 35 sonnet, eran de ~150 tokens

estimamos que una prompt imagen de primeras, cuesta como .0016 USD

- [ ]  Modos de lambda
    - [ ]  Diseño grafico
    - [ ]  Asistente
    - [ ]  Compañero
    - [ ]  Desarrollador
    - [ ]  Tutorial: seleccionar un tutorial de medium con un link o un motor de búsqueda de lambda y hacer preguntas sobre el tutorial

# Objetivos Lambda `v4`

- [ ]  Comenzar la documentación
    - [ ]  DB
    - [ ]  Interfaces
    - [ ]  Bin
    - [ ]  Lambda
    - [ ]  Lambdrive
    - [ ]  Daily
    - [ ]  Apps
    - [ ]  Backups
- [ ]  Que haya un archivo de configuración que permita modificar el funcionamiento de lambda, entre estos
    - Modificación y actualización de modelos de lenguaje
    - Días de recarga de usuarios, actualmente en 30
    - puertos y hosts de ejecución
- [ ]  Integrar y usar de mejor manera los modelos de instruct y embeddings de openAI
- [ ]  Dar paso a la creación de los modos de Lambda
- [ ]  Dar paso a la integración de nuevas IA, desde el modo de recibir llamadas a Lambda
- [ ]  Dar paso a la creación del grafo de memoria de los usuarios e incorporar algún mecanismo de gustos y recuerdos de Lambda.

# Hacia donde crecer

- [ ]  Lambda cambia a modo diseño, para pedir imágenes como en chatgpt plus
- [ ]  Investigar que hace el comando patch y como utilizarlo para lambda
- [ ]  utilizar algún medio de almacenaje de info en el que ciertas funciones guarden `expedientes de los usuarios` con fines: `terapéuticos, nutriólogos, o de aprendizaje` o avance de proyectos. Podemos integrar aquí la visión de Gemini
- [ ]  investigar todo lo que se puede hacer con `ffmpeg` e incorporar todas esas herramientas
- [ ]  Optimizar con prompt engineering las lambda skills
- [ ]  [https://platform.openai.com/docs/overview](https://platform.openai.com/docs/overview) para más ideas con lambda
- [ ]  `Relacionar lambda con los ODS para ventas` y la página web
- [ ]  Una función que muestre la personalidad de lambda
- [ ]  `crear una función de Lambda para almacenar información manualmente, para luego preguntarle respoecto a ese texto manualmente armado`
- [ ]  L, Lambda, para preguntas, Lambda , L , para comandos
- [ ]  Agregar apuntes a leer
- [ ]  investigar como usar SSH con túneles para las comunicaciones de IoT
- [ ]  Agregar una función para leer words
- [ ]  Agregar funciones con excels y csv
- [ ]  Investigar librerías: `moviepy`
- [ ]  Integrar bard a Lambda [https://github.com/dsdanielpark/Bard-API](https://github.com/dsdanielpark/Bard-API)
- [ ]  Función de traducir PDFs

# Hacia donde crecer - Más allá de Lambda

- [ ]  Crear una solución de IA que relacione el historial de compras de farmacias con los pacientes o doctores
- [ ]  Dispositivos IoT para la casa
    - [ ]  Alacena inteligente, que tenga sensores de presión y diga más o menos cuanto de cada producto hay, por ejemplo, tortillas, pastas, arroz, cereal
    - [ ]  Apagadores inteligentes
    - [ ]  Switches para multiples dispositivos
- [ ]  Funciones de páginas web
    - [ ]  Desplegar páginas web solamente subiendo el archivo html y más
- [ ]  Agregar modulos para ciencia de datos
- [ ]  Agregar un módulo de oprimización matemática con GLPK
- [ ]  En el futuro lambda podría servir como un directorio inteligente de empresas y negocios, lambda recomiéndame un lugar para comer Mariscos, lambda dime donde puedo conseguir algo
- [ ]  Desarrollar soluciones de IA para empresas con páginas web. Un chat integrante a las páginas que tenga ia integrada y que responda en base al contenido de la página del negocio. Otro que sea un chat integrado de lambda en web, para páginas web

# Ideas de Funciones:

- [ ]  Una función de logos
- [ ]  Una función de un pool de imágenes para presentaciones, dado un tema y keywords
- [ ]  Un editor de imágenes que vaya generando imágenes recursivamente, de que, haz una imagen, agregale esto, luego esto y así `modo grafico`
- [ ]  Dado un PDF, pedir extraer las n páginas más importantes de un tema y meterlas en un PDF nuevo. Leer las páginas de manera iterativa.
    - extrae lo importante de … sobre …
    - obtén lo importante de … sobre …
    - corta lo importante de … sobre …
- [ ]  Hacer alguna incorporación de wikipedia [https://pypi.org/project/wikipedia/](https://pypi.org/project/wikipedia/)
- [ ]  Una Función de Admin para Recargar usuarios
- [ ]  Calculadora completa de lambda
- [ ]  Ejecutor de cálculos con sintaxis de python
- [ ]  Resumir páginas web

[OpenAI Platform](https://platform.openai.com/examples)

# Lambda para IoT

[Getting Started with Nano ESP32 | Arduino Documentation](https://docs.arduino.cc/tutorials/nano-esp32/getting-started-nano-esp32#compile--upload-sketches)

[Nano ESP32 | Arduino Documentation](https://docs.arduino.cc/hardware/nano-esp32)

## Links importantes raspberry pico y arduino nano esp32

[How to run a webserver on Raspberry Pi Pico W - Raspberry Pi](https://www.raspberrypi.com/news/how-to-run-a-webserver-on-raspberry-pi-pico-w/)

[ESP32 Web Server - Arduino IDE | Random Nerd Tutorials](https://randomnerdtutorials.com/esp32-web-server-arduino-ide/)

# Los Binarios `bin`

## `lambda [commadn]`

Es un script de bash que resume todos los scripts anteriores de lambda (run, kill, update, reboot) siendo ahora únicamente un archivo

## `lservice [servicio] [opciones]`

Es un script de bash que permite ejecutar los servicios de lambda.

## Los servicios

Los servicios tienen su propio folder que es independiente, pero como tal, en `bin/services` habrán ligas a los ejecutables de dichos servicios. De manera que si se desea ejecutar alguno simplemente sea ingresar algo así: `services/bchat-server`

## El instalador `install`

La idea es que si lambda se muda a un servidor nuevo o simplemente se hacen cambios, como nuevas carpetas o demás. Que lambda tenga un script de bash que permita crear esas carpetas y archivos de configuración. Esto podría facilitarse si a esta nueva instancia de lambda se le proporciona un archivo de backup que le permita restaurar un “checkpoint”.

**se ejecutará después de tener el repo de lambda ya en el servidor**

`git clone https://github.com/OmarSaldanna/Lambda.git`

1. verificar que lambda este en `$HOME/Lambda`
2. instalar librerías de `requirements.txt`
3. crear el folder de los `backups`
4. crear el folder de la `ram`
5. crear las ligas de los binarios de los servicios `bin/services`
    1. de esta manera ejecutar un servicio será `services/bchat-server`
6. agregar los binarios de lambda a la variable `$PATH`
7. formar las ligas de los servicios a los binarios
8. agregar la rutina de respaldos a cron
    1. `14 15 * * 0 lambda rupdate && lambda backup`
9. restaurar la memoria con un `backup`
10. los permisos de los **binarios** y de los **servicios**
11. ejecutar lambda `lambda run`

```bash
#!/bin/bash

# 1: the command must be ran in $HOME/Lambda
if [ "$(pwd)" != "$HOME/Lambda" ]; then
	echo -> You have to be in $HOME/Lambda
	exit
fi

# 2: install requierements.txt

```

# Servicios `services/service`

Los servicios de lambda son programas subyacentes a lambda que sirven para diversas cosas. Quizá los servicios en algún futuro no tengan que ser usados mediante un comando específico. Idea: diccionario de funciones y lwr.

Idea: usar ligas para tener los ejecutables de los servicios en la carpeta de binarios. Hacer que los archivos de ejecución de los servicios, tengan un modo de apagado

Que pueda guardar contraseñas, y por ende que tenga alguna especie de servicio de cifrado para todos

## Funcionamiento

- Los servicios tendrán sus folders dentro de la carpeta `services/` y dentro de ellos tendrán el contenido necesario para ejecutar el servicio.
- La ejecución de los servicios se hará mediante un **script de bash** que llevará el mismo nombre que el directorio del servicio. Dicho script tendrá un `hard link` localizado en folder de `bin/services` de manera que para ejecutarlo solo tendrá que usarse `services/service`
- Los servicios serán ejecutados mediante `tmux` de manera que cada servicio tendrá una sesión diferente a las de lambda, corriendo de manera independiente.

## Servicios

# Errores y Soluciones:

- Errores al instalar paquetes con pip3 en **Debian 11. Solucionado eliminando el archivo**

[How do I solve "error: externally-managed-environment" everytime I use pip3?](https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-everytime-i-use-pip3)

[Estándares](https://www.notion.so/Est-ndares-d87d4fc0ff774e518e508ddeeb9fea5e?pvs=21)