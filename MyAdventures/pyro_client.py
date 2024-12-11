# client.py
import Pyro4

# Conectar al servidor Pyro
def connect_to_server():
    # Dirección del servidor Pyro (debe coincidir con la URI del servidor)
    uri = input("Introduce la URI del servidor Pyro: ")
    server = Pyro4.Proxy(uri)  # Conectar al servidor Pyro
    return server

# Enviar comandos para controlar los bots
def interact_with_server(server):
    while True:
        print("Comandos disponibles:")
        print(":sendMessage <message> - Enviar un mensaje al chat")
        print(":enableBot <bot_type> <player_id> - Activar un bot")
        print(":disableBot <bot_type> <player_id> - Desactivar un bot")
        print(":getPlayers - Obtener lista de jugadores")
        print(":exit - Salir del cliente")

        command = input("Introduce un comando: ").strip()

        if command.startswith(":sendMessage"):
            message = command[len(":sendMessage"):].strip()
            response = server.send_message(message)
            print(response)

        elif command.startswith(":enableBot"):
            parts = command.split()
            if len(parts) != 3:
                print("Uso incorrecto. Usa: :enableBot <bot_type> <player_name>")
                continue
            bot_type = parts[1]
            player_id = int(parts[2])
            response = server.enable_bot(bot_type, player_id)
            print(response)

        elif command.startswith(":disableBot"):
            parts = command.split()
            if len(parts) != 3:
                print("Uso incorrecto. Usa: :disableBot <bot_type> <player_id>")
                continue
            bot_type = parts[1]
            player_id = int(parts[2])
            response = server.disable_bot(bot_type, player_id)
            print(response)

        elif command == ":getPlayers":
            players = server.get_players()
            print(f"Jugadores conectados: {players}")

        elif command == ":exit":
            print("Saliendo del cliente...")
            break

        else:
            print("Comando no reconocido.")

if __name__ == "__main__":
    server = connect_to_server()
    interact_with_server(server)
