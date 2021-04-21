# # responsible for storing current staet of chess and determineing the calid moves
# also keep moves log
class GameState():
    def __init__(self):
        #8x8
        self.board=[
            [ "bR","bN","bB","bQ","bK","bB","bN","bR" ],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--",],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        # self.board = [
        #     ["--", "--", "--", "--", "bK", "--", "--", "--",],
        #     ["--", "--", "--", "--", "--", "--", "--", "--",],
        #     ["--", "--", "--", "--", "--", "--", "--", "--", ],
        #     ["--", "--", "--", "--", "--", "--", "--", "--", ],
        #     ["--", "--", "--", "--", "--", "--", "--", "--", ],
        #     ["--", "--", "--", "--", "--", "--", "--", "--", ],
        #     ["--", "--", "--", "--", "--", "--", "--", "--",],
        #     ["--", "--", "--", "wQ", "wK", "--", "--", "--",],
        # ]

        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                            'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove=True
        self.moveLog=[]
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.checkMate=False
        self.staleMate=False
        self.enpassantPossible=()#cordinates for enpassant coordinare
        self.enPassantPossibleLog=[self.enpassantPossible]
        self.currentCastlingRight=CastleRights(True,True,True,True)
        self.castleRightLog=[CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wks,self.currentCastlingRight.bqs)]





    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove # switching turns
        #update king location
        if move.pieceMoved=='wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved=='bK':
            self.blackKingLocation = (move.endRow,move.endCol)

        #pawn promotoin
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.pieceMoved[0]+'Q'

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol]='--'#capturing pawn

        #update enpassant possible variable
        if move.pieceMoved[1]=='p' and abs(move.startRow-move.endRow)==2:
            self.enpassantPossible=((move.startRow+move.endRow)//2,move.startCol)

        else:
            self.enpassantPossible=()

        if move.isCastleMove:
            if move.endCol-move.startCol ==2:
                self.board[move.endRow][move.endCol-1]=self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1]='--'
            else:
                self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2]='--'

        self.enPassantPossibleLog.append(self.enpassantPossible)

        self.updateCastleRights(move)

        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wks,self.currentCastlingRight.bqs))






    def undoMove(self):
        if len(self.moveLog)!=0:
            move=self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove=not self.whiteToMove
            #update king position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol]='--'#leave landing square blank
                self.board[move.startRow][move.startCol]=move.pieceCaptured
            self.enPassantPossibleLog.pop()
            self.enpassantPossible=self.enPassantPossibleLog[-1]

            self.castleRightLog.pop()
            self.currentCastlingRight=self.castleRightLog[-1]

            if move.isCastleMove:
                if move.endCol-move.startCol==2:
                    self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1]='--'
                else:
                    self.board[move.endRow][move.endCol-2]=self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1]='--'
            self.checkMate=False
            self.staleMate=False

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False
        if move.pieceCaptured=='wR':
            if move.endRow==7:
                if move.endCol==0:
                    self.currentCastlingRight.wqs=False
                elif move.endCol==7:
                    self.currentCastlingRight.wks=False
        elif move.pieceCaptured=='bR':
            if move.endRow==0:
                if move.endCol==0:
                    self.currentCastlingRight.bqs=False
                elif move.endCol==7:
                    self.currentCastlingRight.bks=False





    #considering check
    def getValidMoves(self):
        tempEnpassantPossible=self.enpassantPossible
        tempCastleRights=CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wks,self.currentCastlingRight.bqs)
        moves=self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)

        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            self.whiteToMove=not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove=not self.whiteToMove
            self.undoMove()

        if len(moves)==0:
            if self.inCheck():
                self.checkMate=True
                print("checkmate\n")
            else:
                self.staleMate=True
                print("Stalemate\n")
        else:
            self.checkMate=False
            self.staleMate=False


        self.enpassantPossible=tempEnpassantPossible
        self.currentCastlingRight=tempCastleRights
        return moves




    #without check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow==r and move.endCol==c:
                return True

        return False




    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if(turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove:
            if self.board[r-1][c]=="--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board))

            #capture
            if c-1>=0: #capture to the left
                if self.board[r-1][c-1][0]=='b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove=True))

            if c+1<=7: #capture to thr right
                if self.board[r - 1][c +1][0] =='b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c +1), self.board, isEnpassantMove=True))

        else:#black pawn move
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board))

            if c-1>=0:#capture to left
                if self.board[r+1][c-1][0]=='w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c+1<=7:
                if self.board[r+1][c+1][0]=='w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r +1, c + 1), self.board, isEnpassantMove=True))




    def getRookMoves(self,r,c,moves):
        directions=((-1,0),(0,-1),(1,0),(0,1))
        enemyColor= "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":#enpty space valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))






    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)


    def getKingsideCastleMoves(self,r,c,moves):
        if self.board[r][c+1]=='--' and self.board[r][c+2]=='--' and \
                not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))

    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]=='--' and \
                not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))




    def getBishopMoves(self,r,c,moves):
        directions=((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self,r,c,moves):
        kingMoves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor="w" if self.whiteToMove else "b"
        for i in range(8):
            endRow=r+kingMoves[i][0]
            endCol=c+kingMoves[i][1]
            if 0<=endRow< 8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:#empty or enemy piece
                    moves.append(Move((r,c),(endRow,endCol),self.board))

class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs

class Move():
    # computer nmatrix to rank-file notation in chess
    ranksToRows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}
    filesToCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles={v : k for k , v in filesToCols.items()}

    def __init__(self,startSq,endSq,board,isEnpassantMove=False,isCastleMove=False):
         self.startRow=startSq[0]
         self.startCol=startSq[1]
         self.endRow=endSq[0]
         self.endCol=endSq[1]
         self.pieceMoved = board[self.startRow][self.startCol]
         self.pieceCaptured=board[self.endRow][self.endCol]
         self.isPawnPromotion =False
         if (self.pieceMoved=='wp' and self.endRow==0) or (self.pieceMoved=='bp' and self.endRow==7):
             self.isPawnPromotion=True

         self.isEnpassantMove = isEnpassantMove
         if self.isEnpassantMove:
             self.pieceCaptured='wp' if self.pieceMoved=='bp' else 'bp'

         self.isCastleMove=isCastleMove

         self.moveID = self.startRow*1000 + self.startCol*100 +self.endRow*10 + self.endCol
         # print(self.moveID)

    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]

