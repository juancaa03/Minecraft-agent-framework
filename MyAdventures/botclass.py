import mcpi.minecraft as game
import mcpi.block as blocks
import mcpi.entity as entities
import mcpi.event as events
import random
import time
from threading import Thread
from dotenv import dotenv_values
from hugchat import hugchat
from hugchat.login import Login


# main abstract class for a bot
class Bot():
    def __init__(self, entity):
        self.mc = game.Minecraft.create()   # minecraft game server connection
        self.entity = entity    # player who called the function
        self.control = None     # control variable for main loop in bot function
        self.t1 = Thread        # declaration of a thread for the bot (needs to be updated by the specific bot)
        self.player_name = self.mc.entity.getName(self.entity)
    
    # main function to start a thread with the bot
    def begin(self):
        if(not self.t1.is_alive()):
            self.control = True
            self.t1.start()
            self.mc.postToChat(f"§2<{self.name}> ***The bot has been enabled for {self.player_name}!!")
        else:
            self.mc.postToChat(f"§2<{self.name}> ***The bot is already running for {self.player_name}!!")
    
    # main function to stop the bot thread
    def stop(self):
        if(self.t1.is_alive()):
            self.control = False
            self.t1.join()
            self.mc.postToChat(f"§2<{self.name}> ***The bot has been disabled for {self.player_name}!!")
        else:
            self.mc.postToChat(f"§2<{self.name}> ***The bot is not running yet for {self.player_name}!!")
        
        
# specific bot class to spawn TNT near the player
class TNT(Bot):
    def __init__(self, entity):
        super().__init__(entity)  # inherit attributes
        self.name = "TNTBot"    # name of this specific bot
        self.t1 = Thread(target=self._main) # update thread with the function to execute
        self.counter = 0
        
    # specific function of the TNT bot
    def _main(self):
        while(self.control):    # run while the bot is enabled
            if self.counter > 0:
                time.sleep(1)
                self.counter = self.counter - 1
            else:
                self.counter = random.randint(3, 15)
                # spawn TNT once in a random interval between 3 and 15 seconds
                pos = self.mc.entity.getTilePos(self.entity)    # Get player position
                self.mc.spawnEntity(pos.x, pos.y+2, pos.z, entities.PRIMED_TNT.id)   # Spawn an ignited TNT on top of the player




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
        # HugChat setup
        try:
            secrets = dotenv_values('C:\\users\\stef2\\Desktop\\Minecraft-agent-framework\\MyAdventures\\hf.env')
            self.hf_email = secrets['EMAIL']
            self.hf_pass = secrets['PASS']
        except Exception as e:
            print(f"§2Error loading HugChat credentials: {e}")

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
                    self.handle_gpt_command(text + "  ")

    # Function to handle GPT prompts
    def handle_gpt_command(self, prompt):
        try:
            response = generate_response(prompt, self.hf_email, self.hf_pass)
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
        # HugChat setup
        try:
            secrets = dotenv_values('C:\\users\\stef2\\Desktop\\Minecraft-agent-framework\\MyAdventures\\hf.env')
            self.hf_email = secrets['EMAIL']
            self.hf_pass = secrets['PASS']
        except Exception as e:
            print(f"§2Error loading HugChat credentials: {e}")

    # Main function for the Insult bot (to process commands)
    def _main(self):
        while self.control:
            chatEvents = self.mc.events.pollChatPosts()
            
            for command in chatEvents:
                text = str(command.message) # Convert chat event to str
                sender_entity_id = command.entityId
                if sender_entity_id == self.bot_entity_id:
                    continue
                
                if(not text.startswith(":") and not text.startswith("<")):
                    self.insult_command("Generate low insults for this player: "+ self.player_name + "(Keep it short please), he typed this: "+text)


    # Function to handle GPT prompts
    def insult_command(self, prompt):
        try:
            response = generate_response(prompt, self.hf_email, self.hf_pass)
            self.mc.postToChat(f"<Insult> {response}")  # Limit response length
            #response.close();
        except Exception as e:
            self.mc.postToChat(f"<Insult> Error: {str(e)}")

class BotManager:
    __instance = None
    player_list = []
    tnt_bot_list = {}
    chat_ai_bot_list = {}
    insult_bot_list = {}
    
    @staticmethod
    def getInstance():
        if BotManager.__instance == None:
            BotManager()
        return BotManager.__instance
    
    def __init__(self):
        if BotManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BotManager.__instance = self
    

    def update_player_list(self, mc):
        """Actualiza las listas de jugadores y bots para cada jugador."""
        new_player_list = mc.getPlayerEntityIds()
        if len(new_player_list) > len(self.player_list):
            diff = list(set(new_player_list).difference(self.player_list))
            self.player_list.extend(diff)
            for player in diff:
                self.tnt_bot_list[player] = TNT(player)
                self.chat_ai_bot_list[player] = ChatAI(player)
                self.insult_bot_list[player] = Insult(player)
            self.printLists()
        
        elif len(new_player_list) < len(self.player_list):
            diff = list(set(self.player_list).difference(new_player_list))
            self.player_list = new_player_list  #[x for x in self.player_list if x in new_player_list]
            for player in diff:
                self.tnt_bot_list[player].stop()
                del self.tnt_bot_list[player]
                
                self.chat_ai_bot_list[player].stop()
                del self.chat_ai_bot_list[player]
                
                self.insult_bot_list[player].stop()
                del self.insult_bot_list[player]
            self.printLists()
            
            
            # Usar map() con una lambda para crear las listas de bots por tipo
            #self.tnt_bot_list = dict(map(lambda entity: (entity, TNT(entity)), self.player_list))
            #self.chat_ai_bot_list = dict(map(lambda entity: (entity, ChatAI(entity)), self.player_list))
            #self.insult_bot_list = dict(map(lambda entity: (entity, Insult(entity)), self.player_list))

    
    def get_bot_list(self, bot_type):
        """Obtiene la lista de bots del tipo especificado."""
        
        print(f"Received bot type: {bot_type}")
        if bot_type == 'TNT'.casefold():
            return self.tnt_bot_list
        elif bot_type == 'ChatAI'.casefold():
            return self.chat_ai_bot_list
        elif bot_type == 'Insult'.casefold():
            return self.insult_bot_list
        else:
            raise ValueError("Invalid bot type")
    
    
    def printLists(self):
        print("Player list = "+str(self.player_list))
        print("TNT list = "+str(self.tnt_bot_list))
        print("GPT list = "+str(self.chat_ai_bot_list))
        print("Insult list = "+str(self.insult_bot_list))