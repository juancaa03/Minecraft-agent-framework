import mcpi.minecraft as game
import mcpi.block as blocks
import mcpi.entity as entities
import mcpi.event as events
from threading import Thread


# main abstract class for a bot
class Bot:
    def __init__(self):
        self.mc = game.Minecraft.create()   # minecraft game server connection
        self.control = None     # control variable for main loop in bot function
        self.t1 = Thread        # declaration of a thread for the bot (needs to be updated by the specific bot)
    
    # main function to start a thread with the bot
    def begin(self):
        if(not self.t1.is_alive()):
            self.control = True
            self.t1.start()
        else:
            self.mc.postToChat("***The bot is already running!!")
    
    # main function to stop the bot thread
    def stop(self):
        if(self.t1.is_alive()):
            self.control = False
            self.t1.join()
            self.mc.postToChat("***The bot has been disabled!!")
        else:
            self.mc.postToChat("***The bot is not running yet!!")
        
        
# specific bot class to spawn TNT near the player
class TNT(Bot):
    def __init__(self):
        super().__init__()  # inherit attributes
        self.t1 = Thread(target=self._main) # update thread with the function to execute
        
    # specific function of the TNT bot
    def _main(self):
        while(self.control):    # run while the bot is enabled
            pos = self.mc.player.getTilePos()    # Get player position
            floor = self.mc.getBlock(pos.x, pos.y-1, pos.z)  # Check what block the player is standing on
            if(floor != blocks.AIR.id and floor != blocks.WATER.id and floor != blocks.WATER_STATIONARY.id):	# If the player is not flying or swimming
                    self.mc.spawnEntity(pos.x, pos.y+2, pos.z, entities.PRIMED_TNT.id)   # Spawn an ignited TNT on top of the player