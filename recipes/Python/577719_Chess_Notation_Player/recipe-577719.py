# Chess Game


board = ["r", "n", "b", "q", "k", "b", "n", "r", "x", "x", "x", "x", "x", "x", "x", "x", " ", " ",
         " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
         " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "X", "X", "X", "X", "X", "X",
         "X", "X", "R", "N", "B", "Q", "K", "B", "N", "R"]

# Black and White squares will be useful when checking bishop moves
blackSquares = [0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,
                52,54,57,59,61,63]
whiteSquares = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,
                53,55,56,58,60,62]
# 0 for white and 1 for black
player = 0
destination = 0
origin = 0
movingPiece = ""


def introScreen():
    print("Hello, welcome to the Chess Notation Viewer")
    print("This allows you to view every stage of a notated chess")
    print("match as it would appear on the board.")
    input()
    print("The lower  case letters represent White pieces and the")
    print("upper case letters represent Black pieces.")
    input()
    print("Enter the notations and the board will show the moves.")
    print("Here is the original position.")


# translates a letter-number coordinate such as e4 to a position on the board, eg 28
def coordinate(letter, number,notation):
    location = (ord(notation[letter]) - 97) + 8 * (int(notation[number]) - 1)
    return location
   

def calculateInput():
    notation = input()
    origin = 0
    if player == 0:
        # This is for moves made by pawns
        if notation[0].islower() == True:
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
                origin = coordinate(0,3,notation) - 8
            else:
                destination = coordinate(0,1,notation)
                if board[destination - 8] == "x":
                    origin = destination - 8
                if board[destination - 16] == "x":
                    origin = destination - 16
            movingPiece = "x"
            
        # This is for moves made by bishops
        if notation[0] == "B":
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
            else:
                destination = coordinate(1,2,notation)
            if destination in whiteSquares:
                for i in range(31):
                     if board[whiteSquares[i]] =="b":
                         origin = whiteSquares[i]
            else:
                for i in range(31):
                       if board[blackSquares[i]] =="b":
                          origin = blackSquares[i]
            movingPiece = "b"
            
        # This is for moves made by Queens
        if notation[0] == "Q":
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
            else:
                destination = coordinate(1,2,notation)
            for i in range(63):
                    if board[1] == "q":
                        origin = i
            movingPiece = "q"
            
        # This is for moves made by kings
        if notation[0] == "K":
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
            else:
                destination = coordinate(1,2,notation)
            for i in range(63):
                    if board[1] == "k":
                        origin = i
            movingPiece = "k"
            
        if notation[0] == "N":
            knightMoves = [15,17,6,10,-10,-6,-17,-15]
            destination = coordinate(len(notation)-2, len(notation) - 1,notation)
            if len(notation) > 3 and notation[1] != "x":
                if notation[1].isalpha() == True:
                    for i in range(7):
                        if board[(ord(notation[1]) - 97)+8*i] == "n":
                            origin = (ord(notation[1]) - 97)+8*i
                else:
                    for i in range(7):
                        if board[8*(int(notation[1])-1)+i] == "n":
                            origin = 8*(int(notation[1])-1)+i
            else:
                if destination <= 15:
                    if knightMoves.count(-17) == 1:
                        knightMoves.remove(-17)
                    if knightMoves.count(-15) == 1:
                        knightMoves.remove(-15)
                if destination <= 7:
                    if knightMoves.count(-10) == 1:
                        knightMoves.remove(-10)
                    if knightMoves.count(-6) == 1:
                        knightMoves.remove(-6)
                if destination >= 48:
                    if knightMoves.count(15) == 1:
                        knightMoves.remove(15)
                    if knightMoves.count(17) == 1:
                        knightMoves.remove(17)
                if destination >= 56:
                    if knightMoves.count(6) == 1:
                        knightMoves.remove(6)
                    if knightMoves.count(10) == 1:
                        knightMoves.remove(10)
                if destination % 8 == 0 or destination % 8 == 1:
                    if knightMoves.count(6) == 1:
                        knightMoves.remove(6)
                    if knightMoves.count(-10) == 1:
                        knightMoves.remove(-10)
                if destination % 8 == 0:
                    if knightMoves.count(15) == 1:
                        knightMoves.remove(15)
                    if knightMoves.count(-17) == 1:
                        knightMoves.remove(-17)
                if destination % 8 == 6 or destination % 8 == 7:
                    if knightMoves.count(10) == 1:
                        knightMoves.remove(10)
                    if knightMoves.count(-6) == 1:
                        knightMoves.remove(-6)
                if destination % 8 == 7:
                    if knightMoves.count(17) == 1:
                        knightMoves.remove(17)
                    if knightMoves.count(-15) == 1:
                        knightMoves.remove(-15)
                for i in range(len(knightMoves)):
                    if board[destination + knightMoves[i]] == "n":
                        origin = destination + knightMoves[i]
            movingPiece = "n"
            
        if notation[0] == "R":
            destination = coordinate(len(notation)-2, len(notation) - 1,notation)
            if len(notation) > 3 and notation[1] != "x":
                if notation[1].isalpha() == True:
                    for i in range(7):
                        if board[(ord(notation[1]) - 97)+8*i] == "r":
                            origin = (ord(notation[1]) - 97)+8*i
                else:
                    for i in range(7):
                        if board[8*(int(notation[1])-1)+i] == "r":
                            origin = 8*(int(notation[1])-1)+i
            else:
                for i in range(int(((destination % 8 + 56) - destination)/8 - 1)):
                    if board[destination + 8 * (i+1)] == "r":
                        origin = destination + 8 * (i+1)
                        break
                    elif board[destination + 8 * (i+1)] == " ":
                        pass
                    else:
                        break
                for i in range(int((destination - (destination % 8))/8 - 1)):
                    if board[destination - 8 * (i+1)] == "r":
                        origin = destination - 8 * (i+1)
                        break
                    elif board[destination + 8 * (i+1)] == " ":
                        pass
                    else:
                        break
                for i in range(int(destination % 8 - 1)):
                    if board[destination - (i+1)] == "r":
                        origin = destination -(i+1)
                        break
                    elif board[destination - (i+1)] == " ":
                        pass
                    else:
                        break
                for i in range(int(6 - destination % 8)):
                    if board[destination + (i+1)] == "r":
                        origin = destination + (i+1)
                        break
                    elif board[destination + (i+1)] == " ":
                        pass
                    else:
                        break
                movingPiece = "r"
        
            
            
                
    if player == 1:
         # This is for moves made by pawns
        if notation[0].islower() == True:
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
                origin = coordinate(0,3,notation) + 8
            else:
                destination = coordinate(0,1,notation)
                if board[destination + 8] == "X":
                    origin = destination + 8
                if board[destination + 16] == "X":
                    origin = destination + 16
            movingPiece = "X"
            
        # This is for moves made by bishops
        if notation[0] == "B":
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
            else:
                destination = coordinate(1,2,notation)
            if destination in whiteSquares:
                for i in range(31):
                     if board[whiteSquares[i]] =="B":
                         origin = whiteSquares[i]
            else:
                for i in range(31):
                       if board[blackSquares[i]] =="B":
                          origin = blackSquares[i]
            movingPiece = "B"
            
        # This is for moves made by Queens
        if notation[0] == "Q":
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
            else:
                destination = coordinate(1,2,notation)
            for i in range(63):
                    if board[i] == "Q":
                        origin = i
            movingPiece = "Q"
            
        # This is for moves made by kings
        if notation[0] == "K":
            if notation[1] == "x":
                destination = coordinate(2,3,notation)
            else:
                destination = coordinate(1,2,notation)
            for i in range(63):
                    if board[i] == "K":
                        origin = i
            movingPiece = "K"
            
        if notation[0] == "N":
            knightMoves = [15,17,6,10,-10,-6,-17,-15]
            destination = coordinate(len(notation)-2, len(notation) - 1,notation)
            if len(notation) > 3 and notation[1] != "x":
                if notation[1].isalpha() == True:
                    for i in range(7):
                        if board[(ord(notation[1]) - 97)+8*i] == "N":
                            origin = (ord(notation[1]) - 97)+8*i
                else:
                    for i in range(7):
                        if board[8*(int(notation[1])-1)+i] == "N":
                            origin = 8*(int(notation[1])-1)+i
            else:
                if destination <= 15:
                    if knightMoves.count(-17) == 1:
                        knightMoves.remove(-17)
                    if knightMoves.count(-15) == 1:
                        knightMoves.remove(-15)
                if destination <= 7:
                    if knightMoves.count(-10) == 1:
                        knightMoves.remove(-10)
                    if knightMoves.count(-6) == 1:
                        knightMoves.remove(-6)
                if destination >= 48:
                    if knightMoves.count(15) == 1:
                        knightMoves.remove(15)
                    if knightMoves.count(17) == 1:
                        knightMoves.remove(17)
                if destination >= 56:
                    if knightMoves.count(6) == 1:
                        knightMoves.remove(6)
                    if knightMoves.count(10) == 1:
                        knightMoves.remove(10)
                if destination % 8 == 0 or destination % 8 == 1:
                    if knightMoves.count(6) == 1:
                        knightMoves.remove(6)
                    if knightMoves.count(-10) == 1:
                        knightMoves.remove(-10)
                if destination % 8 == 0:
                    if knightMoves.count(15) == 1:
                        knightMoves.remove(15)
                    if knightMoves.count(-17) == 1:
                        knightMoves.remove(-17)
                if destination % 8 == 6 or destination % 8 == 7:
                    if knightMoves.count(10) == 1:
                        knightMoves.remove(10)
                    if knightMoves.count(-6) == 1:
                        knightMoves.remove(-6)
                if destination % 8 == 7:
                    if knightMoves.count(17) == 1:
                        knightMoves.remove(17)
                    if knightMoves.count(-15) == 1:
                        knightMoves.remove(-15)
                for i in range(len(knightMoves) - 1):
                    if board[destination + knightMoves[i]] == "N":
                        origin = destination + knightMoves[i]
            movingPiece = "N"
            
        if notation[0] == "R":
            destination = coordinate(len(notation)-2, len(notation) - 1,notation)
            if len(notation) > 3 and notation[1] != "x":
                if notation[1].isalpha() == True:
                    for i in range(7):
                        if board[(ord(notation[1]) - 97)+8*i] == "R":
                            origin = (ord(notation[1]) - 97)+8*i
                else:
                    for i in range(7):
                        if board[8*(int(notation[1])-1)+i] == "R":
                            origin = 8*(int(notation[1])-1)+i
            else:
                for i in range(int(((destination % 8 + 56) - destination)/8 - 1)):
                    if board[destination + 8 * (i+1)] == "R":
                        origin = destination + 8 * (i+1)
                        break
                    elif board[destination + 8 * (i+1)] == " ":
                        pass
                    else:
                        break
                for i in range(int((destination - (destination % 8))/8 - 1)):
                    if board[destination - 8 * (i+1)] == "R":
                        origin = destination - 8 * (i+1)
                        break
                    elif board[destination + 8 * (i+1)] == " ":
                        pass
                    else:
                        break
                for i in range(int(destination % 8 - 1)):
                    if board[destination - (i+1)] == "R":
                        origin = destination -(i+1)
                        break
                    elif board[destination - (i+1)] == " ":
                        pass
                    else:
                        break
                for i in range(int(6 - destination % 8)):
                    if board[destination + (i+1)] == "R":
                        origin = destination + (i+1)
                        break
                    elif board[destination + (i+1)] == " ":
                        pass
                    else:
                        break
                movingPiece = "R"

    if notation == "0-0" or notation == "O-O":
        if player == 0:
            board[6] = "k"
            board[5] = "r"
            board[7] = " "
            board[4] = " "
        if player == 1:
            board[62] = "K"
            board[61] = "R"
            board[63] = " "
            board[60] = " "
    elif notation == "0-0-0" or notation == "O-O-O":
        if player == 0:
            board[2] = "k"
            board[3] = "r"
            board[0] = " "
            board[4] = " "
        if player == 1:
            board[58] = "K"
            board[59] = "R"
            board[56] = " "
            board[60] = " "
                
    else:
        board[destination] = movingPiece
        board[origin] = " "

            

def showScreen():
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("8| " + board[56] + " | " + board[57] + " | " + board[58] + " | " + board[59] + 
          " | " + board[60] + " | " + board[61] + " | " + board[62] + " | " + board[63] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("7| " + board[48] + " | " + board[49] + " | " + board[50] + " | " + board[51] +
          " | " + board[52] + " | " + board[53] + " | " + board[54] + " | " + board[55] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("6| " + board[40] + " | " + board[41] + " | " + board[42] + " | " + board[43] +
          " | " + board[44] + " | " + board[45] + " | " + board[46] + " | " + board[47] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("5| " + board[32] + " | " + board[33] + " | " + board[34] + " | " + board[35] +
          " | " + board[36] + " | " + board[37] + " | " + board[38] + " | " + board[39] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("4| " + board[24] + " | " + board[25] + " | " + board[26] + " | " + board[27] +
          " | " + board[28] + " | " + board[29] + " | " + board[30] + " | " + board[31] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("3| " + board[16] + " | " + board[17] + " | " + board[18] + " | " + board[19] +
          " | " + board[20] + " | " + board[21] + " | " + board[22] + " | " + board[23] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("2| " + board[8] + " | " + board[9] + " | " + board[10] + " | " + board[11] +
          " | " + board[12] + " | " + board[13] + " | " + board[14] + " | " + board[15] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print(" |   |   |   |   |   |   |   |   |")
    print("1| " + board[0] + " | " + board[1] + " | " + board[2] + " | " + board[3] +
          " | " + board[4] + " | " + board[5] + " | " + board[6] + " | " + board[7] + " |")
    print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")
    print("   a   b   c   d   e   f   g   h  ")





introScreen()
showScreen()
while 1 == 1:  
    calculateInput()
    player = (player + 1) % 2
    showScreen()
