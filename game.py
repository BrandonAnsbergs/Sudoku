import pygame
import os
from grid import Grid  # Assuming "grid.py" contains the Grid class


# Set environment variable for window position
os.environ['SOL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)

# Initialize pygame and create display surface
surface = pygame.display.set_mode((1200,900))
pygame.display.set_caption('Sudoku')

# Initialize fonts
pygame.font.init()
game_font = pygame.font.SysFont('Comic Sans MS', 50)
game_font2 = pygame.font.SysFont('Comic Sans MS', 24)

# Create grid object
grid = Grid(pygame, game_font)

# Flag for game loop
running = True

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Set running to False to exit the loop
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
            if pygame.mouse.get_pressed()[0]:  # Check left mouse button click
                pos = pygame.mouse.get_pos()
                grid.get_mouse_click(pos[0], pos[1])  # Handle mouse click on grid
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.win:
                grid.restart()  # Restart game if spacebar is pressed and the game is won
    
    # Fill the surface with black color
    surface.fill((0,0,0))

    # Draw the grid
    grid.draw_all(pygame, surface)

    # Display win message if the game is won
    if grid.win:
        # Render "You Won!" text
        won_surface = game_font.render("You Won!", False, (0,255,0))
        surface.blit(won_surface, (950,650))

        # Render "Press Space to Restart!" text
        press_space_surf = game_font2.render("Press Space to Restart!", False, (0,255,0))
        surface.blit(press_space_surf,  (950,750))

    # Update the display
    pygame.display.flip()
