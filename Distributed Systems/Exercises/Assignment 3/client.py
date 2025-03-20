# Client-side for Chat System for multiple clients
import socket
import threading

SERVER_IP = '127.0.0.1'
PORT = 8080

# Function to receive messages from the server
def receiveMessages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            # If no message was sent (= message is empty), break from the loop
            if not message:
                break
            print(message)

        except ConnectionResetError:
            print('Server has closed the connection')
            break

        # If the user types '/exit', close the client
        except OSError:
            print('Client has closed the connection')
            break

        except Exception as e:
            print(f'Error occurred while receiving messages: {e}')
            break
    client.close()


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    try:
        client.connect((SERVER_IP, PORT))
    except:
        print("Unable to connect to the server")
        return

    newThread = threading.Thread(target=receiveMessages, args=(client,))
    newThread.start()

    print('Welcome to the chat system!')

    try:
        while True:
            message = input().strip()

            if not isinstance(message, str):
                print('Please enter the message in string format')
                continue
            
            # If the message is '/exit', close the client
            if message == '/exit':
                client.sendall(message.encode())
                break
            client.sendall(message.encode())
    
    except KeyboardInterrupt as e:
        print('User has exited the chat system with Ctrl + C')
        client.close()

    client.close()

if __name__ == '__main__':
    main()
