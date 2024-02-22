import socket
import chess
import os

class Client:
    def __init__(self):
        self.board = chess.Board()
    
    def get_piece_emojis(self):
        """
        Returns a dictionary mapping piece types to emojis.

        The dictionary is reversed if the client's color is black (to keep consistent perspective view between two players),
        so that their pieces are represented with white emojis and the white pieces are represented with black emojis.
        """
        piece_emoji_white = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            None: '.' 
        }
        piece_emoji_black = {
            'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙',
            'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
            None: '.' 
        }
        return piece_emoji_black if self.color == 'B' else piece_emoji_white


    def print_board(self):
        """
        Prints the chess board to the console.

        The board is printed with emojis representing the chess pieces. The view of the board is flipped for the black player,
        so that their pieces are at the bottom and the white pieces are at the top.

        The board is printed with column labels (a-h) at the top and row labels (1-8) at the left side. The order of the row
        labels is reversed for the black player, so that 8 is at the bottom and 1 is at the top.

        After the board is printed, it is flipped back to its original state if the view was flipped for the black player.
        """

        os.system('cls' if os.name == 'nt' else 'clear')
        piece_emoji = self.get_piece_emojis()
        print(f"You are {'Transparent - White' if self.color == 'W' else 'Solid - Black'}\n")    
        print('  a b c d e f g h')

        # Flip the board if the client's color is black
        if self.color == 'B':
            self.board = self.board.mirror()

        # Print each row with row label
        for i in range(7, -1, -1):
            # Print the correct row number based on the client's color
            row_number = 8 - i if self.color == 'B' else i + 1
            print(row_number, end=' ')
            for j in range(8):
                piece = self.board.piece_at(i * 8 + j)
                print(piece_emoji[str(piece) if piece else None], end=' ')
            print()

        # Flip the board back after printing it
        if self.color == 'B':
            self.board = self.board.mirror()


    def start(self, host = '127.0.0.1', port = 12345):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            # Receive and store color information
            self.color = s.recv(1024).decode()
            while not self.board.is_checkmate():
                try:
                    data = s.recv(1024)
                    if data:
                        data_decoded = data.decode()
                        print('Received', repr(data_decoded))
                        if data_decoded[0] == 'B':  # Check if the message is a board state
                            # Remove the 'B' prefix before setting the FEN
                            self.board.set_fen(data_decoded[1:])
                        self.print_board()
                        print('\n')
                        if self.color == ('W' if self.board.turn else 'B'):  # Check if it's this client's turn
                            move = input("Enter your move: ")
                            s.sendall(move.encode())
                        else:
                            print("Waiting for other player's move...")
                except socket.error:
                    print("Lost connection to server.")
                    break
if __name__ == "__main__":
    client = Client()
    client.start()