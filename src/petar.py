import numpy as np
from map import Tile, Map

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


def run_BFS(start: Tile, end: Tile, _map):
    nexup = [start]
    found = False
    for iteration in range(1, 10): # max 10 iters 
        
        if nexup == []: # no more tiles to lookup
            break
        start = nexup.pop(0)
        
        for direction in range(6):
            bfs = np.zeros((27,9))
            cursor: Tile = start
            
            while True:
                cursor = Map.get_neighbor(cursor, direction)
                # stop cases
                if cursor is None: # if out of bounds
                    break

                if cursor.tile_content.item_type == "pond":
                    bfs[cursor.row, cursor.column] = -1
                    break

                if cursor == end: # dosli smo do kraja puta
                    break

                # otherwise 
                if bfs[cursor.row, cursor.column] == 0 or iteration < bfs[cursor.row, cursor.column]: 
                    nexup.append(cursor)
                    found = True
                    bfs[cursor.row, cursor.column] = iteration
    print(bfs)
    if found:
        print(f"found way in {iteration} steps")
    


def check_path_pond(start: Tile, direction: int, step: int):
    curr = start
    global _map #hotfix
    for i in range(step): #iteracija koliko i koraka
        curr = Map.get_neighbor(curr, direction)
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
            neighbor = Map.get_neighbor(cursor, direction)
            matrix[direction, step] = matrix[direction, step-1] #+ neighbor.score
            cursor = neighbor #samo nastavi od komsije
            
    return
