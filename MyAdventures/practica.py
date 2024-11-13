import mcpi.minecraft as game
import Pyro4 as pyro
import time
import botclass as bots

# Function to update the lists of bots, each assigned to a player (some of them)
def updatePlayerList():
    """Returns a list of players, followed by dictionaries of the bots that require to be
    unique for each player in particular"""
    list = mc.getPlayerEntityIds()  # Obtain a list of all connected players
    
    # For every player online, create a bot (do the same for every kind of bot)
    TNTbotList = {entity: bots.TNT(entity) for entity in list}
    # <<<< Add the new bot dicts here to update them as well >>>>
    
    return (list, TNTbotList)
    

mc = game.Minecraft.create()    # Connect to the Minecraft game
Script = 1  # Control variable to exit program when finished


# Player list, dictionaries for the bots that are unique to each player, and singular bots
playerList = []

TNTbotList = {}
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# * Add bot dict for every new implemented bot and include the dict in the updatePlayerList function !!!! *
# *********************************************************************************************************

playerList, TNTbotList = updatePlayerList()   	# Lists initialisation

# Main program start
mc.postToChat("<MAIN> ***Main program has started!!")

# Execute until player wishes to stop it
while(Script):
    # If a new player joins, we want to assign them a bot so we update the lists
    if(len(mc.getPlayerEntityIds()) != len(playerList)):
        playerList, TNTbotList = updatePlayerList()
    
    # Read chat to see if anyone used a custom command
    chatEvents = mc.events.pollChatPosts()
    
    for command in chatEvents:
        text = str(command.message) # Convert chat event to str
        if(not text.startswith(":")):   # Skip if it doesn't start with ":"
            continue
        
        player = command.entityId   # Else, register what player sent the command
        
        # Check what command was executed (ignore case)
        if (text.casefold() == ":enableTNT".casefold()):
            TNTbotList[player].begin() # Start TNT bot for the player who ordered it
            
        elif (text.casefold() == ":disableTNT".casefold()):
            TNTbotList[player].stop()   # Stop the TNT bot for the player who ordered it
            del TNTbotList[player]  # Delete the object (thread) for this player
            TNTbotList[player] = bots.TNT(player)   # And create a new one that is ready
            
        elif (text.casefold() == ":endProgram".casefold()):
            for player in playerList:
                TNTbotList[player].stop()   # Make sure there are no threads running before closing program
            Script = 0  # Command to finish the execution of this program
            
mc.postToChat("<MAIN> ***Ended execution of main program!!")  