from random import sample
from button import SelectNumber  # Assuming "button.py" contains the SelectNumber class
from copy import deepcopy

def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    # Function to create line coordinates for drawing grid lines
    points = []
    for y in range(1,9):
        temp = []
        temp.append((0, y * cell_size))
        temp.append((900, y * cell_size))
        points.append(temp)

    for x in range(1,10):
        temp = []
        temp.append((x * cell_size, 0))
        temp.append((x * cell_size, 900))
        points.append(temp)
    return points

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def pattern(row_num: int, col_num: int) -> int:
    # Function to generate pattern for grid creation
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE

def shuffle(samp: range) -> list:
    # Function to shuffle a range
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    # Function to create a Sudoku grid
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)]for c in cols]for r in rows]

def remove_numbers(grid: list[list]) -> None:
    # Function to remove numbers from the grid to make it a puzzle
    num_of_cells = GRID_SIZE * GRID_SIZE
    empties = num_of_cells * 3 // 7
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0

class Grid:
    def __init__(self, pygame, font):
        # Initialize grid parameters
        self.cell_size = 100
        self.num_x_offset = 35
        self.num_y_offset = 12
        self.line_coordinates = create_line_coordinates(self.cell_size)
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        self.win = False

        # Remove numbers to create puzzle
        remove_numbers(self.grid)
        # Get coordinates of pre-occupied cells
        self.occupied_cell_coordinates = self.pre_occupied_cells()
        
        # Initialize font and selection
        self.game_font = font
        self.selection = SelectNumber(pygame, self.game_font)

    def restart(self) -> None:
        # Restart the game by resetting the grid
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()
        self.win = False

    def check_grid(self):
        # Check if the current grid matches the test grid (solution)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        # Check if a cell is pre-occupied (initially filled)
        for cell in self.occupied_cell_coordinates:
            if x == cell[1] and y == cell[0]:
                return True
        return False

    def get_mouse_click(self, x: int, y: int) -> None:
        # Handle mouse clicks
        if x <= 900:
            grid_x, grid_y = x // 100, y // 100
            if not self.is_cell_preoccupied(grid_x, grid_y):
                self.set_cell(grid_x, grid_y, self.selection.selected_number) 
        self.selection.button_clicked(x,y)   
        if self.check_grid():
            self.win = True

    def pre_occupied_cells(self) -> list[tuple]:
        # Get coordinates of pre-occupied cells
        occupied_cell_coordinates = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x,y) != 0:
                    occupied_cell_coordinates.append((x,y))
        return occupied_cell_coordinates

    def __draw_lines(self, pg, surface) -> None:
        # Draw grid lines
        for index, point in enumerate(self.line_coordinates):
            pg.draw.line(surface, (0, 50, 0), point[0], point[1])
            if index == 2 or index == 5 or index == 10 or index == 13:
                pg.draw.line(surface, (255, 200, 0), point[0], point[1])
            else:
                pg.draw.line(surface, (0, 50, 0), point[0], point[1])

    def __draw_numbers(self, surface) -> None:
        # Draw numbers on the grid
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x,y) != 0:
                    if (y, x) in self.occupied_cell_coordinates:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0, 200, 255))
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0, 255, 0))

                    if self.get_cell(x, y) != self.__test_grid[y][x]:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (255, 0 ,0))

                    surface.blit(text_surface, (x * self.cell_size + self.num_x_offset, y * self.cell_size + self.num_y_offset))

    def draw_all(self, pg, surface):
        # Draw grid lines and numbers
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface)

    def get_cell(self, x: int, y: int) -> int:
        # Get value of a cell in the grid
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        # Set value of a cell in the grid
        self.grid[y][x] = value

    def show(self):
        # Print the grid (for debugging purposes)
        for cell in self.grid:
            print(cell)

if __name__ == "__main__":
    # Create and display the grid
    grid = Grid()
    grid.show()
