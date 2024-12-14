import Pyro4
import mcpi.minecraft as game
from BotManager import BotManager
from botclass import TNT, ChatAI, Insult  # Importar clases de bots

# Inicializar el servidor Pyro
@Pyro4.expose
class MinecraftPyroServer:
    def __init__(self):
        self.mc = game.Minecraft.create()
        self.bot_manager = BotManager()  # Crear instancia de BotManager con Minecraft

    def send_message(self, message):
        self.mc.postToChat(message)
        return f"Mensaje enviado: {message}"
    
    def get_players(self):
        try:
            players = self.mc.getPlayerEntityIds()
            return players
        except Exception as e:
            return f"Error al obtener jugadores: {e}"

    def enable_bot(self, bot_type, player_id):
        try:
            # Actualizar la lista de jugadores y bots
            self.bot_manager.update_player_list(
                self.mc,  # Pasar la instancia de Minecraft
                {'TNT': TNT, 'ChatAI': ChatAI, 'Insult': Insult}  # Pasar las clases de bots
            )
            bot_list = self.bot_manager.get_bot_list(bot_type)
            if player_id not in bot_list:
                return f"El jugador con ID {player_id} no está conectado o no tiene un bot disponible."

            bot = bot_list[player_id]
            bot.begin()
            return f"Bot {bot_type} activado para el jugador {player_id}."
        except Exception as e:
            return f"Error: {e}"

    def disable_bot(self, bot_type, player_id):
        try:
            bot_list = self.bot_manager.get_bot_list(bot_type)
            if player_id not in bot_list:
                return f"El jugador con ID {player_id} no tiene un bot de tipo {bot_type} activo."

            bot = bot_list[player_id]
            bot.stop()
            del bot_list[player_id]  # Eliminar el bot de la lista
            return f"Bot {bot_type} desactivado para el jugador {player_id}."
        except Exception as e:
            return f"Error: {e}"


# Iniciar el servidor Pyro
if __name__ == "__main__":
    daemon = Pyro4.Daemon(host="0.0.0.0", port=9090).serveSimple({ MinecraftPyroServer: "practicatap.practica" }, ns = True)
    uri = daemon.register(MinecraftPyroServer())
    print(f"Servidor Pyro iniciado en {uri}")
    daemon.requestLoop()