﻿[![codecov](https://codecov.io/github/juancaa03/Minecraft-agent-framework/graph/badge.svg?token=ODXU3JNQH7)](https://codecov.io/github/juancaa03/Minecraft-agent-framework)

Minecraft Agent Framework

Stefan Octavian Tabirca
Juan Carlos Medinilla Alonso

Fecha: 13/01/2025

1. Introducci≤n

El presente proyecto tiene como objetivo el desarrollo de un framework en Python que
permite la creaci≤n y ejecuci≤n de agentes personalizados en un servidor compartido de
Minecraft. Estos agentes pueden interactuar con el entorno del juego, modificar bloques,
y comunicarse a travΘs del chat. El trabajo cumple con los requisitos del enunciado,
incluyendo la demostraci≤n de conceptos de programaci≤n funcional y reflexiva, asφ
como la implementaci≤n de bots como ejemplos prßcticos.

Agentes implementados:

- TNTBot: Genera y detona bloques de TNT cerca de un jugador.
- ChatAI: Responde a mensajes en el chat usando un modelo de lenguaje.
- InsultBot: Emite insultos humorφsticos basados en entradas del chat.

2. Requisitos previos

- Software necesario:

o  Minecraft Java Edition
o  Servidor configurado de Adventures in Minecraft
o  Python 3.9 o superior

- Bibliotecas utilizadas:

o  mcpi: Interacci≤n con el servidor Minecraft.
o  Pyro4: Comunicacion remota cliente-servidor.
o  threading: Control de hilos para bots.
o  dotenv: Carga de credenciales.
o  hugchat: Implementacion de la inteligencia artificial.

- Configuracion del servidor Minecraft:

1.  Descargar el servidor desde Adventures in Minecraft.
2.  Ajustar la memoria asignada modificando el archivo start.sh.
3.  Asegurar la conexi≤n con el cliente Minecraft usando "localhost" como

direcci≤n del servidor.

3. Actualizaci≤n del pluginà

Debido a que nuestro conocimiento tΘcnico sobre el funcionamiento interno del juego
Minecraft es bastante avanzado, nos hemos dado cuenta de una limitaci≤n que era causa
del plugin que interact·a con el servidor. La limitaci≤n en cuesti≤n trata sobre las
entidades en el juego:

A la hora de implementar el TNTBot, con las funciones que ofrecφa la API original tan
solo nos permitφa crear bloques en el entorno, por lo que para generar un TNT cerca del
jugador, la ·nica manera de hacerlo era con bloques, pero eso no tiene ning·n reto ya
que hasta que el jugador no decida golpear el bloque de TNT, Θste no se enciende.

Aquφ es donde entra en juego los aspectos mßs tΘcnicos del juego, siendo el aspecto
relevante para el TNTBot, es que al encender un bloque de TNT, deja de ser un bloque y
se convierte en una entidad, por lo que lo que el TNTBot debe hacer, es generar una
entidad de TNT encendido, pero eso no estaba implementado en la API asφ que no se
podφa hacer nativamente.

Entonces decidimos buscar informaci≤n en internet sobre c≤mo funciona el plugin
internamente, que archivos y funciones de python crea y utiliza para ver si lo podemos
modificar de alguna manera hasta que dimos con una pßgina donde se podφan descargar
diferentes versiones del mismo plugin. Allφ fue cuando encontramos una versi≤n mßs
reciente la cual incorporaba exactamente las funciones que necesitßbamos para generar
entidades, ademßs de algunas otras funciones ·tiles que tambiΘn hemos utilizado, como
obtener el nombre del jugador utilizando su ID de entidad.

Todos los archivos de la nueva versi≤n del plugin los pudimos descargar desde el
siguiente github, perteneciente al mismo creador de la API mcpi, y tambiΘn el propio
plugin (.jar) desde la pßgina spigotmc.org, siendo la versi≤n mßs reciente y que nosotros
hemos utilizado la 1.12.1:

https://github.com/martinohanlon/mcpi

https://www.spigotmc.org/resources/raspberryjuice.22724/history

4. Arquitectura del sistema

El sistema estß compuesto por los siguientes m≤dulos:

4.1 BotManager

ò

Implementa el patr≤n de dise±o Singleton para garantizar una ·nica instancia
global.

ò  Gestiona las listas de jugadores y bots asociados.
ò  Se asegura de actualizar los estados de los bots al detectar cambios en los

jugadores conectados.

4.2 Clases de bots

Cada bot hereda de una clase abstracta Bot, que define unas propiedades y operaciones
bßsicas como:

ò  begin(): Inicia el bot.
ò  stop(): Detiene el bot.

Descripci≤n de bots implementados:

ò  TNTBot:

o  Genera bloques de TNT encendida sobre el jugador en intervalos

aleatorios.

o  Usa la funci≤n spawnEntity para colocar explosivos cerca del jugador.

ò  ChatAI:

o  Escucha el chat en busca de comandos que comiencen con :gpt.
o  Responde utilizando un modelo de lenguaje conectado mediante

hugchat.

ò

InsultBot:

o  Genera respuestas humorφsticas o insultos basados en mensajes del

jugador.

4.3 Comunicaci≤n remota

ò  Servidor Pyro (pyro_server.py):

o  Expone una interfaz para activar y desactivar bots, enviar mensajes al

chat y consultar jugadores conectados.

ò  Cliente Pyro (pyro_client.py):

o  Permite al usuario interactuar con el servidor de manera remota mediante

comandos.

5. Implementaci≤n del sistema

5.1 Flujo principal (practica.py)

ò  El script principal gestiona:

1.  La inicializaci≤n de BotManager.
2.  La actualizaci≤n dinßmica de jugadores conectados.
3.  El procesamiento de comandos personalizados del chat.
ò  Comandos disponibles en el juego* (insensible a may·sculas):

o  :enableTNT / :disableTNT: Activa o desactiva el TNTBot.
o  :enableGPT / :disableGPT: Activa o desactiva el ChatAI.
o  :enableInsult / :disableInsult: Activa o desactiva el InsultBot.
o  :endProgram: Detiene todos los bots y finaliza la ejecuci≤n.

*Los comandos de cada bot son individuales para cada jugador, es decir, cada
jugador tiene su propio bot asignado y solo puede ser activado/desactivado por
el jugador mismo

5.2 Ejecuci≤n remota

ò  El servidor Pyro expone mΘtodos como enable_bot, disable_bot y

send_message.

ò  El cliente Pyro ofrece una interfaz fßcil de usar para interactuar con el servidor

pyro, que a su vez interactuarß con el juego de Minecraft.

6. Pruebas unitarias

Se desarrollaron pruebas automßticas utilizando pytest, cubriendo los siguientes casos:

ò  Activaci≤n y desactivaci≤n de cada tipo de bot.
ò  Validaci≤n de la conexi≤n con el servidor Pyro.
ò  Envio de mensajes y verificaci≤n de jugadores conectados.

Integraci≤n con GitHub Actions:

ò  Los tests se ejecutan automßticamente en cada push al repositorio.
ò  Los resultados se suben a Codecov para generar un reporte de cobertura.
ò  En el repositorio de GitHub se incluye un badge de Codecov que muestra el

porcentaje de cobertura alcanzado.

7. Conclusi≤n

Este proyecto cumple con los requisitos establecidos, destacando por su
modularidad y extensibilidad. Los bots implementados demuestran conceptos
avanzados de programaci≤n funcional y reflexiva.

Ademßs, tambiΘn posee un gran potencial de expansi≤n debido a la simplicidad de los
diferentes componentes del framework y serφa muy sencillo crear un nuevo bot sin tener
que modificar mucho c≤digo ya existente.


