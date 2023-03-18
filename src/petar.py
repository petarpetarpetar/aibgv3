import numpy as np
from map import Tile

'''
0 - gore
1 - gore-desno
2 - dole-desno
3 - dole
4 - dole-levo
5 - gore-levo
'''


"""
@function matrix - racuna matricu polja 

@param curr - trenutno polje, polje sa kog hoces da izracunas
@param _map - celoukupna mapa i informacije o poljima, [[Tile1, Tile2...][...]]
"""


def runBFS(start: Tile, end: Tile, _map):
    for direction in range(6):
        cursor = start
        
        while True:
            pass    

    pass

def checkPathPond(start: Tile, direction: int, step: int):
    curr = start
    global _map #hotfix
    for i in range(step): #iteracija koliko i koraka
        curr = getNeighbor(curr, direction, _map)
        if curr.type == "pond": #TODO: vidi kako je balsa implementirao tile
            return True
        
    return False


def matrix(curr: Tile, _map):
    #matrix[i, j] sadrzi koliko je dobar potez da se ide u 'i' directionu 'j' stepa
    matrix = np.zeros((6,17)) #6 pravaca, 16 je najduza dijagonala + 1 za dinamicku matricu
    
    #dinamicki izracunati matricu
    for direction in range(6):
        cursor = curr # za sledeci direction se vrati na pocetni tile
        for step in range(1, 17):
            neighbor = getNeighbor(cursor, direction)
            matrix[direction, step] = matrix[direction, step-1] #+ neighbor.score
            cursor = neighbor #samo nastavi od komsije
            
    return
