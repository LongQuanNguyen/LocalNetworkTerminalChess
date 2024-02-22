import socket
import chess
import threading
from game import ChessGame


class Server:
    def __init__(self, game):
        self.game = game
        self.connections = []

    def start(self, host = '127.0.0.1', port = 12345):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print("Waiting for connections...")
            while len(self.connections) < 2:
                conn, addr = s.accept()
                print(f"Connected by {addr}")
                self.connections.append(conn)
                # Assign color to client
                color = 'W' if len(self.connections) == 1 else 'B'
                conn.sendall(color.encode())
            print("Two clients connected. Starting game...")
            # Send initial board state to clients
            for c in self.connections:
                c.sendall(self.game.board.fen().encode())
            self.game_loop()

    def game_loop(self):
        """
        Main game loop for the server. It receives moves from each client, validates them, 
        applies them to the game board, and sends the updated board state to all clients.
        """
        while True:
            for conn in self.connections:
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        move = chess.Move.from_uci(data.decode())
                        if move in self.game.board.legal_moves:
                            self.game.board.push(move)
                            break
                        else:
                            conn.sendall('Invalid move.'.encode())
                            continue
                    except (ValueError, socket.error):
                        conn.sendall('Invalid input.'.encode())
                        continue
                for c in self.connections:
                    c.sendall(('B' + self.game.board.fen()).encode())

if __name__ == "__main__":
    game = ChessGame()
    server = Server(game)

    threading.Thread(target=server.start).start()