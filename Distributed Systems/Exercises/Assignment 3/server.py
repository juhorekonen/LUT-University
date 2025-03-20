# Server-side for Chat System for multiple clients
import socket
import threading

HOST = '0.0.0.0'
PORT = 8080

COMMANDS_LIST = """
Available commands:
/exit - Exit the chat
/leave <channel> - Leave a channel
/join <channel> - Join a channel
/private <nickname> <message> - Send a private message
/channels - List all available channels
/users - List all connected users
/commands - Show available commands
"""

# Dictionary to store the client's username and address
clients = {}

# Dictionary to keep track of the client's current channel
currentChannel = {}

# Dictionary to store channels and their clients
channels = {'general': set()}

# Function to broadcast message to all clients in the channel
def broadcast(message, channel, sender = None):
    for client in channels.get(channel, []):
        if client != sender:
            clients[client].sendall(f'[{channel}] {message}'.encode())

# Function to handle client's connection
def handleClient(client, address):
    print(f"New connection from {address}")
    client.sendall("Enter your username: ".encode())
    username = client.recv(1024).decode().strip()
    clients[username] = client
    client.sendall("You are now connected to the server".encode())
    client.sendall("To see the available commands, type '/commands'\n".encode())

    channels['general'].add(username)
    currentChannel[username] = 'general'
    broadcast(f"{username} has joined the general channel\n", 'general', username)

    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                continue
            
            if message.startswith('/private'):
                parts = message.split(' ', 2)
                if len(parts) < 3:
                    client.sendall("Usage: /private <nickname> <message>\n".encode())
                    continue
                elif parts[1] in clients:
                    clients[parts[1]].sendall(f'[Private from {username}]: {parts[2]}\n'.encode())
                else:
                    client.sendall(f'User {parts[1]} not found\n'.encode())
            
            elif message.startswith('/join'):
                parts = message.split(' ', 1)
                if len(parts) < 2:
                    client.sendall("Usage: /join <channel>\n".encode())
                    continue
                else:
                    channelName = parts[1]
                    if channelName not in channels:
                        channels[channelName] = set()
                    channels[channelName].add(username)
                    currentChannel[username] = channelName
                    # print(f'You are here: {currentChannel[username]}')
                    client.sendall(f"Joined channel {channelName}\n".encode())
                    broadcast(f"{username} has joined the channel {channelName}\n", channelName, username)
            
            elif message.startswith('/leave'):
                parts = message.split(' ', 1)
                if len(parts) < 2:
                    client.sendall("Usage: /leave <channel>\n".encode())
                    continue
                else:
                    channelName = parts[1]
                    if channelName in channels:
                        channels[channelName].discard(username)
                        currentChannel[username] = None
                        client.sendall(f"You left the channel {channelName}\n".encode())
                        broadcast(f"{username} has left the channel\n", channelName, username)
            
            # Else if the message is /channels, list all the channels where the user is present
            elif message.startswith('/channels'):
                client.sendall(f"Channels: {', '.join(channels.keys())}\n".encode())

            elif message.startswith('/users'):
                client.sendall(f"Connected users: {', '.join(clients.keys())}\n".encode())
            
            elif message.startswith('/commands'):
                client.sendall(f"{COMMANDS_LIST}".encode())
            
            elif message.startswith('/exit'):
                client.sendall("Exiting channel\n".encode())
                break
            
            else:
                broadcast(f"{username}: {message}", currentChannel[username], username)
        except Exception as e:
            print(f"Error occurred with {username}: {e}")
            break

    client.close()
    del clients[username]
    currentChannel.pop(username, None)
    for channel in channels.values():
        channel.discard(username)
    print(f'{username} disconnected')

# Main function to start the server
def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started on {HOST}:{PORT}")
    except Exception as e:
        print(f"Error occurred while starting the server: {e}")
        return

    while True:
        client, address = server.accept()
        print(f"Connection from {address}")
        newThread = threading.Thread(target=handleClient, args=(client, address), daemon=True)
        newThread.start()

if __name__ == '__main__':
    main()

