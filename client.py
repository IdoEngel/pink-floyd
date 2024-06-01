import socket
import hashlib

SERVER_IP = '127.0.0.1'
SERVER_PORT = 92
WELCOME_MSG = b'CONNECT| | |'
OPTIONS_TO_PRINT = """1 Get Albums
2 Get Album Songs
3 Get song Length
4 Get Song Lyrics
5 Get song Album
6 Search Song By Name
7 Search Song By Lyrics
8 Quit"""
BASE_PROTOCOL = "%s|%s|%s"
DICT_CHOICE = {
    2: "Enter album name: ",
    3: "Enter song name: ",
    4: "Enter song name: ",
    5: "Enter song: ",
    6: "Enter text: ",
    7: "Enter text: ",
    8: ''
}
DICT_ANSWER = {
    1: "The albums list:",
    2: "The songs in the album:",
    3: "The song length:",
    4: "The song lyrics:",
    5: "The album with this song is:",
    6: "The list of songs:",
    7: "The list of songs:"
}


def create_sock():
    """Create a socket to connect to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = (SERVER_IP, SERVER_PORT)
        try:
            sock.connect(server_address)
        except Exception as e:
            print(f'ERROR! - {e}')
            return

        try:
            get_choice(sock)
        except ConnectionResetError:
            print('Connection closed by remote host!')
        except Exception as e:
            print(f'Error! - {e}')


def get_choice(sock):
    """Handle user choices and send requests to the server."""
    sock.sendall(WELCOME_MSG)
    print(f'Server says: {sock.recv(1024).decode().split("|")[2]}')

    if not login(sock):
        print('Incorrect password')
        return

    choice = 10  # Initialize choice with a non-menu value to enter the loop

    while choice != 8:  # Loop until user wants to exit
        additional_data = '<empty>'
        print(OPTIONS_TO_PRINT)

        while True:  # Loop until input value is valid
            try:
                choice = int(input("Enter number: "))

                if choice in range(1, 9):
                    break
                else:
                    print(f'enter the numbers 1 to 8!')

            except ValueError:
                print("Enter a number!!")

        if choice != 1 and choice != 8:
            try:
                additional_data = input(DICT_CHOICE.get(choice, "Invalid choice! Enter text: "))
            except Exception as e:
                print(f'ERROR! - {e}')

        sock.sendall((BASE_PROTOCOL % ('REQ', choice, additional_data)).encode())

        if choice != 8:
            print(DICT_ANSWER.get(choice, "Unknown choice!"))  # Print the operation result
        print((sock.recv(4000).decode()).split('|')[2] + '\n')  # Print server response


def login(sock):
    """Handle the login process with the server."""
    password = input('Please enter the password: ')
    current_hash = hashlib.sha256(password.encode()).hexdigest()
    sock.sendall((BASE_PROTOCOL % ('REQ', 0, current_hash)).encode())
    response = sock.recv(1024).decode()
    return 'Correct Password' in response


def main():
    create_sock()


if __name__ == "__main__":
    main()
