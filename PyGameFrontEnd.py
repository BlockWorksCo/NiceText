#
# Copyright (C) BlockWorks Consulting Ltd - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Steve Tickle <Steve@BlockWorks.co>, June 2015.
#



import time
import sys
import pygame



class PyGameFrontEnd:
    """
    """

    def __init__(self):
        """
        """
        pygame.init()

        self.width                  = 500
        self.height                 = 300
        self.textBackgroundColour   = (0x27,0x28,0x22)
        self.textColour             = (0xf8,0xf8,0xf2)
        #self.fontName              = "Comic Sans MS"
        #self.fontName              = 'Calibri'
        self.fontName               = 'Consolas'
        self.fontSize               = 14
        self.lines                  = []
        self.cursorX                = 20
        self.cursorY                = 20
        self.cursorColour           = (0xff,0xff,0xff)
        self.lastIdleTimestamp      = 0
        self.cursorState            = 0

        self.screen = pygame.display.set_mode( (self.width,self.height), pygame.RESIZABLE )

        self.Display()



    def Clear(self):
        """
        """
        pass



    def SetCursorPosition(self, x,y):
        """
        """
        pass


    def ShowEditingContext(self, context):
        """
        """
        self.Clear()
        self.lines  = context.lines

        self.Display()


    def GetScreenSize(self):
        """
        """        
        byte    = ''
        result  = ''

        while byte != 't':
            byte    = sys.stdin.read(1)
            print('-%s-'%result)
            result  = result + byte


        rowsText,columnsText    = re.compile('9;([0-9]+);([0-9]+)').findall(result)[0]
        rows    = int(rowsText)
        columns = int(columnsText)

        return rows,columns


    def Display( self ):
        """
        """
        myfont = pygame.font.SysFont( self.fontName, self.fontSize )
        #label   = myfont.render( "Some text!", 1, self.textColour )
        #self.screen.blit( label, (100, 100))


        lineNumber  = 0
        lineHeight  = self.fontSize
        for line in self.lines:

            lineText   = myfont.render( line, 1, self.textColour )
            self.screen.blit( lineText, (10, lineNumber*lineHeight))

            lineNumber  = lineNumber + 1


        pygame.display.set_caption("NiceText :o)")
        pygame.display.flip()


    def Idle(self):
        """
        """

        deltaTimestamp   = self.timestamp - self.lastIdleTimestamp

        if deltaTimestamp >= 200:

            cursorRect  = pygame.Rect([self.cursorX,self.cursorY],[10,self.fontSize])
            cursorRect  = pygame.Rect([10,10],[10,self.fontSize])

            if self.cursorState == 0:
                pygame.draw.rect( self.screen, self.textBackgroundColour, cursorRect, 0)
                print('tick')
                self.cursorState = 1

            elif self.cursorState == 1:
                pygame.draw.rect( self.screen, self.cursorColour, cursorRect, 0)
                print('tock')
                self.cursorState = 0

            self.lastIdleTimestamp  = self.timestamp
            pygame.display.flip()

        time.sleep(0.05)



    def GetUserInput(self):
        """
        """
        pygame.event.pump()
        event           = pygame.event.poll()
        self.timestamp  = pygame.time.get_ticks()


        if event.type == pygame.QUIT: 
            pygame.display.quit()

        elif event.type == pygame.VIDEORESIZE:

            width,height    = event.dict['size']
            self.width      = width
            self.height     = height
            self.screen = pygame.display.set_mode( (self.width,self.height), pygame.RESIZABLE )

            self.Display()

        elif event.type == pygame.NOEVENT:
            self.Idle()

