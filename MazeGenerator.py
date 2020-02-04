import numpy as np
from random import choice
from tkinter import *


class MazeGenerator:
    modes = ['basic', 'improved']

    def __init__(self):
        self.visualize = False
        self.mode = 'improved'
        self.dimension = 2
        self.window = None
        self.canvas = None
        self.window_size = None
        self.maze = None
        self.ratio = None
        self.size = None
        self.set_size(10)

    def set_size(self, size: int):
        size += 1 if (size % 2 == 0) else 0
        self.size = size
        return True

    def set_mode(self, mode: str):
        if mode in self.modes:
            self.mode = mode
            return True
        else:
            return False

    def set_dimension(self, dimension: int):
        if 2 <= dimension <= 4:
            self.dimension = dimension
            return True
        else:
            return False

    def set_visualize(self, vis: bool = True, window_size: int = 1000):
        self.visualize = vis
        if vis:
            self.ratio = window_size // self.size
            window_size = self.size * self.ratio
            self.window_size = window_size
            self.window = Tk()
            self.canvas = Canvas(self.window, width=window_size, height=window_size)
            self.canvas.pack()
        return True

    def generate(self):
        return self.generate_maze()

    def generate_maze(self):
        d = self.dimension
        self.maze = np.zeros([self.size for i in range(d)], int)
        unvisited_cells = self.create_unvisited_cells()

        # just for 2 dimensions
        self.create_canvas_background()
        self.update_window()

        cur_cell = [1 for i in range(d)]
        visited_cells = list()
        path_stack = list()
        visited_cells.append(cur_cell)
        unvisited_cells.remove(cur_cell)

        while unvisited_cells:
            unvisited_neighbors = list()
            for i in range(d):
                if cur_cell[i] != 1:
                    neighbor_cell = cur_cell.copy()
                    neighbor_cell[i] = neighbor_cell[i] - 2
                    if not visited_cells.count(neighbor_cell):
                        unvisited_neighbors.append(neighbor_cell.copy())
                if cur_cell[i] != self.size - 2:
                    neighbor_cell = cur_cell.copy()
                    neighbor_cell[i] = neighbor_cell[i] + 2
                    if not visited_cells.count(neighbor_cell):
                        unvisited_neighbors.append(neighbor_cell.copy())

            if len(unvisited_neighbors):
                if self.mode == 'improved' and len(unvisited_neighbors) > 1:
                    path_stack.append(cur_cell.copy())
                elif self.mode == 'basic':
                    path_stack.append(cur_cell.copy())

                next_cell = choice(unvisited_neighbors)
                wall = [(cur_cell[i] + next_cell[i]) // 2 for i in range(d)]
                if d == 2:
                    self.maze[wall[0], wall[1]] = 1
                    self.set_cell_color_white(cur_cell)
                    self.set_cell_color_white([wall[0], wall[1]])
                if d == 3:
                    self.maze[wall[0], wall[1], wall[2]] = 1
                if d == 4:
                    self.maze[wall[0], wall[1], wall[2], wall[3]] = 1
                cur_cell = next_cell.copy()
            elif len(visited_cells):
                # works just for 2 dimensions
                self.set_cell_color_white(cur_cell)

                cur_cell = path_stack.pop()

                # works just for 2 dimensions
                self.set_cell_color_active(cur_cell)
            else:
                print('Jesus Christ it\'s recursion!')
                exit()

            # works just for 2 dimensions
            self.set_cell_color_active(cur_cell)

            if not visited_cells.count(cur_cell):
                visited_cells.append(cur_cell.copy())
            if unvisited_cells.count(cur_cell):
                unvisited_cells.remove(cur_cell)

            # works just for 2 dimensions
            self.update_window()

        # works just for 2 dimensions
        self.mainloop()
        return self.maze

    def create_unvisited_cells(self):
        unvisited_cells = list()
        coordinates = [i for i in range(1, self.size, 2)]
        if self.dimension == 2:
            for y in coordinates:
                for x in coordinates:
                    unvisited_cells.append([y, x])
                    self.maze[y, x] = 1
                    self.set_cell_color_white([y, x])
        elif self.dimension == 3:
            for z in coordinates:
                for y in coordinates:
                    for x in coordinates:
                        unvisited_cells.append([z, y, x])
                        self.maze[z, y, x] = 1
        elif self.dimension == 4:
            for d in coordinates:
                for z in coordinates:
                    for y in coordinates:
                        for x in coordinates:
                            unvisited_cells.append([d, z, y, x])
                            self.maze[d, z, y, x] = 1

        return unvisited_cells

    def set_cell_color_active(self, cell: list):
        return self.set_cell_color(cell, 'red')

    def set_cell_color_white(self, cell: list):
        return self.set_cell_color(cell, '#fff')

    def set_cell_color(self, cell: list, color: str):
        if self.visualize and self.canvas and self.dimension == 2:
            x = cell[0] * self.ratio
            y = cell[1] * self.ratio
            self.canvas.create_rectangle(x, y, x + self.ratio, y + self.ratio, fill=color, outline=color)
            return True
        else:
            return False

    def create_canvas_background(self):
        if self.visualize and self.canvas and self.dimension == 2:
            border_space = self.window_size
            self.canvas.create_rectangle(0, 0, border_space, border_space, fill='#000', outline='#000')
            return True
        else:
            return False

    def update_window(self):
        if self.visualize and self.window and self.dimension == 2:
            self.window.update()
            return True
        else:
            return False

    def mainloop(self):
        if self.visualize and self.window and self.dimension == 2:
            self.window.mainloop()
            return True
        else:
            return False


if __name__ == '__main__':
    maze = MazeGenerator()
    maze.set_size(200)
    maze.set_visualize(window_size=900)
    maze.generate()
