import Pyro4
import mcpi.minecraft as game
from BotManager import BotManager

# Inicializar el servidor Pyro
@Pyro4.expose
class MinecraftPyroServer:
    def __init__(self, mc, bot_manager):
        self.mc = mc
        self.bot_manager = bot_manager

    def send_message(self, message):
        self.mc.postToChat(message)
        return f"Mensaje enviado: {message}"

    def enable_bot(self, bot_type, player_id):
        bot_list = self.bot_manager.get_bot_list(bot_type)
        if player_id not in bot_list:
            return f"Jugador {player_id} no tiene un bot de tipo {bot_type}."
        bot_list[player_id].begin()
        return f"Bot {bot_type} activado para el jugador {player_id}."

    def disable_bot(self, bot_type, player_id):
        bot_list = self.bot_manager.get_bot_list(bot_type)
        if player_id not in bot_list:
            return f"Jugador {player_id} no tiene un bot de tipo {bot_type}."
        bot_list[player_id].stop()
        return f"Bot {bot_type} desactivado para el jugador {player_id}."

# Iniciar el servidor Pyro
if __name__ == "__main__":
    mc = game.Minecraft.create()
    bot_manager = BotManager()

    daemon = Pyro4.Daemon()  # Iniciar demonio Pyro
    uri = daemon.register(MinecraftPyroServer(mc, bot_manager))
    print(f"Servidor Pyro iniciado en {uri}")
    daemon.requestLoop()
