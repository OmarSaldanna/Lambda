# Lambda Discord Bot

## -> English

### Description
This is my own discord bot created with *Python*. There's no an specific objective for the development of this bot. The thing that I want is use these bot for experimental purposes such as internet of things, machine learning model testing, follow anime chapters, advise of new manga books through web scrapping and more things that I will come up with.

Actually this bot doesn't have an "formal" database, the thing it uses to save data is a txt file that follows certain rules to save and split data, rules that are defined in the database file _(modules/database.py)_. The database also allows to save lists and read them.

## -> Español

### Descripción
Este es mi propio bot de discord creado con *Python*. No hay un objetivo específico para el desarrollo de este bot. Lo que quiero con este bot es usarlo para diversos experimentos como implementaciones con Internet de las cosas, experimentar con modelos de inteligencia artificial, seguir animes en emisión y nuevos tomos de manga mediante minería de datos de páginas web, entre otras cosas que eventualmente se me irán ocurriendo.

Actualmente el bot no cuenta con una base de datos "formal", lo que el bot usa para guardar información en un archivo txt que sigue ciertas reglas para guardar y separar datos, dichas reglas están definidas en el archivo que maneja la base de datos _(modules/database.py)_. La base de datos además cuentas con funcionalidades para guardar listas y leerlas.

## Command List / Lista de Comandos
_Note:_ currently most of the commands are in spanish.

### save stuff(text) / guardar cosas(texto)

*-sostenme* [texto]
  
*-dame*
  [texto]


### anime follow / seguimiento de anime

*-sigueanime [link] como [nombre]*

*-animes*
  Estamos siguiendo estos animes:
  - [nombre] - [link]
  ...

*-capitulos [anime name]*
  - *cap [n]* [anime charper link]
  ...


### sound play / poner sonido

*-pon [link]*

*-pausa*
    
*-play*
    
*-stop*


### white list / sala cerrada
_voice channel admits only selected members_

*-salasegua para [@member1] [@member2] ...*

*-agregarasala [@member1] [@member2] ...*

*-eliminardesala [@member1] [@member2] ...*

*-salalibre*


### admin functions (only for me) / funciones de admin (solo para mi)
_these ones are for check db values or alter them_

*-save [key] [value]*

*-give [key]*

*-delete [key]*

*die*

### Lambda Commands / Comandos Lambda
These are "special" commands, pretend to make lambda smart as this commands have a more complex structure than the others, are multi-purpose and the all the commands has the same start: _-Lambda ..._. Here are some examples of the uses(these are in spanish):

_For Grocery_

* -Lambda falta comprar shampoo
* -Lambda no hay pasta de dientes
* -Lambda necesitamos spaguetti
* -Lambda tenemos que comprar lapiceros
* -Lambda ya no hay agua


_For IoT (working on it)_

* -Lambda abre las cortinas
* -Lambda enciende la lampara
* -Lambda apaga la lampara
* -Lambda apaga la luz
* -Lambda apaga el ventilador


_For Reminders_

* -Lambda recuerdame hacer mi tarea de _ a las 12pm
* -Lambda avisale a @alguien que mande su tarea a las 11pm
* -Lambda recuerdale a @everione que al rato hay minecraft [al rato como a las 9]
* -Lambda recuerdame que tengo una reunion en zoom a las 2:30

_Send whatsapp messages (may be on the future)_


_structure_

*-Lambda [verb] [obj]*, first recognize if the command is for Grocery, IoT, or ..., later recognize the action to do and then what to do depeinding on the object.


### daily subroutines / subrutinas diarias (working on it)
_daily executed by the bot_

*-actualizar_animes*
    
  Estos son los capitulos nuevos:
    
  - [animeflv] - *cap [n]* - [link animeflv capitulo]
  ...