def gesture(comparator, parts):

    gesture_list = ""
    position_gesture_list = 0 

    for link in comparator:

        if link[0] in parts and link[1] in parts:

            if parts[link[0]][2] > parts[link[1]][2]:

                gesture_list += f"{1}"
            else: 
                
                gesture_list += f"{0}"

        position_gesture_list += 1

    color_id = 20
    if gesture_list == "11":   # Juntas
        color_id = 30
    elif gesture_list == "10": # Esquerda
        color_id = 40
    elif gesture_list == "01": # Direita
        color_id = 10

    return color_id