FILE_PATH = 'Pink_Floyd_DB.txt'


def create_album_dict():
    """Creates a data structure with dicts
        (key - name of album, value - list of songs)
    :param:
    :return: album_list
    :rtype: dict """
    album_list = dict()

    index_list = -1  # start form -1 so the indexes in the loop will be correct
    name_of_album = ''
    list_of_albums_name = []

    with open(FILE_PATH, "r") as file:
        lines = file.readlines()
        for line in lines:
            # create dict of album
            if '#' in line:
                index_list += 1
                name_of_album = line[1:-7]  # always will have '::' and 4 chars year before and of line
                list_of_albums_name.append(name_of_album)

                album_list[name_of_album] = []  # create new key in dict

            if '*' in line:
                split_line = line.split('::')
                album_list[name_of_album].append(split_line[0][1:])

    # term into tuple data types
    for i in range(len(album_list)):
        album_list[list_of_albums_name[i]] = tuple(album_list[list_of_albums_name[i]])

    return album_list


def create_song_list():
    """Create list of dict -
        each dict - {key = name of song: value = list(len, lyrics, album)}
    :param:
    :return: song_list
    :rtype: dict"""
    song_list = dict()

    index_list = -1  # start form -1 so the indexes in the loop will be correct
    list_of_songs_name = []
    album_name = ''

    with open(FILE_PATH, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if '#' in line:
                album_name = line[1:-7]  # always will have '::' and 4 chars year before and of line

            if '*' in line:
                index_list += 1

                split_line = line.split('::')
                name_of_song = split_line[0][1:]
                list_of_songs_name.append(name_of_song)

                song_list[name_of_song] = []  # create new key in dict
                # add len, lyrics and album
                song_list[name_of_song].append(split_line[2])
                song_list[name_of_song].append(get_lyrics(index, lines))
                song_list[name_of_song].append(album_name)
    # tern into tuple
    for i in range(len(song_list)):
        song_list[list_of_songs_name[i]] = tuple(song_list[list_of_songs_name[i]])

    return song_list


def get_lyrics(index, lines):
    """create string of all the lyrics of the song that starts in the given index & return it
    :param index: the index of the song in 'lines'
    :type index: int
    :param lines: list of all the lines in the file
    :type lines: list
    :return: lyrics
    :rtype: str"""
    lyrics = lines[index].split('::')[3]

    for line in lines[index + 1:]:
        if ('*' not in line) and ('#' not in line):
            lyrics += line
        else:
            return lyrics
