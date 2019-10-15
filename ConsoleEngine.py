'''
Graphic engine for console, Maybe I should die
after import clears screen.
'''

#!/usr/bin/env python
#from __future__ import print_function
import subprocess as sub
import time
import pickle

def Logo():
    print("Created by DrEenot, inspired by Saitan")
Logo()
time.sleep(0.6)
sub.call('cls',shell=True)

class WorkArea:
    def __init__(self,size,MainSymbol):
        #sub.call('cls',shell=True)
        '''        
        size is typle [width,height]
        Main Symbol is a symbol, which will be used for creating borders of work area
        '''
        self.size = size
        sub.call(f"MODE {size[0]+3},{size[1]+3}",shell = True)
        try:
            self.MainSymbol = str(MainSymbol)
        except:
            raise Exception('Something wrong with symbol, try another')
    def write(self,scene):
        '''
        Writes raw buffer of pixels
        buffer is array of 'pixels' - Example : symbols [['#','!','*'],
                                                         ['#','!','*']]
        Nothing = ' '
        '''
        #if scene.size[0] > self.size[0] or scene.size[1] > self.size[1]:
            #raise Exception(f'Wrong Number of lines in input buffer expected {self.size}')
        print(self.MainSymbol * (self.size[0] + 2),end = '\n')
        for y in range(self.size[1]):
            print(self.MainSymbol,end = '')
            print(''.join(scene.scene[y]) , end = '')
            print(self.MainSymbol,end = '\n')
            
        print(self.MainSymbol * (self.size[0] + 2),end = '\n')

    def clear(self):
        sub.call('cls',shell=True)


class GraphicObject:
    def __init__(self,size,symbol):
        self.size = size
        self.symbol = symbol

class Scene:
    def __init__(self,size:list,Symbol:str):
        self.size = size
        self.Symbol = Symbol
        self.scene = []

    def init_scene(self):
        buf = []
        self.scene = []
        for i in range(self.size[0]):
            buf.append(self.Symbol)
        for i in range(self.size[1]):
            self.scene.append(buf.copy())

    def write_symbol(self,position:list,symbol:str):
        self.scene[position[0]][position[1]] = symbol
    
    def write_object(self,position:list,object:GraphicObject):
        for y in range(position[1],position[1]+object.size[1]):
            for x in range(position[0],position[0]+object.size[0]):
                self.scene[y][x] = object.symbol
