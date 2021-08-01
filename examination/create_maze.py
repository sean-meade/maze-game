    def create_maze(self):
        no_of_rows = self.nx
        no_of_cols = self.ny

        html = ''

        for y in range(no_of_cols):
            border = ''
            for x in range(no_of_rows):
                if self.maze_map[x][y].walls['N']:
                    border = '1'
                else:
                    border = '0'
                
                if self.maze_map[x][y].walls['E']:
                    border += ' 1'
                else:
                    border += ' 0'

                if self.maze_map[x][y].walls['S']:
                    border += ' 1'
                else:
                    border += ' 0'

                if self.maze_map[x][y].walls['W']:
                    border += ' 1'
                else:
                    border += ' 0'
                
                div = '<div style="border-width: ' + border + '></div>'

                html += div
