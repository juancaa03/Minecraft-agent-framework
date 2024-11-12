import mcpi.minecraft as game
import mcpi.block as blocks
import mcpi.entity as entities
import mcpi.event as events
import Pyro4 as pyro
import time


# Connect to the Minecraft game
mc = game.Minecraft.create()
TNTControl = 0
Script = 1
while(Script):
    chatEvents = mc.events.pollChatPosts()
    for command in chatEvents:
        if (command.message == ":enableTNT"):
            TNTControl = 1
            mc.postToChat("TNT Bot has been activated")
        elif (command.message == ":disableTNT"):
            TNTControl = 0
            mc.postToChat("TNT Bot has been deactivated")
        elif (command.message == ":stopScript"):
            Script = 0
    
    if(TNTControl):
            pos = mc.player.getTilePos()    # Get player position
            floor = mc.getBlock(pos.x, pos.y-1, pos.z)  # Check what block the player is standing on
            if(floor != blocks.AIR.id and floor != blocks.WATER.id and floor != blocks.WATER_STATIONARY.id):	# If the player is not flying or swimming
                mc.spawnEntity(pos.x, pos.y+2, pos.z, entities.PRIMED_TNT.id)   # Spawn an ignited TNT on top of the player

mc.postToChat("Ended execution of script!")