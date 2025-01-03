import unittest
import Pyro4
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from MyAdventures.mcpi import minecraft as game
from MyAdventures import botclass
from MyAdventures import pyro_server  # Importa las funciones que necesitas probar
from MyAdventures import pyro_client  # Importa las funciones que necesitas probar
from MyAdventures import practica  # Importa las funciones enableBot y disableBot

class TestPracticaFunctions(unittest.TestCase):

        # Conectar al servidor Pyro
    def connect_to_server():
        # Dirección del servidor Pyro (debe coincidir con la URI del servidor)
        try:
            server = Pyro4.Proxy("PYRO:practicatap.practica@73f4n.ddns.net:9090")  # Conectar al servidor Pyro
            return server
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")
            exit(1)

    mc = game.Minecraft.create()
    player_list = mc.getPlayerEntityIds()
    server = connect_to_server()

    def test_activar_tnt(self):
        result = enableBot(self.player_list[0], 'TNT')
        self.assertEqual(result, None)
    
    def test_activar_ai(self):
        result = enableBot(self.player_list[0], 'ChatAI')
        self.assertEqual(result, None)

    def test_activar_insult(self):
        result = enableBot(self.player_list[0], 'Insult')
        self.assertEqual(result, None)

    def test_desactivar_tnt(self):
        result = disableBot(self.player_list[0], 'TNT')
        self.assertEqual(result, None)

    def test_desactivar_ai(self):
        result = disableBot(self.player_list[0], 'ChatAI')
        self.assertEqual(result, None)

    def test_desactivar_insult(self):
        result = disableBot(self.player_list[0], 'Insult')
        self.assertEqual(result, None)

    def test_mostrar_bots(self):
        result = server.show_bots()
        self.assertEqual(result, None)

    def test_enviar_mensaje(self):
        result = server.send_message("Mensaje de prueba")
        self.assertEqual(result, "Mensaje enviado: Mensaje de prueba")
        
    def test_obtener_jugadores(self):
        result = server.get_players()
        self.assertEqual(result, self.player_list)
    
    def test_activar_bot(self):
        result = server.enable_bot('TNT', self.player_list[0])
        self.assertEqual(result, f"Bot TNT activado para el jugador {self.player_list[0]}.")

    def test_desactivar_bot(self):
        result = server.disable_bot('TNT', self.player_list[0])
        self.assertEqual(result, f"Bot TNT desactivado para el jugador {self.player_list[0]}.")

if __name__ == '__main__':
    unittest.main()

# Use: python -m unittest tests.py