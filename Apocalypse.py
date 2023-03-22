"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """

    poc_grid.Grid.__init__(self, grid_height, grid_width)
    self._obstacle_list = []
    if obstacle_list != None:
        self._obstacle_list = obstacle_list
        for cell in obstacle_list:
            self.set_full(cell[0], cell[1])
    if zombie_list != None:
        self._zombie_list = list(zombie_list)
    else:
        self._zombie_list = []
    if human_list != None:
        self._human_list = list(human_list)
    else:
        self._human_list = []


def clear(self):
    """
    Set cells in obstacle grid to be empty
    Reset zombie and human lists to be empty
    """
    poc_grid.Grid.clear()
    self._zombie_list = []
    self._human_list = []
    poc_grid.Grid.clear(self)


def add_zombie(self, row, col):
    """
    Add zombie to the zombie list
    """
    self._zombie_list.append((row, col))


def num_zombies(self):
    """
    Return number of zombies
    """
    return len(self._zombie_list)


def zombies(self):
    """
    Generator that yields the zombies in the order they were
    added.
    """
    # replace with an actual generator
    for zombie in self._zombie_list:
        yield zombie


def add_human(self, row, col):
    """
    Add human to the human list
    """
    self._human_list.append((row, col))


def num_humans(self):
    """
    Return number of humans
    """
    return len(self._human_list)


def humans(self):
    """
    Generator that yields the humans in the order they were added.
    """
    # replace with an actual generator
    for human in self._human_list:
        yield human


def obstacle(self):
    '''
    Generate that yields the list of obstacles.
    '''
    for obstacle in self._obstacle_list:
        yield obstacle


def compute_distance_field(self, entity_type):
    """
    Function computes and returns a 2D distance field
    Distance at member of entity_list is zero
    Shortest paths avoid obstacles and use four-way distances
    """
    height = self._grid_height
    width = self._grid_width

    # create a grid visited that is initialized to all empty
    visited = poc_grid.Grid(height, width)

    # place all the obstacles to the visited grid
    for obstacle in self.obstacle():
        visited.set_full(obstacle[0], obstacle[1])

    # initialize distance field so that all the cells contain the product of its height and width
    distance_field = [[dummy_row * dummy_col for dummy_col in range(width)] for dummy_row in range(height)]

    # create a boundary queue which contains a copy of the list of the entity type
    boundary = poc_queue.Queue()

    if entity_type == ZOMBIE:
        list_type = self._zombie_list
    else:
        list_type = self._human_list

    for cells in list_type:
        boundary.enqueue(cells)
        visited.set_full(cells[0], cells[1])
        distance_field[cells[0]][cells[1]] = 0
    # based on breadth-first search
    while boundary:
        current_cell = boundary.dequeue()
        neighbour_cell = visited.four_neighbours(current_cells[0], current_cells[1])

        # traverse for all neighbours of current cell to calculate the distance
        for cell in neighbour_cell:
            if visited.is_empty(cell[0], cell[1]):
                visited.set_full(cell[0], cell[1])
                boundary.enqueue(cell)
                distance_field[cell[0]][cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
    return distance_field


def move_humans(self, zombie_distance_field):
    """
    Function that moves humans away from zombies, diagonal moves
    are allowed
    """
    human_list = []
    for humans in self._human_list:
        max_list = []

        # traverse all neighbours of the current human
        neighbours = self.eight_neighbours(humans[0], humans[1])
        neighbours.append(humans)

        for cell in neighbours:
            if not self.is_empty(cell[0], cell[1]):
                continue
            if len(max_list) == 0:
                max_list.append(cell)
            elif zombie_distance_field[cell[0]][cell[1]] == zombie_distance_field[max_list[0][0]][max_list[0][1]]:
                max_list.append(cell)

            elif zombie_distance_field[cell[0]][cell[1]] > zombie_distance_field[max_list[0][0]][max_list[0][1]]:
                max_list = [cell]
        human_list.append(random.choice(max_list))
    self._human_list = human_list


def move_zombies(self, human_distance_field):
    """
    Function that moves zombies towards humans, no diagonal moves
    are allowed
    """
    zombie_list = []
    for zombie in self._zombie_list:
        min_list = []
        # get the list of 4 neighbours of the zombie
        neighbours = self.four_neighbours(zombie[0], zombie[1])

        # append zombie to the neighbour list
        for cell in neighbours:
            # if current neighbour is occupied, then skip to the next cell. And if the cell is an obstacle, then also skip to next cell.
            if not self.is_empty(cell[0], cell[1]):
                continue
            if len(min_list) == 0:
                min_list.append(cell)
            elif human_distance_field[cell[0]][cell[1]] == human_distance_field[min_list[0][0]][min_list[0][1]]:
                min_list.append(cell)
            elif human_distance_field[cell[0]][cell[1]] < human_distance_field[min_list[0][0]][min_list[0][1]]:
                min_list = [cell]
        zombie_list.append(random.choice(min_list))

    self._zombie_list = zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))
