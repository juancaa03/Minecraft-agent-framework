class BotManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BotManager, cls).__new__(cls)
            # Inicializar atributos en la primera instancia
            cls._instance.player_list = []
            cls._instance.tnt_bot_list = {}
            cls._instance.chat_ai_bot_list = {}
            cls._instance.insult_bot_list = {}
        return cls._instance

    def update_player_list(self, mc, bot_classes):
        """Actualiza las listas de jugadores y bots para cada jugador."""
        new_player_list = mc.getPlayerEntityIds()
        if new_player_list != self.player_list:
            self.player_list = new_player_list
            # Usar map() con una lambda para crear las listas de bots por tipo
            self.tnt_bot_list = dict(map(lambda entity: (entity, bot_classes['TNT'](entity)), self.player_list))
            self.chat_ai_bot_list = dict(map(lambda entity: (entity, bot_classes['ChatAI'](entity)), self.player_list))
            self.insult_bot_list = dict(map(lambda entity: (entity, bot_classes['Insult'](entity)), self.player_list))

    def get_bot_list(self, bot_type):
        """Obtiene la lista de bots del tipo especificado."""
        if bot_type == 'TNT':
            return self.tnt_bot_list
        elif bot_type == 'ChatAI':
            return self.chat_ai_bot_list
        elif bot_type == 'Insult':
            return self.insult_bot_list
        else:
            raise ValueError("Invalid bot type")
