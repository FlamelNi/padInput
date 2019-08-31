import pygame
import math
import angleLib


def open_window():
    from padInput import get_mapping
    
    # define the RGB value for white, 
    #  green, blue colour . 
    white = (255, 255, 255) 
    green = (0, 255, 0) 
    blue = (0, 0, 128) 
    black = (0, 0, 0)
      
    # assigning values to width and height variable 
    width = 800
    height = 400
    windowName = 'Type Guide'

    # create the display surface object
    # of specific dimension..e(width, height).
    display_surface = pygame.display.set_mode((width, height))
      
    # set the pygame window name 
    pygame.display.set_caption(windowName) 

    # create a font object. 
    # 1st parameter is the font file 
    # which is present in pygame. 
    # 2nd parameter is size of the font 
    # font = pygame.font.Font('C:\\Windows\\Fonts\\Arial.ttf', 32) 
    font = pygame.font.Font('freesansbold.ttf', 16) 

    # print(pygame.font.get_fonts())

    # create a text suface object, 
    # on which text is drawn on it. 
    # create a rectangular object for the 
    # text surface object 
    # set the center of the rectangular object.

    texts = []

    for side in range(0,2):
        
        center_x = side * width / 2 + width / 4
        center_y = height/2
        
        for i in list(get_mapping()[side].keys()):
            
            angle_offset = angleLib.four_to_section(i) * 90
            
            for j in list(get_mapping()[side][i].keys()):
                angle_offset = angleLib.four_to_section(i) * 90
                text = font.render(get_mapping()[side][i][j], True, black, white)
                textRect = text.get_rect()
                offset_x = 0
                offset_y = 0
                if j == '':
                    pass
                elif j == 'L':
                    angle_offset = angle_offset + 30
                elif j == 'R':
                    angle_offset = angle_offset - 30
                elif j == 'B':
                    textRect.center = (center_x, center_y)
                    texts.append((text, textRect))
                    break
                offset_x = angleLib.vec2coord((width/8, angle_offset))[0] + center_x
                offset_y = -angleLib.vec2coord((width/8, angle_offset))[1] + center_y
                # offset_x = round(offset_x)
                # offset_y = round(offset_y)
                textRect.center = (offset_x, offset_y)
                texts.append((text, textRect))
        
        # text = font.render('GeeksForGeeks', True, black, white)
        # textRect = text.get_rect()
        # textRect.center = (width / 2, height / 2) 
        display_surface.fill(white) 
      
        # copying the text surface object 
        # to the display surface object  
        # at the center coordinate. 
        for t in texts:
            display_surface.blit(t[0], t[1])
        pygame.display.update()

def close_window():
    pygame.display.quit()
    pygame.display.init()
    

'''
# infinite loop 
while True : 
  
    # completely fill the surface object 
    # with white color 
    display_surface.fill(white) 
  
    # copying the text surface object 
    # to the display surface object  
    # at the center coordinate. 
    for t in texts:
        display_surface.blit(t[0], t[1]) 
        # display_surface.blit(text, textRect) 
  
    # iterate over the list of Event objects 
    # that was returned by pygame.event.get() method. 
    for event in pygame.event.get() : 
  
        # if event object type is QUIT 
        # then quitting the pygame 
        # and program both. 
        if event.type == pygame.QUIT : 
  
            # deactivates the pygame library 
            pygame.quit() 
  
            # quit the program. 
            quit() 
  
        # Draws the surface object to the screen.   
        pygame.display.update()

'''
