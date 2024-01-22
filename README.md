# About
The snake server can handle multiple clients/snakes simultaneously. Each client will have its
own snake, enabling a multiplayer environment where multiple snakes share the field.
Each client will receive a game state that includes the position of all snakes to display.
them. While playing, Clients can send a public message to the server to be broadcasted to all.
clients. Both the server and the clients encrypt their messages using RSA encryption algorithm.

# Files
snake_server.py: Snake game server-side code which can handle multiple client connections and public messaging. <br />
Snake.py: Helper file for snake_server.py. It contains the functions to handle the game logic. <br />
snake_client.py: Snake game client side <br />

# Usage
Run server file first, then connect to the server via the client.

Controls: <br />
Instead of having the user type in the message it wants to send to the server, each player has a set of predefined messages each associated with the assigned  hotkey of: [‘z’, ‘x’, ‘c’]. <br />
up: ‘w’ <br />
down: ‘s’ <br />
left: ‘a’ <br />
right: ‘d’ <br />
reset (reset the length of the snake and start from a random location) : ‘r’ <br />
quit: ‘q’ <br />
![Screenshot](https://github.com/Rbiern/Multi-player-server-client-snake-game/assets/156489385/3aff8440-8c68-47ec-bd73-f419878d87fc)
