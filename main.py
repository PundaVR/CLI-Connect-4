import os # May need to delete this and the code using it if using something like replit.com

# Board size
xSize = 7 # default: 7
ySize = 6 # default: 6

# Player cells
ply1 = "[X]" # default: "[X]"
ply2 = "[O]" # default: "[O]"

# Holds which player turn
global turn 
turn = ply1

# Board variable, change tiles with: board[y][x] = "[ ]"
global board
board = [['[ ]' for i in range(xSize)] for j in range(ySize)]

global gameInProgress # Is the game in progress?

# Reset the Board
def ResetBoard():
    global board
    board = [['[ ]' for i in range(xSize)] for j in range(ySize)]
    global turn
    turn = ply1

# Print the label along the X axis
def PrintAxisX():
    axisX = ([f'[{i}]' for i in range(xSize)])
    axisLine = ""
    for line in axisX:
        axisLine = axisLine + line
    print(axisLine)

# Print the board
def PrintBoard():
    PrintAxisX()
    for line in board:
        newLine = ""
        for item in line:
            newLine = newLine+item
        print(newLine)

# Gravity for the Y axis when placing a tile, returns the lowest empty cell on the Y axis.
def CheckAxisY(x):
    for y in range((ySize-1), -1, -1):
        if board[y][x] == "[ ]":
            return y
            
# Place a token at X spot
def Place(x, ply):
    y = CheckAxisY(x) # Get the lowest empty cell on the Y axis 
    board[y][x] = ply # Place token
    CheckConnect4(x, y, ply) # Check if Connect4

# Get the player's next move
def GetMove():
    plyInput = input("Enter move (in XY i.e. 4)") 
    while (len(plyInput) != 1 or plyInput.isnumeric() is False): # filter invalid inputs
        plyInput = input("Enter move (in XY i.e. 4)") 
    return int(plyInput[0])

# Begin a new move
def Move():
    global turn
    PrintBoard()
    move = GetMove()
    while (move < 0 or move > 6 or board[0][move] != "[ ]"):
        move = GetMove()
    print(move)
    if(turn == ply1):
        Place(move, ply1)
        turn = ply2
    elif(turn == ply2):
        Place(move, ply2)
        turn = ply1

# Get the Cell at X,Y position
def GetCell(x, y):
    return board[y][x]

# Check surrounding cells, part of checking Connect4
def CheckSurrounding(x,y, ply):
    # return array containing:
    # 0 - Position (L = left, U = up, DR = diagonal down-right)
    # 1 - xPos
    # 2 - yPos
    cells = []
    # check left
    if(x-1 >= 0):
        if(GetCell(x-1,y) == ply):
            cells.append(["L",x-1,y])

    # check right
    if(x+1 <= xSize-1):
        if(GetCell(x+1,y) == ply):
            cells.append(["R", x+1,y])
    # check up
    if(y-1 >= 0):
        if(GetCell(x,y-1) == ply):
            cells.append(["U", x,y-1])

    # check down
    if(y+1 <= ySize-1):
        if(GetCell(x,y+1) == ply):
            cells.append(["D", x,y+1])

    # check diagonal-left-up
    if(x-1 >= 0 and y-1 >= 0):
        if(GetCell(x-1,y-1) == ply):
            cells.append(["UL",x-1,y-1])

    # check diagonal-right-up
    if(x+1 <= xSize-1 and y-1 >= 0):
        if(GetCell(x+1,y-1) == ply):
            cells.append(["UR",x+1,y-1])

    # check diagonal-left-down
    if(x-1 >= 0 and y+1 <= ySize-1):
        if(GetCell(x-1,y+1) == ply):
            cells.append(["DL",x-1,y+1])

    # check diagonal-right-down
    if(x+1 <= xSize-1 and y+1 <= ySize-1):
        if(GetCell(x+1,y+1) == ply):
            cells.append(["DR",x+1,y+1])
    return cells

# Check if the last placed token at (x,y) is a connect 4
def CheckConnect4(x, y, ply):
    # Check the surrounding cells of the last-placed cell, if surrounding cell(s) belongs to ply
    # then follow the path until "connect4" = 4 or cell != ply
    global gameInProgress
    direction = ""
    for cell in CheckSurrounding(x,y,ply): 
        # Poorly coded? Maybe. Does it work? Yes.
        cellIsPly = True
        direction = cell[0]
        connect4 = 2 # starts at 2 because if there is a surrounding cell, thats already 2 cells in a row.
        while cellIsPly: # While the cell is the player's cell
            for newCell in CheckSurrounding(cell[1],cell[2],ply): # for cell in surrounding cells
                if (newCell[0] == direction):
                    connect4 = connect4+1
                    for lastCell in CheckSurrounding(newCell[1],newCell[2],ply): # for cell in new cell's surrounding cells 
                        if (lastCell[0] == direction):
                            connect4 = connect4+1
                        else: cellIsPly = False # cell is not player's cell
                else: cellIsPly = False # cell is not player's cell
        if(connect4 == 4): # if connect 4
            gameInProgress = False
            os.system('cls')
            PrintBoard()
            print(f"=== {ply} Wins! ===")
            
# Game Loop
def Game():
    global gameInProgress
    while(gameInProgress):
        os.system('cls')
        Move()
    
    # Below code occurs when the game ends (someone found connect 4)
    plyInput = input("\nDo you want to play again? y/n:\n")
    while (plyInput.lower() != 'y' and plyInput.lower() != 'n'):
        plyInput = input("\nDo you want to play again? y/n:\n")
    if (plyInput == "y"):
        gameInProgress = True
        ResetBoard()
        Game()

# Very start of the program
plyInput = input("Are you ready to start? y/n:\n")
while (plyInput.lower() != 'y' and plyInput.lower() != 'n'):
    plyInput = input("Are you ready to start? y/n:\n")
if("y" in plyInput):
    ResetBoard()
    PrintBoard()
    gameInProgress = True
    Game()
    