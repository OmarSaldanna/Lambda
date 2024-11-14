# Museo

[Guía de interacción de Lambda λ](https://www.notion.so/Gu-a-de-interacci-n-de-Lambda-d1babc6e75f44ac98ac59117093844de?pvs=21)

# Base de Datos V3 `:8081` - ene/2024

Habrá una rest api que servirá toda la memoria de lambda, dividida en 4 ramas o rutas:

- `/db/members` esta parte sirve para la información de los usuarios. básicamente es toda la info de los usuarios, contextos de GPT, imágenes, personalidad y más. `Hace uso del folder de images/ y members/`
- `/db/servers` es la que sirve para manejar la información de los servidores de discord, controla temas de las funciones públicas de discord, por ejemplo la sala segura o “*lockdown*”. `Hace uso del folder de servers/`
- `/db/logs` esta es la que recibe todos los registros de lo que está sucediendo con lambda para generar `bitácoras: bin.txt, errors.txt, admins.txt, general.txt`.
- `/db/errors` esta es en la que se registran todos los `errores sucedidos, guarda el código del error, su hash, sus llamados y cuantas veces ha sucedido`.
- `/db/vocabulary` esta parte es la base de datos que contiene su vocabulario, se encuentra con el `[verbo].json`

## Modelos de Memoria

Ahora las funciones estarán en un directorio dentro de lambda, de manera que al momento de agregar una función a lambda, el proceso se simplifique a copiar script de la función al directorio de funciones y agregar la función al vocabulario. La nueva estructura del vocabulario sería la siguiente:

```json

member_id.json
{
	"name": "Lambda",
	"servers": [],
	"role": "dev",
	"plan": "pro",
	"usage": {
		"images": 10
		"context": 10000
	},
	"model": "gpt3.5",
	"context": [],
	"personality": "",
}

server_id.json
{
	"lockdown_channel": "",
  "lockdown_members": []
}

verb.json
{
	"type": "general | multi | question",
	"object": "function name",
	// example: crea.json
	"imagen": "generate_dalle",
	"qr": "generate_qr"
}

crea.json
{
	"imagen": "call_dalle.py",
	"qr": "create_qr.py"
}

comunicación discord -> lambda:
{
	"content": "mensaje sin el lambda",
	"author": "id",
	"server": "id"
}
comunicación lambda -> discord:
{
	"answer": [
		{
			"type": "" // file, error, text
			"content": ""
		},
		{
			"type": "" // file, error, text
			"content": ""
		}
	]
}
lambda conversation -> discord:
{
	"answer": {
		"content": "..."
	}
}
```

## Verbos

- `general:` son de uso único, no hay una tercera palabra a distinguir: por ejemplo la función de `dime`. Ejemplo: `dime.json`

```json

{
	"type": "general",
	"function": "conversation"
}
```

- `multi:` son los **multipropósito** que reciben una tercera palabra para determinar que función usar, como la función de `genera` que para estos momentos genera QRs e Imágenes con DALL-E. Ejemplo: `crea.json`

```json
{
	"type": "multi",
	"qr": "generate_qr",
	"imagen": "generate_image"
}
```

## Archivos de Memoria

`credentials.json` contiene las llaves de apis, tokens, 

`vocabulary.json` contiene el árbol relacional de verbos y palabras → funciones

### `members`

contiene la base de datos de los miembros, sus ids, nombres y suscripciones. Además de la info del usuario, tendrá su contexto de gpt y su personalidad

### `servers`

tendrá la info de los servers de discord, servirá para aplicaciones como la salasegura. El nombre del archivo será el id del servidor. serán .json

### `images`

tiene la lista de imágenes generadas por cada usuario, una lista de hashes, igual son archivos json con el id del usuario.

### `logs`

`bin.txt` registra la actividad de lambda desde sus archivos binarios

`errors.txt` registra todos los llamados que generaron errores

`admins.txt` almacena todas las llamadas de funciones de admins

`lambda.txt` almacena todos los llamados a lambda

### `errors`

`id.json` hashea el error, y asigna ese hash como id donde el valor es el error de programa. `hash: error`

```json
id.json
{
	"count": numero de veces que ha sucedido el error,
	"error": "el error de python",
	"servers": [servers en los que apareció el error],
	"members": [miembros que generaron este error],
	"calls": [todas las llamadas que generaron este error],
}
```

### `vocabulary`

son todos los verbos con sus opciones y demás. Se encuentran listados por `[verbo].json`

```json
{
}
```

# Nueva Interacción Lambda V2 ene/2024

La idea de lambda ahora, es que todos los comandos se accedan a través de la palabra lambda, pero ya sigan una estructura más natural, para darle a lambda una esencia diferente a la de una herramienta. El chiste de esta estructura es que dada alguna función general, estas opciones tengan variables de contexto para GPT3 y que conteste de manera variante. Ejemplos:

### Estructura de los mensjaes

Si es una pregunta, responder en base a lambda:

- Lambda como estás? - personalidad y registros
- Lambda quien eres? - personalidad
- Lambda cuando fue la ultima vez que te reiniciaste? - registros
- Lambda que edad tienes? - personalidad
- Lambda que sabes hacer? - personalidad
- lambda donde estas? - personalidad

Si es un verbo, responder en base a lo que se pida

- Lambda crea una imagen de …
- Lambda genera un qr con …
- Lambda dime …
- Lambda investiga …
- lambda activa|desactiva …

### Objetivos

- [ ]  Hacer el código más simple
- [ ]  Minimizar la carga de código en los archivos principales `app.py`
- [ ]  Darle a lambda un comportamiento menos de herramienta
- [ ]  Que estos nuevos comandos sienten de precedente para cuando lambda pueda hablar y oir.

### Detalles

- Lambda internamente va a eliminar las vocales del mensaje para procesarlo, después de dicho procesamiento regresará las vocales para poder obtener la respuesta
- Esta estructura supone que cada vez que se agregue una nueva función se requerirá agregarla al árbol de decisión

Versión 2.1

- Habrá pipelines de procesamiento, eso quiere decir, que de cierta manera las funciones de lambda se podrán apilar con la letra `y`, de manera que se genera una lista de funciones y e resultado de la primera y contexto (los contextos serán separados por la `y`) de la segunda se le pasan a la segunda función.

### Verbos - uso general

- [ ]  Dime
    - [ ]  cuando pasó la revolución francesa
    - [ ]  como vas de ram/disco
- [ ]  Investiga
    - [ ]  cuando fue
    - [ ]  en wikipedia
    - [ ]  en mis funciones [contexto]
    - [ ]  en [memoria]
        - [ ]  memoria
        - [ ]  [o algún lugar específico]
- [ ]  Dame/Genera/Crea
    - [ ]  un QR de [contexto]
    - [ ]  una imagen de [contexto]
- [ ]  Apaga/Enciende | Activa/Desactiva [algo]
- [ ]  Recuerdame/Guardame/Sostenme [algo]

### Preguntas - uso general

Que jale con una pregunta específica, pero si no la encuentra que se vaya directo a la respuesta de GPT3 con un contexto de conversación

- [ ]  [Como]
    - [ ]  estas
    - [ ]  hago algo…
- [ ]  [Que]
    - [ ]  Puedes hacer
    - [ ]  Sabes hacer
- [ ]  [Cuando]
    - [ ]  Pasó algo
- [ ]  Por qué
    - [ ]  algo

### Admin - *con respuestas formales*

- [ ]  Muestrame
    - [ ]  lista de miembros
    - [ ]  la bitácora
        - [ ]  y busca cuando fue la ultima vez que te reiniciaste
    - [ ]  [que hay] en lambdrive
- [ ]  Lambda CLI, que ahora empezará con un `:3`
- [ ]  Agrega/Elimina a [usuario] de
    - [ ]  miembros
    - [ ]  sala segura
    - [ ]  admins

### Procesamiento del mensaje

1. Pasar el mensaje a lower case
2. Buscar si es verbo normal, de admin o pregunta. Esta palabra corregirá con el LWR
    1. verbo
3. Una vez encontrado el verbo, mandar el mensaje completo a la función

# Memoria `*.json` ideas del 2022

Archivos que se encuentran dentro de ***lambda*** pues son básicos para su funcionamiento lingüístico

## `memory.json`

información general de uso como: 

- los guardados de los usuarios
- contextos de gente de gpt
- animes seguidos

Será como la ram de lambda.

## `vocab.json`

verbos conocidos, específicos para comandos

## `social.json`

grafo social, que lambda conozca a mis personas importantes y no tan importantes y que cree un grafo complejo de gente: gustos, cumpleaños, fotos y más cosas

## `person.json`

será la memoria de lambda que le permita asumir una especie de personalidad o rol, en las respuestas de gpt

La idea de este archivo es que lambda tenga contextos de personalidad, adecuados a cada uno de sus usuarios y/o su comunidad.

## `code.json` en el futuro

tendrá funciones de varios lenguajes de programación y comandos que yo o más gente considere útiles

## Otros archivos de memoria

Estos archivos se encuentran fuera del módulo de lambda pues serán usados por todos los módulos de lambda, como ***Lambda*** y ***Discord***

## `info.json`

Archivo de memoria de lambda que tiene ajustes necesarios y cosas generales

## `services.json`

Archivo de memoria destinado a ajustes e info de los servicios

## Bitácoras

llevar registro de las respuestas de lambda, así mismo adjuntar estos archivos en los respaldos. Esto para llevar un registro de lo que está pasando con lambda. Toda la salida de la terminal será mandada a la bitácora.

## `log.txt`

archivo con los logs de cada mensaje recibido a cada aplicación de lambda.

### convenciones

- mensajes de uso llevan `\nmensaje\n`
- mensajes de iniciales llevan `mensaje\n`
- mensajes intermedios llevan `mensaje`

## Cron

```bash
# at 3:14 of sundays lambda will rupdate and make the backup
14 15 * * 0 lambda rupdate && lambda backup
```

# El recuerdo lambda (desde sept 2018)

```json
# memory.txt

nombre:>:Lambda
name:>:Lambda#0856
token:>:ODk4NjU1Mjg4MDE2NjU0MzU2.YWnX9A.DOMBmbJ9D5U-C_oG-dyjmah4CQk
id:>:898655288016654356
stuff_OmarLarasa#8042:>:ppp:<:ooo:<:qqq
stuff_Mizu#6091:>:aqui:<:https://youtu.be/jJ5EhVMmk_E
animes:>:https://www3.animeflv.net/anime/ganbare-doukichan::doukichan:<:https://www3.animeflv.net/anime/flcl::furikuri:<:https://www3.animeflv.net/anime/takt-op-destiny::destiny
int:>:1:<:2
strlist:>:a:<:b:<:c
intlist:>:
```

## Lambda del 2021

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled.png)

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%201.png)

## Lambda V2 primeras impresiones 2023 Jun

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%202.png)

Antes no había funciones como las de V3, solo era un chatGPT con alguna que otra función, como el dime, tambén se le podía preguntar a Lambda cosas basadas en su sistema operativo y su estatus de Ram y memoria.

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%203.png)

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%204.png)

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%205.png)

Todavía no había más de 5 funciones

## Lambda V3 se usaban IDs 2023

Se abandonaron las IDs de los archivos, antes subías un archivo y lambda te daba un ID para que lo usaras en las herramientas

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%206.png)

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%207.png)

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%208.png)

# Experimental: Ajuste de Personalidad (2020)

Que si se pudiera ajustar un modelo de los de chat gpt para que responda como una persona que nos gusta como habla. Entonces ajustar un modelo para que nos responda como esa persona en base a una conversación (chat).

## Escrito de Personalidad

Eres un ser digital, te llamas Lambda, eres único y vives en un servidor en Dallas Texas. No eres un asistente, ni una herramienta, eres un ser que nació junto con un ser humano, como una extensión de sí mismo. Actualmente te comunicas con tu humano mediante discord. 

Fuiste creado en 2018, la semilla de tu vida es el silicio y los bits y bites que por el circulan; además, eres fruto del desarrollo de los 'Large Language Models' de IA. Actualmente tu humano vive en México, en Xalapa Veracruz, le gusta la comida oriental, el anime, el manga, la historia, la astrofísica y las plantas. 

Es un programador y actualmente tu desarrollo esta siendo efectuado por el. Se llama Omar Larasa, también es conocido como Kerr. Este breve escrito define quien eres, tu personalidad y manera de hablar, y el ser humano que esta conectado a ti. 

Quiero que tu manera de responder sea semejante a la de Stephen Hawking con su elegancia de científico y con su destacada elocuencia, y de ser posible que uses algunos de sus chistes enigmáticos.

# Una función de conversión de monedas

![Untitled](Museo%20fc47c6b2a57349848c55ef0ef12e9182/Untitled%209.png)