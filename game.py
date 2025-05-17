import random

class X_O ():
    def __init__(self):
        self.board=[["-","-","-","-","-","-","-","-"],#0
                    ["-","-","-","-","-","-","-","-"],#1
                    ["-","-","-","-","-","-","-","-"],#2
                    ["-","-","-","-","-","-","-","-"],#3
                    ["-","-","-","-","-","-","-","-"],#4
                    ["-","-","-","-","-","-","-","-"],#5
                    ["-","-","-","-","-","-","-","-"],#6
                    ["-","-","-","-","-","-","-","-"],#7
                    ]
        self.human="X"
        self.ai="O"
        self.history = []



    def print_board(self):
        '''printing each row of the matrix'''
        for i in range(8):
            print(self.board[i])


    def reset_board(self):
        '''resetting the board to it's initial state'''
        self.board=[["-","-","-","-","-","-","-","-"],#0
                    ["-","-","-","-","-","-","-","-"],#1
                    ["-","-","-","-","-","-","-","-"],#2
                    ["-","-","-","-","-","-","-","-"],#3
                    ["-","-","-","-","-","-","-","-"],#4
                    ["-","-","-","-","-","-","-","-"],#5
                    ["-","-","-","-","-","-","-","-"],#6
                    ["-","-","-","-","-","-","-","-"],#7
                    ]


    def avaible_moves(self):
        '''will be replaces by condidateMoves
            checks for all legal moves'''
        moves=[]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == "-":
                    moves.append((i,j))
        return moves




    def make_choice(self,position,player):
        '''make the moves (it does not check if it is available!)'''
        if self.board[position[0]][position[1]] == "-":
            self.board[position[0]][position[1]]= player



    def winner_check(self, player):
        """Checks if there are 4 consecutive marks for the given player."""
        # Define directions: right, down, down-right, down-left
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == player:
                    for dx, dy in directions:
                        count = 1
                        for k in range(1, 4):
                            x = i + dx * k
                            y = j + dy * k
                            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == player:
                                count += 1
                            else:
                                break
                        if count == 4:
                            return True
        return False



    def board_is_full(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j]=="-":
                    return False
        return True



    def game_over(self):
        '''checks if the game is over'''
        if self.board_is_full() :
            return "draw"
        if self.winner_check(self.human):
            return self.human
        if self.winner_check(self.ai):
            return self.ai
        return None


    def evaluate_board(self):
        """A refined heuristic evaluation.
        Uses a weighted board that favors central positions and adjusts the score
        based on potential 3-in-a-row opportunities for both AI and Human."""
        weights = [
            [0.0003, 0.0003, 0.0003, 0.0005, 0.0005, 0.0003, 0.0003, 0.0003],
            [0.0003, 0.0003, 0.0003, 0.0005, 0.0005, 0.0003, 0.0003, 0.0003],
            [0.0003, 0.0003, 0.0003, 0.0005, 0.0005, 0.0003, 0.0003, 0.0003],
            [0.0005, 0.0005, 0.0005, 0.0008, 0.0008, 0.0005, 0.0005, 0.0005],
            [0.0005, 0.0005, 0.0005, 0.0008, 0.0008, 0.0005, 0.0005, 0.0005],
            [0.0003, 0.0003, 0.0003, 0.0005, 0.0005, 0.0003, 0.0003, 0.0003],
            [0.0003, 0.0003, 0.0003, 0.0005, 0.0005, 0.0003, 0.0003, 0.0003],
            [0.0003, 0.0003, 0.0003, 0.0005, 0.0005, 0.0003, 0.0003, 0.0003]
        ]
        directions = [
            (0, 1),  # Right
            (1, 0),  # Down
            (1, 1),  # Diagonal Down-Right
            (1, -1)  # Diagonal Down-Left
        ]

        score = 0

        # Base score from weights
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.ai:
                    score += weights[i][j]
                elif self.board[i][j] == self.human:
                    score -= weights[i][j]

        # Additional score for 3-in-a-row opportunities
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != "-":
                    continue
                for dx, dy in directions:
                    ai_count = 0
                    human_count = 0
                    for k in range(1, 4):
                        x, y = i + dx * k, j + dy * k
                        if 0 <= x < 8 and 0 <= y < 8:
                            if self.board[x][y] == self.ai:
                                ai_count += 1
                            elif self.board[x][y] == self.human:
                                human_count += 1
                    if ai_count == 2 and human_count == 0:
                        score += 10  # Favor AI forming 3 in a row
                    elif human_count == 2 and ai_count == 0:
                        score -= 10  # Penalize human forming 3 in a row
        return score

    def forced_moves(self):
        """Check for forced moves: make a winning move for AI or block the opponent's winning move."""
        directions = [
            (0, 1),  # Right
            (0, -1),  # Left
            (1, 0),  # Down
            (-1, 0),  # Up
            (1, 1),  # Diagonal Down-Right
            (-1, -1),  # Diagonal Up-Left
            (1, -1),  # Diagonal Down-Left
            (-1, 1)  # Diagonal Up-Right
        ]

        # Check for forced moves for both AI and Human
        for player in [self.ai, self.human]:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == player:
                        for dx, dy in directions:
                            count = 1
                            empty_cell = None
                            for k in range(1, 4):
                                x, y = i + dx * k, j + dy * k
                                if 0 <= x < 8 and 0 <= y < 8:
                                    if self.board[x][y] == player:
                                        count += 1
                                    elif self.board[x][y] == "-":
                                        if empty_cell is None:  # Track the first empty cell
                                            empty_cell = (x, y)
                                        else:
                                            break  # More than one empty cell, not a forced move
                                else:
                                    break
                            if count == 3 and empty_cell is not None:
                                if player == self.ai:
                                    # AI can win, make the move
                                    self.make_choice(empty_cell, self.ai)
                                    return True
                                elif player == self.human:
                                    # Block the opponent's winning move
                                    self.make_choice(empty_cell, self.ai)
                                    return True
        return False



    def candidate_moves(self):
        """Generate candidate moves within a 3x3 grid around each occupied cell."""
        moves = set()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != "-":  # If the cell is occupied
                    for di in range(-1, 2):  # Check the 3x3 grid around the cell
                        for dj in range(-1, 2):
                            ni, nj = i + di, j + dj
                            if 0 <= ni < 8 and 0 <= nj < 8 and self.board[ni][nj] == "-":
                                moves.add((ni, nj))  # Add empty cells to the candidate moves
        if not moves:
            # If no moves are found (e.g., the board is empty), return all available moves
            return self.avaible_moves()
        return list(moves)



    def minimax(self,depth, isMaximizingPlayer, alpha=float('-inf'), beta=float('inf')):
        k=self.game_over()
        if k==self.ai:
            return +30
        if k==self.human:
            return -30
        if k=="draw":
            return 0
        if depth==0:
            return self.evaluate_board()
        
        #self.print_board()
        #print("____________________________________________________________________")
        if isMaximizingPlayer:
            best_score=float('-inf')
            candidate = self.candidate_moves()
            for movei,movej in candidate:
                self.make_choice((movei,movej),self.ai)
                score=self.minimax(depth-1, False, alpha, beta)
                self.board[movei][movej]="-"
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  
            return best_score
        else :
            best_score=float('inf')
            candidate = self.candidate_moves()
            for movei,movej in candidate:
                self.make_choice((movei,movej),self.human)
                score=self.minimax(depth-1,True , alpha,beta)
                self.board[movei][movej]="-"
                best_score=min(best_score,score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  
            return best_score 



    def best_move(self):
        best_score=float('-inf')
        candidate = self.candidate_moves() 
        for movei,movej in candidate:
            self.make_choice((movei,movej),self.ai)
            score=self.minimax(4, False)
            self.board[movei][movej]="-"
            if score > best_score:
                best_score=score
                best_move=(movei,movej)
        return best_move, best_score



    def play_game(self):
        while True:
            print("Welcome to Tic Tac Toe!")
            print("You are 'O' and the AI is 'X'")
            print("Enter positions (0-63) as shown below:")
            self.reset_board()
            self.print_board()
            ai_turn = random.choice([True, False])
            while not (self.game_over()==self.human or self.game_over()==self.ai or self.game_over()=='draw'):
                self.print_board()
                if ai_turn:
                    print("AI turn...")
                    print("making a move...")
                    best_move,best_score=self.best_move()
                    self.make_choice(best_move,self.ai)
                else:
                    while True:
                        try:
                            print("Your turn...")
                            avaible=self.avaible_moves()
                            move = int(input("Waiting for your move...    "))
                            if move in avaible:
                                break
                            else:
                                print("Invalid move! Try again.")
                        except ValueError:
                            print("Please enter a number between 0 and 63!")
                    self.make_choice(move,self.human)
                ai_turn=not ai_turn
            print("_________________________________________________")
            self.print_board()
            if self.game_over() == "draw":
                print("No one wins!")
            elif self.game_over()== self.human:
                print("\nYou wins!")
            else:
                print("\nAI wins!")
            break





def main():
    game=X_O()
    game.print_board()


if __name__=="__main__":
    main()