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
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whitetoMove= True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False


    def undoMove(self):
         if len(self.moveLog)!=0:
              move = self.moveLog.pop()
              self.board[move.startRow][move.startCol] = move.pieceMoved
              self.board[move.endRow][move.endCol] = move.pieceCaptured
              self.whitetoMove = not self.whitetoMove
              if move.pieceMoved == "wK":
               self.whiteKingLoc = (move.endRow, move.endCol)
              if move.pieceMoved == "bK":
               self.blackKingLoc = (move.endRow, move.endCol)
              

    def makeMove(self,move):
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.whitetoMove = not self.whitetoMove
            if move.pieceMoved == "wK":
               self.whiteKingLoc = (move.endRow, move.endCol)
            if move.pieceMoved == "bK":
               self.blackKingLoc = (move.endRow, move.endCol)

    def getValidMoves(self):
         moves = self.getAllPossibleMoves()

         for i in range(len(moves)-1,-1,-1):
             self.makeMove(moves[i])
             self.whitetoMove = not self.whitetoMove
             if self.incheck():
                 moves.remove(moves[i])
             self.whitetoMove = not self.whitetoMove
             self.undoMove()
         if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
         else:
            self.checkMate = False
            self.staleMate = False
    

         return moves
    
    def incheck(self):
        if self.whitetoMove:
            return self.sqUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.sqUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    
    def sqUnderAttack(self,r,c):
        self.whitetoMove = not self.whitetoMove
        oppMoves = self.getAllPossibleMoves()
        self.whitetoMove = not self.whitetoMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    

    def getAllPossibleMoves(self):
         moves = []
         for r in range(len(self.board)):
              for c in range(len(self.board)):
                   turn = self.board[r][c][0]
                   piece = self.board[r][c][1]
                   if(turn == 'w' and self.whitetoMove) or (turn == 'b' and not self.whitetoMove):
                        self.moveFunctions[piece](r,c, moves)
         return moves 

    def getPawnMoves(self,r,c,moves):
          if self.whitetoMove:
              if self.board[r-1][c] == "--":
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c] == "--":
                       moves.append(Move((r,c),(r-2,c),self.board))
                    if c-1>=0: #moves left
                        if self.board[r-1][c-1][0]=="b":
                           moves.append(Move((r,c),(r-1,c-1),self.board))
                    if c+1<=7: #moves right
                         if self.board[r-1][c+1][0]=="b":
                           moves.append(Move((r,c),(r-1,c+1),self.board))
          else:
               if self.board[r+1][c] == "--":
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r==1 and self.board[r+2][c] == "--":
                       moves.append(Move((r,c),(r+2,c),self.board))
                    if c-1>=0: #moves left
                        if self.board[r+1][c-1][0]=="w":
                           moves.append(Move((r,c),(r+1,c-1),self.board))
                    if c+1<=7:    #moves right
                         if self.board[r+1][c+1][0]=="w":
                           moves.append(Move((r,c),(r+1,c+1),self.board))
             


    def getRookMoves(self,r,c,moves):
            directions = ((-1,0),(1,0),(0,-1),(0,1))
            if self.whitetoMove:
               enemyColor = "b" 
            else:
               enemyColor ="w"
            for d in directions:
                for i in range(1,8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                    else:
                        break
            
                        

    

    def getKnightMoves(self,r,c,moves):
          knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
          if self.whitetoMove:
               allyColor = "w"
          else:
              allyColor = "b"
          for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
    


    def getBishopMoves(self,r,c,moves):
            directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #top-left,top-right,bottom-left,bottom-right
            if self.whitetoMove:
               enemyColor = "b" 
            else:
               enemyColor ="w"
            for d in directions:
                for i in range(1,8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                    else:
                        break
            
    def getQueenMoves(self,r,c,moves):
         self.getRookMoves(r,c,moves)
         self.getBishopMoves(r,c,moves)

    def getKingMoves(self,r,c,moves):
          directions = ((1,1),(1,-1),(1,0),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1))
          allyColor = "w" if self.whitetoMove else "b"
          for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
    

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
        
