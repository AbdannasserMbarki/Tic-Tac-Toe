import random
from game import X_O
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class graphX_O(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setGeometry(450,150,350,350)
        self.setWindowTitle("AI Tic-Tac-Toe: The Ultimate Challenge")
        self.setWindowIcon(QIcon("./images/icon.png"))
        self.game=X_O()
        self.AIturn= random.choice([True, False])
        if self.AIturn==False:
            self.label.setText("Human turn...")
        else : 
            self.label.setText("AI turn...")
            self.AiTurn()

    def initUi(self):
        '''create the graphical interface (button grid and lables)'''
        self.label=QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText("") #to access it from anywhere
        #create board
        self.buttons={}
        grid_layout=QGridLayout()
        for row in range(8):
            for col in range(8):
                button=QPushButton("",self)
                button.setFixedSize(30,30)
                button.clicked.connect(self.buttonClicked)
                grid_layout.addWidget(button,row,col)
                self.buttons[(row,col)]=button
        #display flex: col
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def buttonClicked(self):
        '''player turn(check for button clicked)'''
        if self.AIturn==False:
            sender=self.sender()
            for row in range(8):
                for col in range(8):
                    if sender == self.buttons[(row,col)]:
                        if self.game.board[row][col] == "-":
                            self.buttons[(row,col)].setText(self.game.human)
                            self.game.make_choice((row,col),self.game.human)
                            self.label.setText("AI turn...")
                            break
        if self.game.game_over():
            self.end_game()
        else: 
            self.AIturn=True
            self.AiTurn()


    def AiTurn(self):
        """Handle the AI's turn."""
        self.label.setText("AI turn...")
        # Check for forced moves first
        if not self.game.forced_moves():
            # If no forced move is found, use the best_move function
            bestMove, _ = self.game.best_move()
            self.game.make_choice(bestMove, self.game.ai)
            self.buttons[bestMove].setText(self.game.ai)
        else:
            # If a forced move was made, update the board
            for row in range(8):
                for col in range(8):
                    if self.game.board[row][col] == self.game.ai and self.buttons[(row, col)].text() == "":
                        self.buttons[(row, col)].setText(self.game.ai)
                        break

        self.AIturn = False
        self.label.setText("Human turn...")
        if self.game.game_over():
            self.end_game()



    def end_game(self):
        """Display the game result and reset the game."""
        result = self.game.game_over()
        if result == "draw":
            QMessageBox.information(self, "Game Over", "It's a draw!")
        elif result == self.game.human:
            QMessageBox.information(self, "Game Over", "You win!")
        elif result == self.game.ai:
            QMessageBox.information(self, "Game Over", "AI wins!")
        self.reset_game()

    def reset_game(self):
        """Reset the game board and clear the UI."""
        self.game.reset_board()
        for button in self.buttons.values():
            button.setText("")




def main():
    app = QApplication(sys.argv)
    window = graphX_O()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()





