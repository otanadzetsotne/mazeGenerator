import numpy as np
from random import choice
from tkinter import *


class MazeGenerator:
    modes = ['basic', 'improved']
    measurements = [2, 3]

    def __init__(self):
        self.visualize = False
        self.mode = 'improved'
        self.measurement = 2
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

    def set_measurement(self, measurement: int):
        if measurement in self.measurements:
            self.measurement = measurement
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
        if self.measurement == 2:
            return self.generate_2d()
        elif self.measurement == 3:
            return self.generate_3d()

    def generate_3d(self):
        self.maze = np.zeros((self.size, self.size, self.size), int)
        coordinates = [i for i in range(1, self.size, 2)]
        unvisited_cells = list()
        for z in coordinates:
            for y in coordinates:
                for x in coordinates:
                    unvisited_cells.append([z, y, x])
                    self.maze[z, y, x] = 1

        cur_cell = [1, 1, 1]
        visited_cells = list()
        path_stack = list()
        visited_cells.append(cur_cell)
        unvisited_cells.remove(cur_cell)

        while unvisited_cells:
            unvisited_neighbors = list()

            if cur_cell[0] != 1:
                neighbor_up = [cur_cell[0] - 2, cur_cell[1], cur_cell[2]]
                if not visited_cells.count(neighbor_up):
                    unvisited_neighbors.append(neighbor_up)

            if cur_cell[0] != self.size - 2:
                neighbor_down = [cur_cell[0] + 2, cur_cell[1], cur_cell[2]]
                if not visited_cells.count(neighbor_down):
                    unvisited_neighbors.append(neighbor_down)

            if cur_cell[1] != 1:
                neighbor_north = [cur_cell[0], cur_cell[1] - 2, cur_cell[2]]
                if not visited_cells.count(neighbor_north):
                    unvisited_neighbors.append(neighbor_north)

            if cur_cell[1] != self.size - 2:
                neighbor_south = [cur_cell[0], cur_cell[1] + 2, cur_cell[2]]
                if not visited_cells.count(neighbor_south):
                    unvisited_neighbors.append(neighbor_south)

            if cur_cell[2] != 1:
                neighbor_west = [cur_cell[0], cur_cell[1], cur_cell[2] - 2]
                if not visited_cells.count(neighbor_west):
                    unvisited_neighbors.append(neighbor_west)

            if cur_cell[2] != self.size - 2:
                neighbor_east = [cur_cell[0], cur_cell[1], cur_cell[2] + 2]
                if not visited_cells.count(neighbor_east):
                    unvisited_neighbors.append(neighbor_east)

            if len(unvisited_neighbors):
                if self.mode == 'improved' and len(unvisited_neighbors) > 1:
                    path_stack.append(cur_cell.copy())
                elif self.mode == 'basic':
                    path_stack.append(cur_cell.copy())

                next_cell = choice(unvisited_neighbors)
                wall_z = (cur_cell[0] + next_cell[0]) // 2
                wall_y = (cur_cell[1] + next_cell[1]) // 2
                wall_x = (cur_cell[2] + next_cell[2]) // 2
                self.maze[wall_z, wall_y, wall_x] = 1

                cur_cell = next_cell.copy()
            elif len(visited_cells):
                cur_cell = path_stack.pop()
            else:
                print('Jesus Christ it\'s recursion!')
                exit()

            if not visited_cells.count(cur_cell):
                visited_cells.append(cur_cell.copy())

            if unvisited_cells.count(cur_cell):
                unvisited_cells.remove(cur_cell)

        return self.maze

    def generate_2d(self):
        self.maze = np.zeros((self.size, self.size), int)
        coordinates = [i for i in range(1, self.size, 2)]
        unvisited_cells = list()
        for x in coordinates:
            for y in coordinates:
                unvisited_cells.append([x, y])
                self.maze[x, y] = 1
                self.set_cell_color_white([x, y])

        self.create_canvas_background()
        self.update_window()

        cur_cell = [1, 1]
        visited_cells = list()
        path_stack = list()
        visited_cells.append(cur_cell)
        unvisited_cells.remove(cur_cell)

        while unvisited_cells:
            unvisited_neighbors = list()

            if cur_cell[0] != 1:
                up_neighbor = [cur_cell[0] - 2, cur_cell[1]]
                if not visited_cells.count(up_neighbor):
                    unvisited_neighbors.append(up_neighbor)

            if cur_cell[1] != 1:
                left_neighbor = [cur_cell[0], cur_cell[1] - 2]
                if not visited_cells.count(left_neighbor):
                    unvisited_neighbors.append(left_neighbor)

            if cur_cell[0] != self.size - 2:
                down_neighbor = [cur_cell[0] + 2, cur_cell[1]]
                if not visited_cells.count(down_neighbor):
                    unvisited_neighbors.append(down_neighbor)

            if cur_cell[1] != self.size - 2:
                right_neighbor = [cur_cell[0], cur_cell[1] + 2]
                if not visited_cells.count(right_neighbor):
                    unvisited_neighbors.append(right_neighbor)

            if len(unvisited_neighbors):
                if self.mode == 'improved' and len(unvisited_neighbors) > 1:
                    path_stack.append(cur_cell.copy())
                elif self.mode == 'basic':
                    path_stack.append(cur_cell.copy())

                next_cell = choice(unvisited_neighbors)
                wall_x = (cur_cell[0] + next_cell[0]) // 2
                wall_y = (cur_cell[1] + next_cell[1]) // 2
                self.maze[wall_x, wall_y] = 1

                self.set_cell_color_white(cur_cell)
                self.set_cell_color_white([wall_x, wall_y])
                cur_cell = next_cell.copy()
            elif len(visited_cells):
                self.set_cell_color_white(cur_cell)
                cur_cell = path_stack.pop()
                self.set_cell_color_active(cur_cell)
            else:
                print('Jesus Christ it\'s recursion!')
                exit()

            self.set_cell_color_active(cur_cell)

            if not visited_cells.count(cur_cell):
                visited_cells.append(cur_cell.copy())

            if unvisited_cells.count(cur_cell):
                unvisited_cells.remove(cur_cell)

            self.update_window()

        self.mainloop()
        return self.maze

    def set_cell_color_active(self, cell: list):
        return self.set_cell_color(cell, 'red')

    def set_cell_color_white(self, cell: list):
        return self.set_cell_color(cell, '#fff')

    def set_cell_color(self, cell: list, color: str):
        if self.visualize and self.canvas:
            x = cell[0] * self.ratio
            y = cell[1] * self.ratio
            self.canvas.create_rectangle(x, y, x + self.ratio, y + self.ratio, fill=color, outline=color)
            return True
        else:
            return False

    def create_canvas_background(self):
        if self.visualize and self.canvas:
            border_space = self.window_size
            self.canvas.create_rectangle(0, 0, border_space, border_space, fill='#000', outline='#000')
            return True
        else:
            return False

    def update_window(self):
        if self.visualize and self.window:
            self.window.update()
            return True
        else:
            return False

    def mainloop(self):
        if self.visualize and self.window:
            self.window.mainloop()
            return True
        else:
            return False


if __name__ == '__main__':
    maze = MazeGenerator()
    maze.set_size(200)
    maze.set_visualize(window_size=900)
    maze.generate()
