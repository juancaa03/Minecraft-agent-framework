import mcpi.minecraft as game
import botclass as bots

# Instanciar el BotManager Singleton
bot_manager = bots.BotManager.getInstance()
print(bot_manager)

mc = game.Minecraft.create()    # Connect to the Minecraft game
Script = 1  # Control variable to exit program when finished

# Función para detener los bots
def stop_bot(bot):
    bot.stop()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# * Add bot dict for every new implemented bot and include the dict in the updatePlayerList function !!!! *
# *********************************************************************************************************

# Actualización inicial
bot_manager.printLists()
bot_manager.update_player_list(mc)
bot_manager.printLists()

# Main program start
mc.postToChat("§a<MAIN> ***Main program has started!!")

# Execute until player wishes to stop it
while(Script):
    bot_manager.update_player_list(mc)
    
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
            TNTbotList = bot_manager.get_bot_list('TNT')    # Obtain the list of the specified bot
            TNTbotList[player].stop()  # Stop the TNT bot for the player who ordered it
            del TNTbotList[player]  # Delete the object (thread) for this player
            TNTbotList[player] = bots.TNT(player)   # And create a new one that is ready
            
            
        elif (text.casefold() == ":enableGPT".casefold()):
            bot_manager.get_bot_list('ChatAI')[player].begin()  # Inicia el bot de ChatAI para el jugador que lo ordenó
            
        elif (text.casefold() == ":disableGPT".casefold()):
            GPTbotList = bot_manager.get_bot_list('ChatAI')    # Obtain the list of the specified bot
            GPTbotList[player].stop()  # Stop the TNT bot for the player who ordered it
            del GPTbotList[player]  # Delete the object (thread) for this player
            GPTbotList[player] = bots.ChatAI(player)   # And create a new one that is ready


        elif (text.casefold() == ":enableInsult".casefold()):
            bot_manager.get_bot_list('Insult')[player].begin()  # Inicia el bot de ChatAI para el jugador que lo ordenó
            
        elif (text.casefold() == ":disableInsult".casefold()):
            InsultBotList = bot_manager.get_bot_list('Insult')    # Obtain the list of the specified bot
            InsultBotList[player].stop()  # Stop the TNT bot for the player who ordered it
            del InsultBotList[player]  # Delete the object (thread) for this player
            InsultBotList[player] = bots.Insult(player)   # And create a new one that is ready
            
            
        elif (text.casefold() == ":endProgram".casefold()):
            # Detener todos los bots y terminar el programa
            for bot_type in ['TNT', 'ChatAI', 'Insult']:
                bot_list = bot_manager.get_bot_list(bot_type)
                list(map(stop_bot, bot_list.values()))
            Script = 0  # Command to finish the execution of this program



mc.postToChat("§a<MAIN> ***Ended execution of main program!!")