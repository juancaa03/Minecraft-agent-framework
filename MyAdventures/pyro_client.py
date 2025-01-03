import Pyro4

# Conectar al servidor Pyro
def connect_to_server():
    # Dirección del servidor Pyro (debe coincidir con la URI del servidor)
    try:
        server = Pyro4.Proxy("PYRO:practicatap.practica@73f4n.ddns.net:9090")  # Conectar al servidor Pyro
        print("Conexión exitosa al servidor.")
        return server
    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
        exit(1)

# Enviar comandos para controlar los bots
def interact_with_server(server):
    response = server.wake_server()
    print(response)
    
    while True:
        print("\nBots disponibles:\nTNT - ChatAI - Insult")
        print("Comandos disponibles:")
        print(":sendMessage <message> - Enviar un mensaje al chat")
        print(":enableBot <bot_type> <player_id> - Activar un bot")
        print(":disableBot <player_id> - Desactivar un bot")
        print(":getPlayers - Obtener lista de jugadores conectados")
        print(":exit - Salir del cliente")
        

        command = input("Introduce un comando: ").strip().casefold()

        try:
            if command.startswith(":sendMessage".casefold()):
                message = command[len(":sendMessage"):].strip()
                response = server.send_message(message)
                print(response)

            elif command.startswith(":enableBot".casefold()):
                parts = command.split()
                if len(parts) != 3:
                    print("Uso incorrecto. Usa: :enableBot <bot_type> <player_id>")
                    continue
                bot_type = parts[1]
                player_id = int(parts[2])
                response = server.enable_bot(bot_type, player_id)
                print(response)

            elif command.startswith(":disableBot".casefold()):
                parts = command.split()
                if len(parts) != 3:
                    print("Uso incorrecto. Usa: :disableBot <bot_type> <player_id>")
                    continue
                bot_type = parts[1]
                player_id = int(parts[2])
                response = server.disable_bot(bot_type, player_id)
                print(response)

            elif command == ":getPlayers".casefold():
                players = server.get_players()
                print(f"Jugadores conectados: {players}")
            
            elif command == ":showBots".casefold():
                players = server.show_bots()
                print(f"Bots: {players}")

            elif command == ":exit".casefold():
                print("Saliendo del cliente...")
                break

            else:
                print("Comando no reconocido.")
        except Exception as e:
            print(f"Error al ejecutar el comando: {e}")

if __name__ == "__main__":
    server = connect_to_server()
    interact_with_server(server)