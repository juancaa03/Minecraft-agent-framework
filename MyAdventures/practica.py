
import mcpi.minecraft as game
import mcpi.block as blocks
import mcpi.entity as entities
import mcpi.event as event
import time
import Pyro4 as pyro



# Connect to the Minecraft game
mc = game.Minecraft.create()
TNTBot = 1



while (True):
#    chatEvents = mc.events.pollChatPosts()
#    for command in chatEvents:
#        if (command.message == ":enableTNT"):
#            TNTBot = 1
#            mc.postToChat("TNT Bot has been activated")
#        elif (command.message == ":disableTNT"):
#            TNTBot = 0
#            mc.postToChat("TNT Bot has been deactivated")
            
        
    if(TNTBot == 1):
        pos = mc.player.getTilePos()
        floor = mc.getBlock(pos.x, pos.y-1, pos.z)
        if(floor != blocks.AIR.id and floor != blocks.WATER.id and floor != blocks.WATER_STATIONARY.id):
            #mc.setBlock(pos.x, pos.y, pos.z, blocks.TNT.id)
            #mc.setBlock(pos.x, pos.y-1, pos.z, blocks.REDSTONE_BLOCK.id)
            mc.spawnEntity(pos.x, pos.y+1, pos.z, entities.PRIMED_TNT.id)