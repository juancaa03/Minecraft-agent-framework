import mcpi.minecraft as game
import Pyro4 as pyro
import time
import botclass as bots
from BotManager import BotManager

# Instanciar el BotManager Singleton
bot_manager = BotManager()

# Diccionario para registrar clases de bots
bot_classes = {
    'TNT': bots.TNT,
    'ChatAI': bots.ChatAI,
    'Insult': bots.Insult,
}

mc = game.Minecraft.create()    # Connect to the Minecraft game
Script = 1  # Control variable to exit program when finished

# Función para detener los bots
def stop_bot(bot):
    bot.stop()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# * Add bot dict for every new implemented bot and include the dict in the updatePlayerList function !!!! *
# *********************************************************************************************************

# Actualización inicial
bot_manager.update_player_list(mc, bot_classes)

# Main program start
mc.postToChat("§a<MAIN> ***Main program has started!!")

# Execute until player wishes to stop it
while(Script):
    bot_manager.update_player_list(mc, bot_classes)
    
    # Read chat to see if anyone used a custom command
    chatEvents = mc.events.pollChatPosts()
    
    for command in chatEvents:  
        text = str(command.message) # Convert chat event to str
        if(not text.startswith(":")):   # Skip if it doesn't start with ":"
            continue
        
        player = command.entityId   # Else, register what player sent the command
        
        # Check what command was executed (ignore case)
        if (text.casefold() == ":enableTNT".casefold()):
            bot_manager.get_bot_list('TNT')[player].begin() # Start TNT bot for the player who ordered it
            
        elif (text.casefold() == ":disableTNT".casefold()):
            bot_manager.get_bot_list('TNT')[player].stop()   # Stop the TNT bot for the player who ordered it
            bot_manager.update_player_list(mc, bot_classes)
            
        elif (text.casefold() == ":enableGPT".casefold()):
            bot_manager.get_bot_list('ChatAI')[player].begin()  # Inicia el bot de ChatAI para el jugador que lo ordenó
            
        elif (text.casefold() == ":disableGPT".casefold()):
            bot_manager.get_bot_list('ChatAI')[player].stop()
            bot_manager.update_player_list(mc, bot_classes)

        elif (text.casefold() == ":enableInsult".casefold()):
            bot_manager.get_bot_list('Insult')[player].begin()  # Inicia el bot de ChatAI para el jugador que lo ordenó
            
        elif (text.casefold() == ":disableInsult".casefold()):
            bot_manager.get_bot_list('Insult')[player].stop()
            bot_manager.update_player_list(mc, bot_classes)
            
        elif (text.casefold() == ":endProgram".casefold()):
            # Detener todos los bots y terminar el programa
            for bot_type in ['TNT', 'ChatAI', 'Insult']:
                bot_list = bot_manager.get_bot_list(bot_type)
                list(map(stop_bot, bot_list.values()))
            Script = 0  # Command to finish the execution of this program



mc.postToChat("§a<MAIN> ***Ended execution of main program!!")