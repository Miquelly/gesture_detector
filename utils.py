import config
import numpy as np
from typing import List, Tuple

def corresponding_points(links: dict, list_position_id: dict, list_color_link) -> Tuple[List]:
    list_position_links = []  # Lista de pontos para formar as retas correspondente aos ossos do esqueleto
    
    list_color_links = []
    list_x_links = []
    list_y_links = []

    i = 0
    
    for link in links:
        if link[0] in list_position_id and link[1] in list_position_id:
            list_position_links.append([list_position_id[link[0]], list_position_id[link[1]]])
            list_color_links.append(config.array_color[int(list_color_link[i])])
        i += 1
    # x, y, cor de cada link formando os xs, ys, cores do links de um esqueleto
        
    for connections in list_position_links:

        # connections: Coordenadas para ligar/ Ligações para formar a reta dos ossos => [(x1,y1),(x2,y2)]
        
        x1_x2 = [pts[0] for pts in connections]
        y1_y2 = [pts[1] for pts in connections]

        list_x_links.append(x1_x2)
        list_y_links.append(y1_y2)

    return (list_x_links, list_y_links, list_color_links)

def colors(compare_position, list_position_id):

    color_list = np.zeros(18)
    action = ''

    for conjunto_pts in compare_position:
            
        if conjunto_pts[0] in list_position_id and conjunto_pts[1] in list_position_id:

            if list_position_id[conjunto_pts[0]][1] < list_position_id[conjunto_pts[1]][1]:
                action += f"{1}"
            else:
                action += f"{0}"

    # array_color = ['b-', '#FFFF00', 'r-', 'g-']
    color = 0
    if action == "11":   # Juntas
        color = 1
    elif action == "10": # Esquerda
        color = 2
    elif action == "01": # Direita
        color = 3

    for position in range(len(color_list)):
            
            color_list[position] = color

    return color_list