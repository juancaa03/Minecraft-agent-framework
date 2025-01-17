import Pyro4
import mcpi.minecraft as game
import botclass as bots

# Inicializar el servidor Pyro
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class MinecraftPyroServer:
    def __init__(self):
        self.mc = game.Minecraft.create()
        self.bot_manager = bots.BotManager.getInstance()  # Crear instancia de BotManager con Minecraft
        print(self.bot_manager)
        self.bot_manager.update_player_list(self.mc)
        self.bot_manager.printLists()
        self.mc.postToChat("§5<Pyro4> Pyro4 Server currently running...")

    # Funcion para activar bots
    def enableBot(self, player, bot_type):
        self.bot_manager.get_bot_list(bot_type)[player].begin()

    # Funcion para desactivar bots
    def disableBot(self, player, bot_type):
        bot_list = self.bot_manager.get_bot_list(bot_type)
        bot_list[player].stop()
        del bot_list[player]
        if bot_type == 'TNT'.casefold():
            bot_list[player] = bots.TNT(player)
        elif bot_type == 'ChatAI'.casefold():
            bot_list[player] = bots.ChatAI(player)
        elif bot_type == 'Insult'.casefold():
            bot_list[player] = bots.Insult(player)

    def send_message(self, message):
        self.mc.postToChat("§5<Pyro4> " + message)
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
            self.bot_manager.update_player_list(self.mc)
            self.enableBot(player_id, bot_type)
            return f"Bot {bot_type} activado para el jugador {player_id}."
        except Exception as e:
            return f"Error: {e}"

    def disable_bot(self, bot_type, player_id):
        try:
            # Actualizar la lista de jugadores y bots
            self.bot_manager.update_player_list(self.mc)
            self.disableBot(player_id, bot_type)
            return f"Bot {bot_type} desactivado para el jugador {player_id}."
        except Exception as e:
            return f"Error: {e}"
        
    def show_bots(self):
        for bot_type in ['TNT', 'ChatAI', 'Insult']:
                bot_list = self.bot_manager.get_bot_list(bot_type)
                print(f"{bot_list.values()}")
                
    def wake_server(self):
        return f"The server is connected and active!"


# Iniciar el servidor Pyro
if __name__ == "__main__":
    daemon = Pyro4.Daemon.serveSimple({ MinecraftPyroServer: "practicatap.practica" },  # Nombre del objeto en el servidor pyro4
                                      host = "0.0.0.0",     # 0.0.0.0 para exponer el servidor a internet
                                      port = 9090,  # Puerto por defecto del servidor pyro4
                                      ns = False,   # No usar Nameserver
                                      verbose = True)   # Mostrar informacion adicional
    uri = daemon.register(MinecraftPyroServer())
    print(f"Servidor Pyro iniciado en {uri}")
    daemon.requestLoop()