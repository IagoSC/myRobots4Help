from functools import reduce
from math import sqrt


def reg1(): return [
    ('robo1', 1, (5, 8), 4),
    ('robo2', 2, (5, 4), 4),
    ('robo3', 3, (2, 2), 1),
    ('robo1', 4, (4, 9), 4),
    ('robo3', 5, (1, 3), 3),
    ('robo4', 6, (7, 5), 3),
    ('robo5', 7, (8, 6), 1),
    ('robo1', 8, (3, 2), 4),
    ('robo2', 9, (1, 8), 4)
]

# Dada uma lista de reg retorna todos os robos identificados na lista
def getAllRobotsIds(reg):
    seen = set()
    return [info[0] for info in reg if not info[0] in seen and not seen.add(info[0])]


# Aplica a função a cada info do robo selecionado e retorna um array
def mapSelectedRobot(function, robotId, reg):
    return [function(info) for info in reg if info[0] == robotId]


# Recebe a lista reg e um id de robo e retorna uma lista de todas as infos daquele robo
def filterSelectedRobot(robotId, reg):
    return [info for info in reg if info[0] == robotId]


# Recebe uma lista formato reg e transforma em uma lista de apenas uma das infos
def filterInfoIndex(reg, index):
    return map(lambda info: info[index], reg)


# Recebe entrada e divide em array de robos contendo array de infos
# Decidimos deixar o robotsList como parâmetro para possivel reutilização da função para separar subconjuntos do total de robôs
def separateRobots(robotsList, reg):
    return list(map(lambda robotId: (robotId, filterSelectedRobot(robotId, reg)), robotsList))


# Dado dois pontos euclidianos no formato (x, y) calcula a distancia
def calculateEuclidanDistance(currentPosition, newPosition):
    print(currentPosition, newPosition)
    return sqrt((currentPosition[0] - newPosition[0])**2 + (currentPosition[1] - newPosition[1])**2)


# Calcula a distancia percorrida total e a utima posição
def calculatePathDistance(reg):
    # currentPos = (distance, (positionX, postionY), path)
    return reduce(lambda currentPos, newPos:  (
        currentPos[0] + calculateEuclidanDistance(currentPos[1], newPos), newPos), reg, (0, (0, 0)))


# Return path of the robot including step 0
def getPath(reg):
    return [step[2] for step in reg]


# Return from list the element which has the max value of given index
def getMaxFromIndex(reg, index):
    return max(reg, key=lambda info: info[index])



def distaciaPercorridaRobo(robotId, reg):
    return calculatePathDistance(
        filterInfoIndex(
            filterSelectedRobot(robotId, reg), 2
        )
    )[0]


# Receives a reducerFunction and an initial value to operate a reduce in a given index of the elements of the array
# Returns (id, reducedValue)
# initial = (id, initialValue)
def reduceIndex(function, index, reg, initialValue):
    return reduce(lambda current, new: function(current, new[index]), reg, initialValue)

def caminhosRobos(reg):
    return sorted(
        list(
          map(
            lambda robotInfos: (
                robotInfos[0],
                distaciaPercorridaRobo(robotInfos[0], robotInfos[1]),
                getPath(robotInfos[1])
            ), separateRobots(getAllRobotsIds(reg), reg)
          )
        ),
        key= lambda tuple: tuple
        )


def roboIdentifcaMaisVitimas(reg):
    return getMaxFromIndex(
        map( 
          # robotInfos = (robotId, registers)
          lambda robotInfos: (robotInfos[0], reduceIndex(lambda current, new: current + new, 1, robotInfos[1],  0)), 
          separateRobots(getAllRobotsIds(reg), reg)
        )
      , 1
    )[0]

def roboMaiorFinalOrigem(reg):
    return getMaxFromIndex(
      map(
        lambda robotInfos: (
          robotInfos[0],
          calculateEuclidanDistance(robotInfos[1][-1][2], (0,0)),
          getPath(robotInfos[1])
        ),
        separateRobots(getAllRobotsIds(reg), reg),
      ),  
      1      
    )
