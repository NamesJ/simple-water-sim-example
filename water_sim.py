import time
from datetime import datetime


class Terrain:
    def __init__(self, init_water_state, flow_rate=0.5):
        self.cells = init_water_state # mxn matrix
        self.flow_rate = flow_rate
        self.total_water = self._total_water()
        self.adjuster_cell = (None, None)
        for rix in range(len(self.cells)):
            for cix in range(len(self.cells[0])):
                if type(self.cells[rix][cix]) in {float, int}:
                    self.adjuster_cell = (rix, cix)
                    break
            if self.adjuster_cell != (None, None):
                break
        
    def _neighbors(self, rix, cix):
        neighbors = []
        if rix != 0:
            neighbors.append(((rix-1, cix), self.cells[rix-1][cix]))
            if cix != 0:
                neighbors.append(((rix-1, cix-1), self.cells[rix-1][cix-1]))
                neighbors.append(((rix, cix-1), self.cells[rix][cix-1]))
            if cix != len(self.cells[0])-1:
                neighbors.append(((rix-1, cix+1), self.cells[rix-1][cix+1]))
                neighbors.append(((rix, cix+1), self.cells[rix][cix+1]))
        if rix != len(self.cells) - 1:
            neighbors.append(((rix+1, cix), self.cells[rix+1][cix]))
            if cix != 0:
                neighbors.append(((rix+1, cix-1), self.cells[rix+1][cix-1]))
                neighbors.append(((rix, cix-1), self.cells[rix][cix-1]))
            if cix != len(self.cells[0])-1:
                neighbors.append(((rix+1, cix+1), self.cells[rix+1][cix+1]))
                neighbors.append(((rix, cix+1), self.cells[rix][cix+1]))
        return neighbors

    def _total_water(self):
        total= 0
        for row in self.cells:
            for cell in row:
                if type(cell) in {float, int}:
                    total += cell
        return total
                
    def step(self, d_time):
        cells_new = [[0 for cell in range(len(self.cells[0]))] for rix in range(len(self.cells))]
        for rix, row in enumerate(self.cells):
            for cix, cell in enumerate(row):
                if type(cell) not in {float, int}: # non-water cell
                    continue
                if cell < 0: # no water to distribute
                    continue
                cell_new = cell
                neighbors = self._neighbors(rix, cix)
                n_num_water = len([type(n) in {float, int} for n in neighbors])
                for (n_rix, n_cix), n in neighbors:
                    if type(n) not in {float, int}: # non-water cell
                        continue
                    if n < cell:
                        flow_rate = self.flow_rate# / n_num_water
                        #d_water = (cell_new - n) * flow_rate * d_time
                        d_water = cell_new * flow_rate * d_time
                        #n += d_water
                        cells_new[n_rix][n_cix] += d_water
                        cells_new[rix][cix] -= d_water
                        #cell_new -= d_water
                        #self.cells[n_rix][n_cix] = n
                #self.cells[rix][cix] = cell_new
        for rix, row in enumerate(self.cells):
            for cix, cell in enumerate(row):
                if type(cell) not in {float, int}:
                    continue
                self.cells[rix][cix] = cell + cells_new[rix][cix]
        if self._total_water() != self.total_water:
            adj_rix, adj_cix = self.adjuster_cell
            self.cells[adj_rix][adj_cix] += self.total_water - self._total_water()
            
                
    def __str__(self):
        s = ''
        for row in self.cells:
            for cell in row:
                s += '|{:2.1f}'.format(cell) if type(cell) in {float, int} else f'|{cell:>3}'
            s += '|\n'
        return s
    
    def draw(self):
        print(self.__str__())


def main():
    fps = 5
    step_interval = 1 / fps
    frames = 0
    last_frame_dt = datetime.now()
    
    terrain = Terrain([
        [ 0,   0,   0,   0,  0],
        [ 0,  'x', 'x', 'x', 0],
        [ 0,   0,   0,  'x', 0],
        ['x', 'x',  0,  'x', 0],
        [ 34,   0,   0,  'x', 0]
    ], flow_rate=0.5)

    while True:
        curr_frame_dt = datetime.now()
        dt = (curr_frame_dt - last_frame_dt).total_seconds()
        terrain.step(dt)
        print('\nFrame #{} | Water: {}'.format(frames, terrain._total_water()))
        terrain.draw()
        last_frame_dt = curr_frame_dt
        frames += 1
        time.sleep(step_interval)


if __name__ == '__main__':
    main()
