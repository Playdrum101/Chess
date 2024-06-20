"""" Checks Valid Moves"""

class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whitetoMove= True
        self.moveLog = []

    def undoMove(self):
         if len(self.moveLog)!=0:
              move = self.moveLog.pop()
              self.board[move.startRow][move.startCol] = move.pieceMoved
              self.board[move.endRow][move.endCol] = move.pieceCaptured
              self.whitetoMove = not self.whitetoMove
              

    def makeMove(self,move):
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.whitetoMove = not self.whitetoMove

    def getValidMoves(self):
         return self.getAllPossibleMoves()
    

    def getAllPossibleMoves(self):
         moves = []
         for r in range(len(self.board)):
              for c in range(len(self.board)):
                   turn = self.board[r][c][0]
                   piece = self.board[r][c][1]
                   if(turn == 'w' and self.whitetoMove) or (turn == 'b' and not self.whitetoMove):
                        if piece == "P":
                             self.getPawnmoves(r,c,moves)
                        elif piece == "R":
                             self.getRookmoves(r,c,moves)
         return moves 

    def getPawnmoves(self,r,c,moves):
        if self.whitetoMove:
              if self.board[r-1][c] == "--":
                   moves.append(Move((r,c),(r-1,c),self.board))
                   if r==6 and self.board[r-2][c] == "--":
                       moves.append(Move((r,c),(r-2,c),self.board))

    def getRookmoves(self,r,c,moves):
         pass
    

class Move():

    rankstoRows = { "1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}

    rowstoRanks = { v:k for k,v in rankstoRows.items()}

    filestoCols = { "a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}

    colstoFiles = { v:k for k,v in filestoCols.items()}
      
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol  =startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)


    def __eq__(self,other):
         if isinstance(other,Move):
              return self.moveID == other.moveID
         return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
        

    def getRankFile(self,r,c):
        return self.rowstoRanks[r] + self.colstoFiles[c]
        
