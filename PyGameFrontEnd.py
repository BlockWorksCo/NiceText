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

    def __init__(self, backEnd):
        """
        """
        pygame.init()

        self.backEnd                = backEnd
        self.width                  = 1000
        self.height                 = 600
        self.textBackgroundColour   = (0x27,0x28,0x22)
        self.textColour             = (0xf8,0xf8,0xf2)
        #self.fontName              = "Comic Sans MS"
        #self.fontName              = 'Calibri'
        #self.fontName               = 'Consolas'
        self.fontName               = 'Emilbus Mono'
        self.fontSize               = 20
        self.font                   = pygame.font.SysFont( self.fontName, self.fontSize )
        cw,ch                       = self.font.size(' ')
        self.lines                  = []
        self.cursorX                = 0
        self.cursorY                = 0
        self.cursorColour           = (0xff,0xff,0xff)
        self.lastIdleTimestamp      = 0
        self.cursorState            = 0
        self.characterWidth         = cw
        self.characterHeight        = ch
        self.frameBufferWidth       = self.width / self.characterWidth
        self.frameBufferHeight      = self.height / self.characterHeight
        self.frameBufferStart       = 0
        self.frameBuffer            = ' ' * self.frameBufferWidth * self.frameBufferHeight;

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
        #label   = myfont.render( "Some text!", 1, self.textColour )
        #self.screen.blit( label, (100, 100))

        windowRect  = pygame.Rect([0,0],[self.width,self.height])
        pygame.draw.rect( self.screen, self.textBackgroundColour, windowRect, 0)

        lines   = self.backEnd.GetLinesBetween(self.frameBufferStart, self.frameBufferStart+self.frameBufferHeight)

        lineNumber  = 0
        lineHeight  = self.fontSize
        for line in lines:

            lineText   = self.font.render( line, 1, self.textColour )
            self.screen.blit( lineText, (10, lineNumber*lineHeight))

            lineNumber  = lineNumber + 1

        pygame.display.set_caption("NiceText :o)")
        pygame.display.flip()



    def Idle(self):
        """
        """

        deltaTimestamp   = self.timestamp - self.lastIdleTimestamp

        if deltaTimestamp >= 200:

            cursorRect  = pygame.Rect([self.cursorX*self.characterWidth,self.cursorY*self.characterHeight],[self.characterWidth,self.characterHeight])

            if self.cursorState == 0:
                pygame.draw.rect( self.screen, self.textBackgroundColour, cursorRect, 0)
                self.cursorState = 1

            elif self.cursorState == 1:
                pygame.draw.rect( self.screen, self.cursorColour, cursorRect, 0)
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


        keys    = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            print('K_UP')
            #self.cursorY = self.cursorY - 1
            self.frameBufferStart = self.frameBufferStart - 1
            self.Display()

        if keys[pygame.K_DOWN]:
            print('K_DOWN')
            #self.cursorY = self.cursorY + 1
            self.frameBufferStart = self.frameBufferStart + 1
            self.Display()
            
        if keys[pygame.K_LEFT]:
            print('K_LEFT')
            self.cursorX = self.cursorX - 1
            
        if keys[pygame.K_RIGHT]:
            print('K_RIGHT')
            self.cursorX = self.cursorX + 1
            
        if keys[pygame.K_PAGEUP]:
            print('K_PAGEUP')
            #self.cursorY = self.cursorY + 1
            self.frameBufferStart = self.frameBufferStart - self.frameBufferHeight
            self.Display()
            
        if keys[pygame.K_PAGEDOWN]:
            print('K_PAGEDOWN')
            #self.cursorY = self.cursorY + 1
            self.frameBufferStart = self.frameBufferStart + self.frameBufferHeight
            self.Display()
            


