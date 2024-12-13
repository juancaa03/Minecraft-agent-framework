import Pyro4

# Conectar al servidor Pyro
def connect_to_server():
    # Dirección del servidor Pyro (debe coincidir con la URI del servidor)
    default_uri = "PYRO:obj_167b1c2b8aed444592458f49bf25bb64@localhost:50195"
    uri = input(f"Introduce la URI del servidor Pyro (predeterminado: {default_uri}): ") or default_uri
    try:
        server = Pyro4.Proxy(uri)  # Conectar al servidor Pyro
        print("Conexión exitosa al servidor.")
        return server
    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
        exit(1)

# Enviar comandos para controlar los bots
def interact_with_server(server):
    while True:
        print("\nComandos disponibles:")
        print(":sendMessage <message> - Enviar un mensaje al chat")
        print(":enableBot <bot_type> <player_id> - Activar un bot")
        print(":disableBot <player_id> - Desactivar un bot")
        print(":getPlayers - Obtener lista de jugadores conectados")
        print(":exit - Salir del cliente")

        command = input("Introduce un comando: ").strip()

        try:
            if command.startswith(":sendMessage"):
                message = command[len(":sendMessage"):].strip()
                response = server.send_message(message)
                print(response)

            elif command.startswith(":enableBot"):
                parts = command.split()
                if len(parts) != 3:
                    print("Uso incorrecto. Usa: :enableBot <bot_type> <player_id>")
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
        except Exception as e:
            print(f"Error al ejecutar el comando: {e}")

if __name__ == "__main__":
    server = connect_to_server()
    interact_with_server(server)