from ConsoleEngine import *
import random
import math
from time import sleep

class Rewards:
    def __init__(self):
        self.win = 1000
        self.loose = -1000
        


x = int(input('X: '))
y = int(input('Y: '))
o = int(input('Obstacles: '))
LR = float(input('LR: '))
DF = float(input('DF: '))
size = [x,y]
NOBSTACLES = o
forbidden = []

for y in range(0,4):
    for x in range(0,4):
        forbidden.append([x,y])

obstacles = []
i = 0
while i != NOBSTACLES:
    pos = [random.randint(0,size[1]-1),random.randint(0,size[1]-1)]
    if pos in obstacles or pos in forbidden:
        continue
    obstacles.append(pos)
    i += 1

del forbidden
del i

pr = True
while pr:
    win_position = [random.randint(0,size[1]-1),random.randint(0,size[1]-1)]
    if win_position not in obstacles:
        pr = False

rewards = Rewards()
wnd = WorkArea(size,'#')
scene = Scene(size,' ')

def length(pos1,pos2):
    return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

def logic(agent):
    global rewards

    if agent.position in obstacles:
        return rewards.loose
    elif agent.position == win_position:
        return rewards.win
    elif agent.position[0] >size[0]-1 or agent.position[1] >size[1]-1 or agent.position[0] <0 or  agent.position[1] <0:
        return rewards.loose
    else:
        return (length(agent.prev_position,win_position) - length(agent.position,win_position))

class Agent:
    def __init__(self,position,speed,graphic:GraphicObject):
        global LR, DF
        self.prev_position = position
        self.position = position
        self.speed = speed
        self.graphic = graphic
        self.qmatrix = []
        self.LR = LR
        self.DF = DF
        self.moves = 0

    def move(self,movement:int):
        self.moves += 1
        self.prev_position = self.position.copy()
        if movement == 0:
            self.position[1] += -self.speed
        elif movement == 1:
            self.position[0] += self.speed
        elif movement == 2:
            self.position[1] += self.speed
        elif movement == 3:
            self.position[0] += -self.speed
    
    def raw_qmatrix_init(self,obstacles,destination):
        buf = []
        for row in obstacles:
            for element in row:
                buf.append(element)
        buf.append(destination[0])
        buf.append(destination[1])
        buf.append(0)
        buf.append(0)
        self.raw_qmatrix = buf
        
    def init_qmatrix(self,size):
        for x in range(size[0]):
            for y in range(size[1]):
                self.raw_qmatrix[len(self.raw_qmatrix)-1] = x
                self.raw_qmatrix[len(self.raw_qmatrix)-2] = y
                self.qmatrix.append(self.raw_qmatrix.copy())
                self.qmatrix.append([random.random(),random.random(),random.random(),random.random()])
                
    def get_value(self,predict = True):
        
        self.raw_qmatrix[len(self.raw_qmatrix)-1] = self.prev_position[0]
        self.raw_qmatrix[len(self.raw_qmatrix)-2] = self.prev_position[1]
        if predict:
            index = self.qmatrix.index(self.raw_qmatrix)+1
            self.prev_index = index
            self.prev_qvalue = max(self.qmatrix[index])
            return self.qmatrix[index].index(self.prev_qvalue)
        else:
            index = self.qmatrix.index(self.raw_qmatrix)+1
            return max(self.qmatrix[index])

    def update_qtable(self,reward):
        next_qvalue = self.get_value(False)
        delta = self.LR*(reward + self.DF*next_qvalue - self.prev_qvalue)
        index = self.qmatrix[self.prev_index].index(max(self.qmatrix[self.prev_index]))
        self.qmatrix[self.prev_index][index] += delta


player_graphic = GraphicObject([1,1],"@")
obstacle_graphic = GraphicObject([1,1],"-")
win_graphic = GraphicObject([1,1],"+")
bot = Agent([0,0],1,player_graphic)

bot.raw_qmatrix_init(obstacles,win_position)
bot.init_qmatrix(size)

def prep_scene():
    global scene
    scene.init_scene()
    scene.write_object(bot.position,bot.graphic)
    scene.write_object(win_position,win_graphic)
    for obst in obstacles:
        scene.write_object(obst,obstacle_graphic)

won = True
def main():
    global won
    alive = True
    while alive:        
        prep_scene()
       
        prediction = bot.get_value()
        bot.move(prediction)
        reward = logic(bot)
        if reward == rewards.loose :
            alive = False
        elif reward == rewards.win:
            alive = False
            won = False
        bot.update_qtable(reward)
        wnd.write(scene)
        sleep(0.1)
        #if won == False:
            #wnd.write(scene)
            #sleep(0.1)

while True:
    main()
    bot.position = [0,0]
    bot.prev_position = bot.position
    
#sleep(5)