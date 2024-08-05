from tkinter import *
import random

def start_game():
    global root, buttons, board, turn, game_end, mode, difficulty, button_text_color
    root = Tk()
    root.geometry("720x720")
    root.title("Tic Tac Toe")
    root.resizable(0, 0)

    frame1 = Frame(root)
    frame1.pack()
    titleLabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 26), bg="darkblue", fg="white", width=16)
    titleLabel.grid(row=0, column=0)

    optionFrame = Frame(root, bg="#e6e6e6")
    optionFrame.pack()

    frame2 = Frame(root, bg="#CCCCCC")
    frame2.pack()

    board = {1: " ", 2: " ", 3: " ",
             4: " ", 5: " ", 6: " ",
             7: " ", 8: " ", 9: " "}

    turn = "x"
    game_end = False
    mode = "singlePlayer"
    difficulty = "easy"

    # Button Text Color
    button_text_color = "navy"

    def changeModeToSinglePlayer():
        global mode
        mode = "singlePlayer"
        singlePlayerButton["bg"] = "lightgreen"
        multiPlayerButton["bg"] = "lightgrey"

    def changeModeToMultiplayer():
        global mode
        mode = "multiPlayer"
        multiPlayerButton["bg"] = "lightgreen"
        singlePlayerButton["bg"] = "lightgrey"

    def changeDifficultyEasy():
        global difficulty
        difficulty = "easy"
        easyButton["bg"] = "lightgreen"
        midButton["bg"] = "lightgrey"
        hardButton["bg"] = "lightgrey"

    def changeDifficultyMid():
        global difficulty
        difficulty = "mid"
        easyButton["bg"] = "lightgrey"
        midButton["bg"] = "lightgreen"
        hardButton["bg"] = "lightgrey"

    def changeDifficultyHard():
        global difficulty
        difficulty = "hard"
        easyButton["bg"] = "lightgrey"
        midButton["bg"] = "lightgrey"
        hardButton["bg"] = "lightgreen"

    def updateBoard():
        for key in board.keys():
            buttons[key - 1]["text"] = board[key]

    def checkForWin(player):
        winning_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                return combo
        return None

    def mark_position(board, symbol):
        winning_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]
        ]
        for combo in winning_combinations:
            symbol_count = sum(board[pos] == symbol for pos in combo)
            empty_positions = [pos for pos in combo if board[pos] == " "]
            if symbol_count == 2 and len(empty_positions) == 1:
                board[empty_positions[0]] = symbol
                return True
        opponent_symbol = "x" if symbol == "o" else "o"
        for combo in winning_combinations:
            opponent_count = sum(board[pos] == opponent_symbol for pos in combo)
            empty_positions = [pos for pos in combo if board[pos] == " "]
            if opponent_count == 2 and len(empty_positions) == 1:
                board[empty_positions[0]] = symbol
                return True
        empty_positions = [key for key, value in board.items() if value == " "]
        if empty_positions:
            random_position = random.choice(empty_positions)
            board[random_position] = symbol
            return True
        return False

    def checkForDraw():
        for i in board.keys():
            if board[i] == " ":
                return False
        return True

    def restartGame():
        global game_end
        game_end = False
        for button in buttons:
            button["text"] = " "
            button["bg"] = "lightyellow"
        for i in board.keys():
            board[i] = " "
        titleLabel.config(text="Tic Tac Toe", bg="darkblue")

    def minimax(board, isMaximizing):
        if checkForWin("o"):
            return 1, None
        if checkForWin("x"):
            return -1, None
        if checkForDraw():
            return 0, None

        if isMaximizing:
            bestScore = -100
            bestMove = None
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "o"
                    score, _ = minimax(board, False)
                    board[key] = " "
                    if score > bestScore:
                        bestScore = score
                        bestMove = key
            return bestScore, bestMove
        else:
            bestScore = 100
            bestMove = None
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "x"
                    score, _ = minimax(board, True)
                    board[key] = " "
                    if score < bestScore:
                        bestScore = score
                        bestMove = key
            return bestScore, bestMove

    def level_easy(board):
        key = random.choice([k for k, v in board.items() if v == " "])
        board[key] = "o"

    def level_mid(board):
        mark_position(board, "o")

    def level_hard(board):
        _, bestMove = minimax(board, True)
        if bestMove is not None:
            board[bestMove] = "o"

    def playComputer():
        if mode == "singlePlayer":
            if difficulty == "easy":
                level_easy(board)
            elif difficulty == "mid":
                level_mid(board)
            elif difficulty == "hard":
                level_hard(board)
        updateBoard()
        winner_combo = checkForWin("o")
        if winner_combo:
            highlightWinner(winner_combo)
            titleLabel.config(text="o wins the game", bg="orange")
            global game_end
            game_end = True
        elif checkForDraw():
            titleLabel.config(text="Game Draw", bg="orange")
            game_end = True

    def highlightWinner(combo):
        for pos in combo:
            buttons[pos - 1]["bg"] = "lightgreen"

    def play(event):
        global turn, game_end
        if game_end:
            return

        button = event.widget
        index = buttons.index(button) + 1

        if button["text"] == " " and board[index] == " ":
            board[index] = turn
            updateBoard()
            winner_combo = checkForWin(turn)
            if winner_combo:
                highlightWinner(winner_combo)
                titleLabel.config(text=f"{turn} wins the game", bg="orange")
                game_end = True
                return

            if checkForDraw():
                titleLabel.config(text="Game Draw", bg="orange")
                game_end = True
                return

            turn = "o" if turn == "x" else "x"

            if mode == "singlePlayer" and turn == "o":
                playComputer()
                turn = "x"

    def hint(board):
        _, bestMove = minimax(board, False)
        if bestMove is not None:
            buttons[bestMove - 1]["bg"] = "lightblue"  # Highlight the best move

    # UI setup
    singlePlayerButton = Button(optionFrame, text="SinglePlayer", width=13, height=1, font=("Arial", 15), bg="yellow", fg=button_text_color, relief=RAISED, borderwidth=5, command=changeModeToSinglePlayer)
    singlePlayerButton.grid(row=0, column=0, columnspan=1, sticky=NW)

    multiPlayerButton = Button(optionFrame, text="Multiplayer", width=13, height=1, font=("Arial", 15), bg="yellow", fg=button_text_color, relief=RAISED, borderwidth=5, command=changeModeToMultiplayer)
    multiPlayerButton.grid(row=0, column=2, columnspan=1, sticky=E)

    easyButton = Button(optionFrame, text="Easy", width=6, height=1, font=("Arial", 15), bg="yellow", fg=button_text_color, relief=RAISED, borderwidth=5, command=changeDifficultyEasy)
    easyButton.grid(row=1, column=0, columnspan=1, sticky=NW)

    midButton = Button(optionFrame, text="Mid", width=6, height=1, font=("Arial", 15), bg="yellow", fg=button_text_color, relief=RAISED, borderwidth=5, command=changeDifficultyMid)
    midButton.grid(row=1, column=1, columnspan=1, sticky=N)

    hardButton = Button(optionFrame, text="Hard", width=6, height=1, font=("Arial", 15), bg="yellow", fg=button_text_color, relief=RAISED, borderwidth=5, command=changeDifficultyHard)
    hardButton.grid(row=1, column=2, columnspan=1, sticky=E)

    hintButton = Button(optionFrame, text="Hint", width=10, height=1, font=("Arial", 15), bg="yellow", fg=button_text_color, relief=RAISED, borderwidth=5, command=lambda: hint(board))
    hintButton.grid(row=2, column=1, columnspan=1, sticky=NW)

    buttons = []
    for i in range(3):
        for j in range(3):
            button = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30), bg="yellow", fg=button_text_color, relief=RAISED, borderwidth=5)
            button.grid(row=i, column=j)
            button.bind("<Button-1>", play)
            buttons.append(button)

    restartButton = Button(frame2, text="Restart Game", width=19, height=1, font=("Arial", 20), bg="white", fg=button_text_color, relief=RAISED, borderwidth=5, command=restartGame)
    restartButton.grid(row=4, column=0, columnspan=3)

    root.mainloop()

# Only run the game if this file is executed directly
if __name__ == "__main__":
    start_game()
