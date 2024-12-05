import mcpi.minecraft as game
import mcpi.block as blocks
import mcpi.entity as entities
import mcpi.event as events
from threading import Thread
import time
import random
from dotenv import dotenv_values
from hugchat import hugchat
from hugchat.login import Login


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
            self.mc.postToChat(f"§2<{self.name}> ***The bot has been enabled for player ID {self.entity}!!")
        else:
            self.mc.postToChat(f"§2<{self.name}> ***The bot is already running for player ID {self.entity}!!")
    
    # main function to stop the bot thread
    def stop(self):
        if(self.t1.is_alive()):
            self.control = False
            self.t1.join()
            self.mc.postToChat(f"§2<{self.name}> ***The bot has been disabled for player ID {self.entity}!!")
        else:
            self.mc.postToChat(f"§2<{self.name}> ***The bot is not running yet for player ID {self.entity}!!")
        
        
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


# HugChat setup
try:
    secrets = dotenv_values('hf.env')
    hf_email = secrets['EMAIL']
    hf_pass = secrets['PASS']
except Exception as e:
    print(f"§2Error loading HugChat credentials: {e}")

# Function for generating bot response
def generate_response(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# Main ChatAI Bot Class
class ChatAI(Bot):
    def __init__(self, entity):
        super().__init__(entity)
        self.name = "ChatAI"  # Name of the bot
        self.t1 = Thread(target=self._main)  # Update thread with the function to execute

    # Main function for the ChatAI bot (to process commands)
    def _main(self):
        while self.control:
            chatEvents = self.mc.events.pollChatPosts()
    
            for command in chatEvents:
                text = str(command.message) # Convert chat event to str
                if(not text.startswith(":gpt ")):   # Skip if it doesn't start with ":gpt"
                    continue
                else:
                    text = text[4:]
                    self.handle_gpt_command(text + " (Keep your answer short please and in Minecraft context)")

    # Function to handle GPT prompts
    def handle_gpt_command(self, prompt):
        try:
            response = generate_response(prompt, hf_email, hf_pass)
            self.mc.postToChat(f"<GPT> {response}")  # Limit response length
            #response.close();
        except Exception as e:
            self.mc.postToChat(f"<GPT> Error: {str(e)}")

class Insult(Bot):
    def __init__(self, entity):
        super().__init__(entity)
        self.name = "InsultBot"  # Name of the bot
        self.t1 = Thread(target=self._main)  # Update thread with the function to execute
        self.bot_entity_id = self.t1.name
        self.player_name = self.mc.entity.getName(self.entity)

    # Main function for the Insult bot (to process commands)
    def _main(self):
        while self.control:
            chatEvents = self.mc.events.pollChatPosts()
            
            for command in chatEvents:
                text = str(command.message) # Convert chat event to str
                sender_entity_id = command.entityId
                if sender_entity_id == self.bot_entity_id:
                    continue
                
                if(not text.startswith(":") and not text.startswith("***")):
                    self.insult_command("Generate low insults for this player: "+ self.player_name + "(Keep it short please), he typed this: "+text)


    # Function to handle GPT prompts
    def insult_command(self, prompt):
        try:
            response = generate_response(prompt, hf_email, hf_pass)
            self.mc.postToChat(f"<Insult> {response}")  # Limit response length
            #response.close();
        except Exception as e:
            self.mc.postToChat(f"<Insult> Error: {str(e)}")
