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

# Funcion para activar bots
def enableBot(player, bot_type):
    bot_manager.get_bot_list(bot_type)[player].begin()

# Funcion para desactivar bots
def disableBot(player, bot_type):
    bot_list = bot_manager.get_bot_list(bot_type)
    bot_list[player].stop()
    del bot_list[player]
    if bot_type == 'TNT':
        bot_list[player] = bots.TNT(player)
    elif bot_type == 'ChatAI':
        bot_list[player] = bots.ChatAI(player)
    elif bot_type == 'Insult':
        bot_list[player] = bots.Insult(player)


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
            enableBot(player, 'TNT')
            
        elif (text.casefold() == ":disableTNT".casefold()):
            disableBot(player, 'TNT')
            
        elif (text.casefold() == ":enableGPT".casefold()):
            enableBot(player, 'ChatAI')
            
        elif (text.casefold() == ":disableGPT".casefold()):
            disableBot(player, 'ChatAI')

        elif (text.casefold() == ":enableInsult".casefold()):
            enableBot(player, 'Insult')
            
        elif (text.casefold() == ":disableInsult".casefold()):
            disableBot(player, 'Insult')
            
        elif (text.casefold() == ":endProgram".casefold()):
            # Detener todos los bots y terminar el programa
            for bot_type in ['TNT', 'ChatAI', 'Insult']:
                bot_list = bot_manager.get_bot_list(bot_type)
                list(map(stop_bot, bot_list.values()))
            Script = 0  # Command to finish the execution of this program



mc.postToChat("§a<MAIN> ***Ended execution of main program!!")