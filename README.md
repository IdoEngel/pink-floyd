# pink-floyd
A file management &amp; data organization project in Python

using 'sockets' module, I creata a "server" that can file real data of the musical composition pink floyd.
I used 3 defferent files for this

## Server file
The file that create the comunication with the clients, manage the connection, and make sure that the data will gat to the server.
Using 'sockets' I was able to do it in a simple and readable way.
The server side detting pythonic data types and find the answer from the user.
The server side wont collapse because, and will always listen to new clients.

## Data file
Using file name 'Pink_Floyd_DB.txt' that in the same folder with the data file, the data file create 2 defferent data types.
Using dicts I was able to find all the data I need in the Server.py with simple steps.
Each data type is for defferent type of questions, I created two to be able to find the answer easaly

## Client file
the client file create the communication with the server via 'sockets' module.
It gets the request from the user, build the it in the protocol I created & send the protocol the the server.
The Client file make sure the server gets only valid requests.
