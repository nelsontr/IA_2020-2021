# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 05:
# 93695 Catarina Sousa
# 93743 Nelson Trindade

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search, iterative_deepening_search
import sys
from copy import deepcopy
#import time

class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """

    def __init__(self, dim: int, robots: dict, barriers_pos: dict, objective: list):
        self.robots = robots
        self.dimensions = dim
        self.barriers_pos = barriers_pos
        self.objective = objective

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        return self.robots[robot]

    def check_barriers(self, x: int, y: int, posi: str) -> bool:
        return (str([x, y]) not in self.barriers_pos.keys() or
                posi not in self.barriers_pos[str([x, y])])

    def checkBounderiesRobot(self, robot: str, term: str)-> bool:
        x, y = self.robots[robot]  # position of robot

        if term=="u":
            return x!=1 and ([x-1,y] not in self.robots.values()) and \
            self.check_barriers(x-1,y,"d") and self.check_barriers(x,y,"u")
        elif term=="d":
            return x!=self.dimensions and ([x+1,y] not in self.robots.values())\
            and self.check_barriers(x+1,y,"u") and self.check_barriers(x,y,"d")
        elif term=="l":
            return y!=1 and ([x,y-1] not in self.robots.values()) and \
            self.check_barriers(x,y-1,"r") and self.check_barriers(x,y,"l")
        elif term=="r":
            return y!=self.dimensions and ([x,y+1] not in self.robots.values())\
            and self.check_barriers(x,y+1,"l") and self.check_barriers(x,y,"r")



    def check_boundaries(self) -> list:
        result = []
        for color in ("R", "G", "B", "Y"):
            if self.checkBounderiesRobot(color, "u"):
                result.append((color, "u"))
            if self.checkBounderiesRobot(color, "d"):
                result.append((color, "d"))
            if self.checkBounderiesRobot(color, "l"):
                result.append((color, "l"))
            if self.checkBounderiesRobot(color, "r"):
                result.append((color, "r"))
        return result

    def move(self, action: tuple):
        while(self.checkBounderiesRobot(action[0], action[1])):
            if action[1] == 'l':
                self.robots[action[0]][1] -= 1
            elif action[1] == 'r':
                self.robots[action[0]][1] += 1
            elif action[1] == 'u':
                self.robots[action[0]][0] -= 1
            elif action[1] == 'd':
                self.robots[action[0]][0] += 1

    def check_if_objective(self, board):
        return self.objective[1] == board.robots[self.objective[0]][0] \
            and self.objective[2] == board.robots[self.objective[0]][1]



def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    with open(filename, "r") as file1:
        dim = int(file1.readline()[:-1])
        robots = {}

        for i in range(0, 4):
            aux = file1.readline()[:-1].split(" ")
            robots[aux[0]] = [int(aux[1]), int(aux[2])]

        obj = file1.readline()[:-1].split(" ")
        obj[1], obj[2] = int(obj[1]), int(obj[2])

        barriers = int(file1.readline()[:-1])
        barriers_pos = {}
        for i in range(0, barriers):
            aux = file1.readline()[:-1].split(" ")
            if str([int(aux[0]), int(aux[1])]) not in barriers_pos:
                barriers_pos[str([int(aux[0]), int(aux[1])])] = []
            barriers_pos[str([int(aux[0]), int(aux[1])])].append(aux[2])

    return Board(dim, robots, barriers_pos, obj)


class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = RRState(board)

    def actions(self, state: RRState) -> list:
        return state.board.check_boundaries()

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """

        if state.board.checkBounderiesRobot(action[0], action[1]):
            board2 = Board(state.board.dimensions, deepcopy(state.board.robots), state.board.barriers_pos, state.board.objective)
            state2 = RRState(board2)
            state2.board.move(action)
            return state2
        return state

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        return state.board.check_if_objective(state.board)

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        objective = node.state.board.objective
        robot = node.state.board.robot_position(objective[0])
        dx = abs(robot[0] - objective[1])
        dy = abs(robot[1] - objective[2])
        return (dx + dy)


if __name__ == "__main__":

    #start_time = time.time()

    board = parse_instance(sys.argv[1])
    problem = RicochetRobots(board)

    #solution = astar_search(problem)
    solution = iterative_deepening_search(problem)

    print(len(solution.solution()))
    for i in solution.solution():
        print(i[0], i[1])
    #print("--- %s seconds ---" % (time.time() - start_time))
