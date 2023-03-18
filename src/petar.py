import random
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


def run_BFS(start: Tile, end: Tile, _map: Map, enemy):
    next_iteration_tiles = [start]
    new_tiles = []
    bfs = np.full((27, 9), 0, dtype=int)
    bfs[start.row, start.column] = -1
    visited = []

    found_end = False

    for iteration in range(1, 10):
        if found_end:
            break
        for start in next_iteration_tiles:
            for direction in range(6):
                current = start
                while True:  # dok ne naidjes na pond ili na cosak
                    current: Tile = _map.get_neighbor(current, direction)
                    if current is None:
                        break

                    if current.tile_content.item_type == ItemType.POND:
                        bfs[current.row, current.column] = -5
                        break

                    # Enemy Bee
                    if current.row == enemy[0] and current.column == enemy[1]:
                        break

                    if bfs[current.row, current.column] == 0:  # if unvisited
                        bfs[current.row, current.column] = iteration
                        new_tiles.append(current)

                    if current.row == end.row and current.column == end.column:
                        # print(f"found end in {iteration}")
                        if iteration == 1 or iteration == 0:
                            print(f"steps to end= {bfs[end.row, end.column]}")
                            return current
                        found_end = True
                        break

        next_iteration_tiles = new_tiles
        new_tiles = []
    print(f"steps to end= {bfs[end.row, end.column]}")
    # BACKTRACKING

    num_steps = bfs[end.row, end.column]
    if num_steps <= 0:
        print("cant get there or already there")
        return None

    # run komsije

    # start = end

    # for dir in range(6):
    #     current = _map.get_neighbor(current, dir)
    #     if bfs[current.row, current.column]

    num_steps = bfs[end.row, end.column]

    if num_steps <= 0:
        print("cant get there or already there")
        return None
    else:
        current = end
        candidate_list = []
        flag_found_move = False
        definite = None

        if bfs[end.row, end.column] == 1:  # mozes odmah na pocetku da dodjes tu
            potential = end
            flag_found_move = True
            definite = potential
            print("pa mozes odma")
            return definite

        while not flag_found_move:
            for direction in range(0, 6):
                candidate: Tile = _map.get_neighbor(current, direction)
                if candidate is None:
                    continue

                if bfs[candidate.row, candidate.column] <= bfs[current.row, current.column] and bfs[
                    candidate.row, candidate.column] not in [0, -5]:
                    if candidate not in candidate_list and candidate not in visited:
                        candidate_list.append(candidate)
                        visited.append(candidate)

            potential: Tile = None
            for potential in candidate_list:
                if bfs[potential.row, potential.column] < bfs[current.row, current.column]:
                    current = potential
                    if bfs[potential.row, potential.column] == 1:
                        flag_found_move = True  # u sledecem ces moci da dodjes do pocetne tacke
                    break  # TODO: RANDOM

            if flag_found_move:
                definite = potential
                break

            if candidate_list != [] and not flag_found_move:
                # current = random.choice(candidate_list)
                # candidate_list.remove(current)
                current = candidate_list.pop(0)

        return definite


def check_path_pond(start: Tile, direction: int, step: int):
    curr = start
    global _map  # hotfix
    for i in range(step):  # iteracija koliko i koraka
        curr = Map.get_neighbor(curr, direction)
        if curr.type == "pond":  # TODO: vidi kako je balsa implementirao tile
            return True

    return False


def matrix(curr: Tile, _map):
    # matrix[i, j] sadrzi koliko je dobar potez da se ide u 'i' directionu 'j' stepa
    matrix = np.zeros((6, 17))  # 6 pravaca, 16 je najduza dijagonala + 1 za dinamicku matricu

    # dinamicki izracunati matricu
    for direction in range(6):
        cursor = curr  # za sledeci direction se vrati na pocetni tile
        for step in range(1, 17):
            neighbor = Map.get_neighbor(cursor, direction)
            matrix[direction, step] = matrix[direction, step - 1]  # + neighbor.score
            cursor = neighbor  # samo nastavi od komsije

    return