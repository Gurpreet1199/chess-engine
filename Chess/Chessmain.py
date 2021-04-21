# THis is main driver file
import pygame as p
import ChessEngine
import SmartMoveFinder

WIDTH=HEIGHT=512
DIMENSION=8
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS=15
IMAGES={}

def loadImages():
    pieces={'wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ'}
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+ piece+".png"),(SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate=False
    loadImages()
    running=True
    sqSelected=()#no squre is selected initially(row,column tuple)
    playerClicks=[] #track of clicks
    gameOver=False
    playerOne=True#if human is playing white then true else false for AI
    playerTwo=False#same as above but for black

    while running:
        humanTurn=(gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type==p.QUIT:
                running =False
            elif e.type==p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location=p.mouse.get_pos()#location of mouse
                    col=location[0]//SQ_SIZE
                    row=location[1]//SQ_SIZE
                    if sqSelected==(row,col): #clicking same square twice
                        sqSelected=() #deselect
                        playerClicks=[]
                    else:
                        sqSelected=(row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks)==2:
                        move= ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move==validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade=True
                                animate=True
                                sqSelected=() #reseting user clicks
                                playerClicks=[]
                        if not moveMade:
                            playerClicks=[sqSelected]
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undoMove()
                    moveMade=True
                    animate=False
                    gameOver=False
                if e.key==p.K_r:#reset the board
                    gs=ChessEngine.GameState()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
                    gameOver=False

        #AI MOVE FINDER
        if not gameOver and not humanTurn:
            AImove=SmartMoveFinder.findBestMove(gs,validMoves)
            if AImove is None:
                AImove=SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AImove)
            moveMade=True
            animate=True


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade= False
            animate=False

        drawGameState(screen,gs,validMoves,sqSelected)
        if gs.checkMate:
            gameOver=True
            if gs.whiteToMove:
                drawText(screen,'BLACK WINS BY CHECKMATE')
            else:
                drawText(screen,'WHITE WINS BY CHECKMATE')
        elif gs.staleMate:
            gameOver=True
            drawText(screen,'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()


# highlighting piece
def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected!=():
        r,c=sqSelected
        if gs.board[r][c][0]==('w' if gs.whiteToMove else 'b'):#sqSelected is a piece to be moved
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)#transparency value 0->225
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            #highlite move from that square
            s.fill(p.Color('Yellow'))
            for move in validMoves:
                if move.startRow==r and move.startCol==c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))





def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)#draw saure on the board
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    global colors
    colors=[p.Color("white"),p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]
            if piece !="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def animateMove(move,screen,board,clock):
    global colors
    coords=[]#list of coordinates that the animation will  move through
    dR=move.endRow-move.startRow
    dC=move.endCol-move.startCol
    framesPerSquare=10
    frameCount=(abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c=(move.startRow+dR*frame/frameCount,move.startCol+dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        #erase piece moved from its ending square
        color=colors[(move.endRow+move.endCol)%2]
        endSquare=p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured!='--':
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen,text):
    font=p.font.SysFont("Helvitca",32,True,False)
    textObject=font.render(text,0,p.Color('Black'))
    textLocation=p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
if __name__ == "__main__":
    main()