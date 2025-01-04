import sys
import os
import pytest
import Pyro4

# Asegura que el directorio base y MyAdventures están en el PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importaciones desde MyAdventures
import mcpi.minecraft as game
import botclass
import pyro_server
import pyro_client
import practica

# Función para conectar al servidor Pyro
@pytest.fixture(scope="module")
def server():
    try:
        return Pyro4.Proxy("PYRO:practicatap.practica@73f4n.ddns.net:9090")
    except Exception as e:
        pytest.fail(f"Error al conectar al servidor: {e}")

# Crear instancia de Minecraft y obtener la lista de jugadores
@pytest.fixture(scope="module")
def minecraft_data():
    mc = game.Minecraft.create()
    player_list = mc.getPlayerEntityIds()
    return mc, player_list

def test_activar_tnt(minecraft_data):
    mc, player_list = minecraft_data
    result = practica.enableBot(player_list[0], 'TNT')
    assert result is None

def test_activar_ai(minecraft_data):
    mc, player_list = minecraft_data
    result = practica.enableBot(player_list[0], 'ChatAI')
    assert result is None

def test_activar_insult(minecraft_data):
    mc, player_list = minecraft_data
    result = practica.enableBot(player_list[0], 'Insult')
    assert result is None

def test_desactivar_tnt(minecraft_data):
    mc, player_list = minecraft_data
    result = practica.disableBot(player_list[0], 'TNT')
    assert result is None

def test_desactivar_ai(minecraft_data):
    mc, player_list = minecraft_data
    result = practica.disableBot(player_list[0], 'ChatAI')
    assert result is None

def test_desactivar_insult(minecraft_data):
    mc, player_list = minecraft_data
    result = practica.disableBot(player_list[0], 'Insult')
    assert result is None
'''
def test_mostrar_bots(server):
    result = server.show_bots()
    assert result is None

def test_enviar_mensaje(server):
    result = server.send_message("Mensaje de prueba")
    assert result == "Mensaje enviado: Mensaje de prueba"

def test_obtener_jugadores(server, minecraft_data):
    _, player_list = minecraft_data
    result = server.get_players()
    assert result == player_list

def test_activar_bot(server, minecraft_data):
    _, player_list = minecraft_data
    result = server.enable_bot('TNT', player_list[0])
    assert result == f"Bot TNT activado para el jugador {player_list[0]}."

def test_desactivar_bot(server, minecraft_data):
    _, player_list = minecraft_data
    result = server.disable_bot('TNT', player_list[0])
    assert result == f"Bot TNT desactivado para el jugador {player_list[0]}."'''


# Generate coverage report: pytest --cov --cov-config=./.coveragerc --cov-report term-missing --junitxml=junit.xml -o junit_family=legacy
