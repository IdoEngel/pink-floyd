import socket
import data
import hashlib  # to create hash system

HASH_PASSWORD = hashlib.sha256(b'Magsh1m!m#').hexdigest()  # create a hash password

LISTEN_PORT = 92
SERVER_IP = '127.0.0.1'
WELCOME_MSG = 'HI THERE MAN'
GOOD_BYE_MSG = 'Thank you for using the Pink-Floyd Server! Bye Bye!'
BASE_PROTOCOL = "%s|%s|%s"


def create_sock():
    """Create a server-side sock to connect with clients
    :param:
    :return: """

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_sock:
        # Binding to local port 9090
        server_address = (SERVER_IP, LISTEN_PORT)
        try:
            listening_sock.bind(server_address)
        except Exception as e:
            print(f"ERROR! -\n{e}")

        # Listen for incoming connections
        listening_sock.listen(1)
        print('Waiting for a connection...')

        # Create a new conversation socket
        client_soc, client_address = listening_sock.accept()
        print(f'connected with client port: {client_address[1]}')
        with client_soc:
            try:
                conversation_with_client(client_soc)
            except Exception as e:  # try to send to client error message
                client_soc.sendall((BASE_PROTOCOL % ('RES', 1, e)).encode())


def conversation_with_client(sock):
    """create the conversation with the client (send and resave data)
    :param sock: socket to send the server data
    :type sock: socket.socket
    :return:"""
    # create arr of funcs to access easily
    find_functions = [album_list, songs_in_list, song_len, song_lyrics,
                      find_song_album, find_song_name_base, find_song_lyrics_base]

    msg = sock.recv(1024).decode()
    if "CONNECT| | |" in msg:
        sock.sendall(F'RES|0|{WELCOME_MSG}'.encode())

    if login(sock):
        sock.sendall(b'RES|0|Correct Password')

    else:
        sock.sendall(b'RES|1|Incorrect Password!')

    while True:
        msg = sock.recv(1024).decode()
        msg_parts = msg.split('|')
        if int(msg_parts[1]) == 8:
            sock.sendall((BASE_PROTOCOL % ('RES', 0, GOOD_BYE_MSG)).encode())
            break  # break from the 'while true' loop
        # send a default message what tells the server can tell what is the request
        elif int(msg_parts[1]) in range(1, 8):
            # send a msg to client with answer of the right func from the array
            index = int(msg_parts[1]) - 1
            func_ans = find_functions[index](msg_parts[2]) if index != 0 else find_functions[index]()
            sock.sendall((BASE_PROTOCOL % ('RES', 1 if 'not existed' in func_ans else 0, func_ans)).encode())


def login(sock):
    """check if the password is the same
    :return: is the password the same?
    :rtype: bool"""
    a = sock.recv(2000).decode().split('|')[2]
    return a == HASH_PASSWORD


def album_list():
    """create a string of albums and return it to send to client
    :param:
    :return: string of albums
    :rtype: str """
    database = data.create_album_dict()
    return ', '.join(f'{key}' for key in database.keys())


def songs_in_list(info):
    """create of string of sings in given album, send error if not exist
    :param info: name of album
    :type info: str
    :return: songs in album or error
    :rtype: str """
    database = data.create_album_dict()
    try:
        return ', '.join(f'{song}' for song in database[info])
    except KeyError:
        return 'not existed album!'


def song_len(info):
    """create a string of the len of the song, send error if not exist
    :param info: name of song
    :type info: str
    :return: song len or error
    :rtype: str """
    database = data.create_song_list()
    try:
        return str(database[info][0])
    except KeyError:
        return 'not existed song!'


def song_lyrics(info):
    """create a string of lyrics of song, send error if not exist
    :param info: name of song
    :type info: str
    :return: song lyrics or error
    :rtype: str """
    database = data.create_song_list()
    try:
        return database[info][1]
    except KeyError:
        return 'not existed song!'


def find_song_album(info):
    """create a string of album of song, send error if not exist
        :param info: name of song
        :type info: str
        :return: song album or error
        :rtype: str """
    database = data.create_song_list()
    try:
        return database[info][2]
    except KeyError:
        return 'not existed song!'


def find_song_name_base(info):
    """create string of all songs that 'info' is in their name, send error if not existed
        :param info: word to search in names of all the songs
        :type info: str
        :return: song with 'info' inside of their name or error
        :rtype: str"""
    ans = list()
    database = data.create_song_list()
    for name in database.keys():
        if info.lower() in name.lower():
            ans.append(name)
    return 'not existed word!' if len(ans) == 0 else ', '.join(ans)


def find_song_lyrics_base(info):
    """create string of all songs that 'info' is in their lyrics, send error if not existed
    :param info: word to search in lyrics of all the songs
    :type info: str
    :return: song with 'info' inside of their lyrics or error
    :rtype: str"""
    ans = []
    database = data.create_song_list()
    for name in database.keys():
        if info.lower() in str(database[name][1]).lower():
            ans.append(name)
    return 'not existed word!' if len(ans) == 0 else ', '.join(ans)


def main():
    while True:
        try:
            create_sock()
        except Exception as e:  # if an error occur, return to main and start the program again
            print(f'Error!! -\n{e}\n')
            main()


if __name__ == "__main__":
    main()
