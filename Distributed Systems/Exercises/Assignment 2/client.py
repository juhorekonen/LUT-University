# Client-side for an RPC system
import xmlrpc.client

# Main function to interact with the server using a while loop
# The user can add notes, retrieve notes, or exit the program
def main():
    # Try to connect to the server
    # If the server is not running, an error message will be displayed
    try:
        server = xmlrpc.client.ServerProxy('http://localhost:8000')
    except:
        print('Error: Could not connect to server')
        return

    print('Welcome to the note-taking system!')

    while True:
        print('\nChoose an option:')
        print('1. Add note')
        print('2. Get notes')
        print('3. Fetch topics from Wikipedia')
        print('0. Exit')

        choice = input('Enter choice: ')

        if choice == '1':
            topic = input('Enter topic: ').strip()
            text = input('Enter text: ').strip()
            timestamp = input('Enter timestamp: ').strip()

            if not topic or not text or not timestamp:
                print('Please enter all fields')
                continue

            # Call the addNote function on the server
            try:
                response = server.addNote(topic, text, timestamp)
                print(response)
            except Exception as e:
                print(f'Error occurred while creating a note: {e}')

        elif choice == '2':
            topic = input('Enter topic: ').strip()
            if not topic:
                print('Topic cannot be empty')
                continue

            # Call the getNotes function on the server
            try:
                notes = server.getNotes(topic)
            except Exception as e:
                print(f'Error occurred while retrieving notes: {e}')
                continue

            if type(notes) == str:
                print(notes)
            else:
                for note in notes:
                    print(note)
        
        elif choice == '3':
            topic = input('Enter topic to search Wikipedia: ').strip()
            if not topic:
                print('Topic cannot be empty')
                continue
            try:
                response = server.fetchWikipedia(topic)
                print(response)
            except Exception as e:
                print(f'Error occurred while fetching topics from Wikipedia: {e}')
            
        elif choice == '0':
            print('Exiting...')
            break

        # Otherwise, the chosen option is invalid
        else:
            print('Invalid option')

if __name__ == '__main__':
    main()
