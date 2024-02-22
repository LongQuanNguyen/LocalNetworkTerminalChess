# Chess Game

This project is a simple chess game that can be played between two players over a network, inside terminal. The game is implemented in Python using the `socket` and `chess` libraries.

## Requirements

- Python 3.6 or higher
- `chess` library

You can install the `chess` library using pip:

```bash
pip install python-chess
```

## Running the Game

To run the game, you need to start the server and then start two clients.

### Starting the Server

You can start the server by running the `server.py` script:

```bash
python server.py
```

By default, the server listens on `127.0.0.1:12345`.

### Starting the Clients

You can start a client by running the `client.py` script:

```bash
python client.py
```

By default, the client connects to `127.0.0.1:12345`.

When a client is started, it receives its color (white or black) from the server. The client then enters a loop where it receives the board state from the server, prints the board, and prompts the user for a move if it's their turn.

## Gameplay

The game is played in the standard way. Players enter their moves in the UCI (Universal Chess Interface) format. For example, to move a pawn from e2 to e4, you would enter `e2e4`.

The game continues until a checkmate occurs.

## Troubleshooting

If you encounter any problems while running the game, please check your network connection and make sure that the server and clients are running on the same network and that the correct host and port are being used.
