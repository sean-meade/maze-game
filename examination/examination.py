import random

class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, south, east or west.
    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    # Pairs a side of one cell to the side of the otehr cell.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def __repr__(self): 
        sentence = f'({self.x}, {self.y}), {self.walls}'
        return sentence
    
    def __str__(self): 
        sentence = f'({self.x}, {self.y}), {self.walls}'
        return sentence2

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        # Uses wall pairs (above) to set the wall of the neighbour cell to false
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]
        

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""
        
        return self.maze_map[x][y]

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows) + '\n' + f'{self.maze_map}'

    def create_maze(self):
        no_of_rows = self.nx
        no_of_cols = self.ny

        body = '<div class="container">'
            
        for y in range(no_of_cols):
            border = ''
            row = '<div class="row">'
            for x in range(no_of_rows):
                if self.maze_map[x][y].walls['N']:
                    border = 'border-top'
                else:
                    border = 'border-top-0'
                
                if self.maze_map[x][y].walls['E']:
                    border += ' border-right'
                else:
                    border += ' border-right-0'

                if self.maze_map[x][y].walls['S']:
                    border += ' border-bottom'
                else:
                    border += ' border-bottom-0'

                if self.maze_map[x][y].walls['W']:
                    border += ' border-left'
                else:
                    border += ' border-left-0'
                
                div = '<div class="col ' + border + '"></div>'

                row += div

            body = body + row + '</div>'

        body += '</div>'

        html = """
        <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Document</title>
                    <link
                        rel="stylesheet"
                        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                        crossorigin="anonymous"
                    />
                    <style>
                        body {
                            background: red;
                            padding: 0 !important;
                            margin: 0 !important;
                        }
                        .col {
                            border-color: black;
                            height: 40px;
                            background-color: blue;
                            padding: 0 !important;
                            margin: 0 !important;
                        }
                    </style>
                </head>
                <body>
        """ + body + "</body></html>"
        
        Html_file= open("index.html","w")
        Html_file.write(html)
        Html_file.close()

        return print('success?')

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1