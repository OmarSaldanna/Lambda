# Lambda Discord Bot

## -> English

### Description
This is my own discord bot created with *Python*. There's no an specific objective for the development of this bot. The thing that I want is use these bot for experimental purposes such as internet of things, machine learning model testing, follow anime chapters, advise of new manga books through web scrapping and more things that I will come up with.

Actually this bot doesn't have an "formal" database, the thing it uses to save data is a txt file that follows certain rules to save and split data, rules that are defined in the database file _(modules/database.py)_. The database also allows to save lists and read them.

### About functionality

## -> Español

### Descripción
Este es mi propio bot de discord creado con *Python*. No hay un objetivo específico para el desarrollo de este bot. Lo que quiero con este bot es usarlo para diversos experimentos como implementaciones con Internet de las cosas, experimentar con modelos de inteligencia artificial, seguir animes en emisión y nuevos tomos de manga mediante minería de datos de páginas web, entre otras cosas que eventualmente se me irán ocurriendo.

Actualmente el bot no cuenta con una base de datos "formal", lo que el bot usa para guardar información en un archivo txt que sigue ciertas reglas para guardar y separar datos, dichas reglas están definidas en el archivo que maneja la base de datos _(modules/database.py)_. La base de datos además cuentas con funcionalidades para guardar listas y leerlas.

## Command List / Lista de Comandos
_Note:_ currently most of the commands are in spanish.

### save stuff(text) / guardar cosas(texto)
*-sostenme* <texto>
  
*-dame*
  <texto>

### anime follow / seguimiento de anime
*-sigueanime <link> como <nombre>*

*-animes*
  Estamos siguiendo estos animes:
  - <nombre> - <link>
  ...

*-capitulos [anime name]*
  - *cap<n>* <anime charper link>
  ...

### sound play / poner sonido
*-pon <link>*

*-pausa*
    
*-play*
    
*-stop*

### daily subroutines / subrutinas diarias
_ejecutada una vez al día por el bot_
*-actualizar*
    
  Estos son los capitulos nuevos:
    
  - [animeflv] - *cap [n]* - [link animeflv capitulo]
  ...
