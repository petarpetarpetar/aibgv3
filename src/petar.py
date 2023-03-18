import time
import numpy as np
from map import Tile, Map
from item_type import ItemType

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
    nextup = [start]
    found = False
    bfs = np.zeros((27,9), dtype=int)
    bfs[start.row, start.column] = -1  # pocetak je -1

    for iteration in range(1, 10): # max 10 iters 
        
        if nextup == []:  # no more tiles to lookup
            print("breaking cuz of nextup")
            break
        start = nextup.pop(0)
        
        for direction in range(6):
            cursor: Tile = start
            print(f"gledam {direction=}")
            while True:
                cursor = _map.get_neighbor(cursor, direction)

                if cursor is None: # if out of bounds
                    break

                print(f"poredim {cursor.row}, {cursor.column}")
                if cursor.tile_content.item_type == ItemType.POND:
                    print("POND")
                    bfs[cursor.row, cursor.column] = -4
                    break

                if cursor.row == end.row and cursor.column == end.column: # dosli smo do kraja puta
                    break

                # otherwise 
                if bfs[cursor.row, cursor.column] == 0 or iteration < bfs[cursor.row, cursor.column]: 
                    nextup.append(cursor)
                    found = True
                    bfs[cursor.row, cursor.column] = iteration
            print(bfs)

            time.sleep(0.08)
    if found:
        print(f"found way in {iteration} steps")


def check_path_pond(start: Tile, direction: int, step: int):
    curr = start
    global _map #hotfix
    for i in range(step): #iteracija koliko i koraka
        curr = Map.get_neighbor(curr, direction)
        if curr.type == "pond":  # TODO: vidi kako je balsa implementirao tile
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
