import numpy as np
from tile import Tile

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

def getNeighbor(cursor: Tile, smer: int, _map):

    
    pass

def matrix(curr: Tile, _map):
    #matrix[i, j] sadrzi koliko je dobar potez da se ide u 'i' smeru 'j' koraka
    matrix = np.zeros((6,17)) #6 pravaca, 16 je najduza dijagonala + 1 za dinamicku matricu
    
    #dinamicki izracunati matricu
    for smer in range(6):
        cursor = curr # za sledeci smer se vrati na pocetni tile
        for korak in range(1, 17):
            neighbor = getNeighbor(cursor, smer, _map)
            matrix[smer, korak] = matrix[smer, korak-1] #+ neighbor.score
            cursor = neighbor #samo nastavi od komsije
            
    return
matrix()