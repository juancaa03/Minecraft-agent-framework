import mcpi.minecraft as game
import Pyro4 as pyro
import time
import botclass as bots


# Connect to the Minecraft game
mc = game.Minecraft.create()
Script = 1

while(Script):
    chatEvents = mc.events.pollChatPosts()
    for command in chatEvents:
        if (command.message == ":enableTNT"):
            TNTBot = bots.TNT()
            TNTBot.begin()
            
        elif (command.message == ":disableTNT"):
            TNTBot.stop()
            
        elif (command.message == ":endProgram"):
            Script = 0
            
mc.postToChat("***Ended execution of main program!!")  