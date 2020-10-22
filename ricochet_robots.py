# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 05:
# 93695 Catarina Sousa
# 93743 Nelson Trindade

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys


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

    def check_boundaries(self) -> list:
        result = []
        for color in self.robots:
            x, y = self.robots[color]  # position of robot

            # board walls and robots
            # barriers
            u = (x-1) >= 1 and [(x-1), y] not in self.robots.values() \
                and self.check_barriers(x-1, y, "d") and self.check_barriers(x, y, "u")
            d = (x+1) <= self.dimensions and [(x+1), y] not in self.robots.values()\
                and self.check_barriers(x+1, y, "u") and self.check_barriers(x, y, "d")
            l = (y-1) >= 1 and [x, (y-1)] not in self.robots.values()\
                and self.check_barriers(x, y-1, "r") and self.check_barriers(x, y, "l")
            r = (y+1) <= self.dimensions and [x, (y+1)] not in self.robots.values()\
                and self.check_barriers(x, y+1, "l") and self.check_barriers(x, y, "r")

            # append result
            if u:
                result.append((color, "u"))
            if d:
                result.append((color, "d"))
            if l:
                result.append((color, "l"))
            if r:
                result.append((color, "r"))

        return result

    def move(self, action: tuple):
        while(self.check_bounder(action)):
            if action[1] == 'l':
                self.robots[action[0]][1] -= 1
            if action[1] == 'r':
                self.robots[action[0]][1] += 1
            if action[1] == 'u':
                self.robots[action[0]][0] -= 1
            if action[1] == 'd':
                self.robots[action[0]][0] += 1

    def check_bounder(self, action: tuple) -> bool:
        return action in self.check_boundaries()

    def check_if_objective(self, board):
        return board == objective
    # TODO: outros metodos da classe


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
        obj[0], obj[1], obj[2] = str(obj[0]), int(obj[1]), int(obj[2])

        barriers = int(file1.readline()[:-1])
        barriers_pos = {}
        for i in range(0, barriers):
            aux = file1.readline()[:-1].split(" ")
            if str([int(aux[0]), int(aux[1])]) in barriers_pos:
                barriers_pos[str([int(aux[0]), int(aux[1])])].append(aux[2])
            else:
                barriers_pos[str([int(aux[0]), int(aux[1])])] = [aux[2]]
    return Board(dim, robots, barriers_pos, obj)


class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = board

    def actions(self, state: RRState) -> list:
        return state.board.check_boundaries()

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        if action in self.actions(state):
            return state.board.move(action)
        return state

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        return state.board.check_if_objective(state.board)

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        color = node.state.board.objective[0]
        robot = node.state.board.robot_position(color)
        dx = abs(robot[0] - goal[0])  #TODO
        dy = abs(robot[1] - goal[1])
        return (dx + dy)


if __name__ == "__main__":
    board = parse_instance(sys.argv[1])
    problem = RicochetRobots(board)
    solution = astar_search(problem)
    print(len(solution.solution()))
    for i in solution:
        print(i[0], " ", i[1])
    # TODO:
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
