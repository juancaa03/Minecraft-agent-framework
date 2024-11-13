import mcpi.minecraft as game
import mcpi.block as blocks
import mcpi.entity as entities
import mcpi.event as events
from threading import Thread
import time
import random


# main abstract class for a bot
class Bot:
    def __init__(self, entity):
        self.mc = game.Minecraft.create()   # minecraft game server connection
        self.entity = entity    # player who called the function
        self.control = None     # control variable for main loop in bot function
        self.t1 = Thread        # declaration of a thread for the bot (needs to be updated by the specific bot)
    
    # main function to start a thread with the bot
    def begin(self):
        if(not self.t1.is_alive()):
            self.control = True
            self.t1.start()
            self.mc.postToChat(f"<{self.name}> ***The bot has been enabled for player ID {self.entity}!!")
        else:
            self.mc.postToChat(f"<{self.name}> ***The bot is already running for player ID {self.entity}!!")
    
    # main function to stop the bot thread
    def stop(self):
        if(self.t1.is_alive()):
            self.control = False
            self.t1.join()
            self.mc.postToChat(f"<{self.name}> ***The bot has been disabled for player ID {self.entity}!!")
        else:
            self.mc.postToChat(f"<{self.name}> ***The bot is not running yet for player ID {self.entity}!!")
        
        
# specific bot class to spawn TNT near the player
class TNT(Bot):
    def __init__(self, entity):
        super().__init__(entity)  # inherit attributes
        self.name = "TNTBot"    # name of this specific bot
        self.t1 = Thread(target=self._main) # update thread with the function to execute
        
    # specific function of the TNT bot
    def _main(self):
        while(self.control):    # run while the bot is enabled
            time.sleep(random.randint(3, 30))   # spawn TNT once in a random interval between 3 and 30 seconds
            pos = self.mc.entity.getTilePos(self.entity)    # Get player position
            #floor = self.mc.getBlock(pos.x, pos.y-1, pos.z)  # Check what block the player is standing on
            #if(floor != blocks.AIR.id and floor != blocks.WATER.id and floor != blocks.WATER_STATIONARY.id):	# If the player is not flying or swimming
            self.mc.spawnEntity(pos.x, pos.y+2, pos.z, entities.PRIMED_TNT.id)   # Spawn an ignited TNT on top of the player