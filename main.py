import csv
from math import sqrt, acos, asin, degrees
import numpy as np
import googlemaps

VITESSE_LUMIERE = 299792458
RAYON_TERRE = 6367444.65712259

def satellite_reader(name_file=None, var=None):
    """
    Cette fonction convertit les données .csv en un dictionnaire.
    """
    if var is None:
        var = []
    with open(name_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if len(row) > 0 and row[0].isdigit():
                var.append({
                    'nb': int(row[0]),
                    't': float(row[1].replace(',', '.')),
                    't_prime': float(row[2].replace(',', '.')),
                    'x': float(row[3].replace(',', '.')),
                    'y': float(row[4].replace(',', '.')),
                    'z': float(row[5].replace(',', '.'))
                })
    return var

def ordering(id_test):
    """
    Cette fonction permet de trouver toutes les combinaisons possibles sans répétition
    (s'il n'y a pas de mêmes valeurs dans la liste).
    """
    listing = []
    for a in range(len(id_test)):
        for b in range(len(id_test)):
            order_temp = [id_test[a], id_test[b]]
            if a < b:
                listing.append(order_temp)
    return listing

def calculate_angle(ang1, ang2):
    """
    Cette fonction permet de calculer l'angle entre deux coordonnées de satellites.
    """
    product = float(ang1[0]*ang2[0] + ang1[1]*ang2[1] + ang1[2]*ang2[2])
    module_product = float(sqrt(pow(ang1[0], 2)  + pow(ang1[1], 2) + pow(ang1[2], 2))
                           * sqrt(pow(ang2[0], 2) + pow(ang2[1], 2) + pow(ang2[2], 2)))
    cos = (product/module_product)
    answer = degrees(acos(cos))
    return answer

def np_calculate_matrix(order, data):
    """
    Cette question permet de trouver les coordonnées X, Y et Z, ainsi que le décalage horaire D
    à l'aide du dictionnaire obtenue dans le .csv et en créant une matrice avec.
    """
    matrix = np.array([[data[order[0] - 1]["t"], data[order[0] - 1]["t_prime"],
                       data[order[0] - 1]["x"], data[order[0] - 1]["y"], data[order[0] - 1]["z"]],
                       [data[order[1] - 1]["t"], data[order[1] - 1]["t_prime"],
                        data[order[1] - 1]["x"], data[order[1] - 1]["y"], data[order[1] - 1]["z"]],
                       [data[order[2] - 1]["t"], data[order[2] - 1]["t_prime"],
                        data[order[2] - 1]["x"], data[order[2] - 1]["y"], data[order[2] - 1]["z"]],
                       [data[order[3] - 1]["t"], data[order[3] - 1]["t_prime"],
                        data[order[3] - 1]["x"], data[order[3] - 1]["y"], data[order[3] - 1]["z"]],
                       [data[order[4] - 1]["t"], data[order[4] - 1]["t_prime"],
                        data[order[4] - 1]["x"], data[order[4] - 1]["y"], data[order[4] - 1]["z"]]])

    ans = np.array(
            [[pow(VITESSE_LUMIERE, 2) * pow((matrix[0][1] - matrix[0][0]), 2)
              - pow((matrix[0][2]), 2) - pow((matrix[0][3]), 2) - pow((matrix[0][4]), 2)],
             [pow(VITESSE_LUMIERE, 2) * pow((matrix[1][1] - matrix[1][0]), 2)
              - pow((matrix[1][2]), 2) - pow((matrix[1][3]), 2) - pow((matrix[1][4]), 2)],
             [pow(VITESSE_LUMIERE, 2) * pow((matrix[2][1] - matrix[2][0]), 2)
              - pow((matrix[2][2]), 2) - pow((matrix[2][3]), 2) - pow((matrix[2][4]), 2)],
             [pow(VITESSE_LUMIERE, 2) * pow((matrix[3][1] - matrix[3][0]), 2)
              - pow((matrix[3][2]), 2) - pow((matrix[3][3]), 2) - pow((matrix[3][4]), 2)],
             [pow(VITESSE_LUMIERE, 2) * pow((matrix[4][1] - matrix[4][0]), 2)
              - pow((matrix[4][2]), 2) - pow((matrix[4][3]), 2) - pow((matrix[4][4]), 2)]])

    new_matrix = np.array(
                [[-2 * matrix[0][2], -2 * matrix[0][3], -2 * matrix[0][4],
                  2 * (pow(VITESSE_LUMIERE, 2) * (matrix[0][1] - matrix[0][0])), 1],
                 [-2 * matrix[1][2], -2 * matrix[1][3], -2 * matrix[1][4],
                  2 * (pow(VITESSE_LUMIERE, 2) * (matrix[1][1] - matrix[1][0])), 1],
                 [-2 * matrix[2][2], -2 * matrix[2][3], -2 * matrix[2][4],
                  2 * (pow(VITESSE_LUMIERE, 2) * (matrix[2][1] - matrix[2][0])), 1],
                 [-2 * matrix[3][2], -2 * matrix[3][3], -2 * matrix[3][4],
                  2 * (pow(VITESSE_LUMIERE, 2) * (matrix[3][1] - matrix[3][0])), 1],
                 [-2 * matrix[4][2], -2 * matrix[4][3], -2 * matrix[4][4],
                  2 * (pow(VITESSE_LUMIERE, 2) * (matrix[4][1] - matrix[4][0])), 1]])

    if np.linalg.det(new_matrix) == 0:
        return quit("ERROR 5 - NO ANSWER FOUND IN MATRIX")
    ans_list = np.transpose(np.dot(np.linalg.inv(new_matrix), ans))
    return ans_list

def calculate_coordinates_polar(coords):
    """
    Cette fonction calcule la latitude, longitude et la hauteur du point GPS
    à l'aide des coordonnées X, Y et Z obtenus précedement.
    """
    x, y, z = coords[0][0], coords[0][1], coords[0][2]
    p = sqrt(x**2 + y**2 + z**2)
    lat = degrees(asin(z / p))
    if y >= 0:
        long = degrees(acos(x/sqrt(x**2 + y**2)))
    else:
        long = degrees(-acos(x/sqrt(x**2 + y**2)))
    h = p - RAYON_TERRE
    return [lat, long, h]

def googlemaps_finder(long_lat, api):
    """
    Cette fonction utilise la clé API de Google pour afficher les informations liés aux coordonnées obtenus.
    """
    gmaps = googlemaps.Client(key=api)
    try:
        lat = long_lat[0]
        long = long_lat[1]
        address = gmaps.reverse_geocode((lat, long))
        return address[0]['formatted_address']
    except ValueError:
        return None

def sat_height(order, sat_info):
    """
    Cette fonction permet de trouver l'altitude du satellite.
    """
    x, y, z = sat_info[order[0] - 1]["x"], sat_info[order[0] - 1]["y"], sat_info[order[0] - 1]["z"]
    return sqrt(x**2 + y**2 + z**2) - RAYON_TERRE

if __name__ == "__main__":
    api_key = None
    sat_data = []
    sat_ID = []
    texte_q1 = f"{"-" * 30}Question 1{"-" * 30}\n Quel est l'angle entre chaque satellite ?"
    texte_q2 = f"{"-" * 30}Question 2{"-" * 30}\n Quels sont les coordonnés affiché par le satellite ?"
    texte_q3 = f"{"-" * 30}Question 3{"-" * 30}\n Quel est le décalage horloge du GPS ?"
    texte_q4 = f"{"-" * 30}Question 4{"-" * 30}\n Quels sont les coordonnées polaires du GPS ?"
    texte_q5 = f"{"-" * 30}Question 5{"-" * 30}\n Où est-ce que se trouve ce GPS ?"
    texte_q6 = f"{"-" * 30}Question 6{"-" * 30}\n Quel est l'altitude du premier satellite ? "

    file = str(input("Quel est le nom du fichier .csv dont tu veux prendre les données satellites ? \n"
                    "(Example : '28_Data') : ") + ".csv")
    satellite_reader(file, sat_data)

    print(texte_q1.center(90))
    nb_sat = int(input("Combien de satellite veux-tu calculer ? (recommandé - 5) \n-> "))
    for i in range(nb_sat):
        sat_temp = int(input(f"C'est quoi l'identifiant du satellite nb. {i+1} : "))
        sat_ID.append(sat_temp)
    new_order = ordering(sat_ID)
    for i in range(len(new_order)):
             first = [sat_data[new_order[i][0] - 1]["x"], sat_data[new_order[i][0] - 1]["y"], sat_data[new_order[i][0] - 1]["z"]]
             second = [sat_data[new_order[i][1] - 1]["x"], sat_data[new_order[i][1] - 1]["y"], sat_data[new_order[i][1] - 1]["z"]]
             rep = calculate_angle(first, second)
             print("-" * 71)
             print(f"| L'angle entre le satellite {new_order[i][0]} et le satellite {new_order[i][1]} est : "
                   f"{round(rep, 6) if rep > 15 else "Trop petit"}° |")

    print(texte_q2.center(90))
    if nb_sat == 5:
        polar_list = np_calculate_matrix(sat_ID, sat_data)
        print(f"Les coordonnées X, Y et Z où se trouve le GPS sont : {int(polar_list[0][0])} m, "
              f"{int(polar_list[0][1])} m, {int(polar_list[0][2])} m")
    else:
        quit("ERROR 3 - NOT EXACTLY 5 SATELLITES")

    print(texte_q3.center(90))
    print(f"Le décalage horloge du GPS est : {np.round(polar_list[0][3], 4)} secondes")

    print(texte_q4.center(90))
    lat = calculate_coordinates_polar(polar_list)[0]
    long = calculate_coordinates_polar(polar_list)[1]
    hauteur = calculate_coordinates_polar(polar_list)[2]
    print(f"Les coordonnées polaires du GPS sont : {round(lat, 6)}°, {round(long, 6)}°, {int(hauteur)} mètres")

    print(texte_q5.center(90))
    if api_key is None:
        print("ERROR 12 - NO API KEY FOUND")
    else:
        print(googlemaps_finder(calculate_coordinates_polar(polar_list), api_key))

    print(texte_q6.center(90))
    i = 0
    while i == 0:
        print(f"L'altitude du satellite {sat_ID[0]} est : {int(sat_height(sat_ID, sat_data))} mètres")
        print(f"En termes de r, l'altitude est : {round(((sat_height(sat_ID, sat_data)) / RAYON_TERRE), 2)}r")
        print("-" * 71)
        confirm = str(input("Est-ce que ce satellite est le bon ? (O/N):"))
        if confirm.lower() == "o":
            i += 1
        else:
            sat = int(input("Quel satellite veux-tu trouver l'altitude ? \n-> "))
            sat_ID[0] = sat