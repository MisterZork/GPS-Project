import csv
from math import sqrt, acos, asin, degrees
import numpy as np
import googlemaps
#from dotenv import load_dotenv
#import os

VITESSE_LUMIERE = 299792458
RAYON_TERRE = 6367444.65712259

def satellite_reader(name_file=None, var=None):
    """Cette fonction convertit les données .csv en un dictionnaire"""
    if var is None:
        var = []
    with open(name_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # Extraire les données des satellites
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

def np_satellite_reader(name_file=None, ):
    """Méthode avec numpy pour obtenir une matrice contenant les valeurs de """
    pass #TODO - Do some kind of conversion from .csv to matrix

def ordering(id_test):
    """Crée un ordre pour calculer les angles"""
    listing = []
    for a in range(len(id_test)):
        for b in range(len(id_test)):
            # print(f' test  {i}: {sat_ID[i]}')
            order_temp = [id_test[a], id_test[b]]
            if a < b:
                listing.append(order_temp)
    return listing

def calculate_angle(ang1, ang2):
    """Question 1 - Calculer l'angle entre deux satellites"""
    product = float(ang1[0]*ang2[0] + ang1[1]*ang2[1] + ang1[2]*ang2[2])
    module_product = float(sqrt(pow(ang1[0], 2)  + pow(ang1[1], 2) + pow(ang1[2], 2))
                           * sqrt(pow(ang2[0], 2) + pow(ang2[1], 2) + pow(ang2[2], 2)))
    cos = (product/module_product)
    answer = degrees(acos(cos))
    return answer

def np_calculate_matrix(order, number, data):
    """Question 2 et 3 - Calculer, à partir de cinq satellites, la matrice du .csv contenant les réponses"""
    if number != 5:
        return quit("ERROR 2 - NOT 5 SATELLITES FOUND")
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
    """Question 4 - Calculer, à partir de 5 satellites, les coordonnées polaires du point GPS"""
    x, y, z = coords[0][0], coords[0][1], coords[0][2]
    p = sqrt((x**2) + (y**2) + (z**2))
    lat = degrees(asin(z / p))
    if y >= 0:
        long = degrees(acos(x / sqrt(x**2 + y**2)))
    else:
        long = degrees(-acos(x / sqrt(x**2 + y**2)))
    h = p - RAYON_TERRE
    return [lat, long, h]

def googlemaps_finder(longlat):
    """Question 5 - Utiliser le module googlemaps pour obtenir la description du lieu affiché"""
    # gmaps = googlemaps.Client(key="")
    gmaps = googlemaps.Client(key="INSERT-API-KEY")
    lat = longlat[0]
    long = longlat[1]
    adress = gmaps.reverse_geocode((lat,long))

    return (adress[0]['formatted_address'])

def satellite_cartesian(nb):
    """Question 6 - Permet d'avoir la hauteur d'un des satellites sélectionné"""
    pass

if __name__ == "__main__":
    #load_dotenv()
    #API-KEY = os.getenv('API-KEY')

    sat_data = []
    sat_ID = []
    texte_q1 = f"{"-" * 30}Question 1{"-" * 30}\n Quel est l'angle entre chaque satellite ?"
    texte_q2 = f"{"-" * 30}Question 2{"-" * 30}\n Quels sont les coordonnés affiché par le satellite ?"
    texte_q3 = f"{"-" * 30}Question 3{"-" * 30}\n Quel est le décalage horloge du GPS ?"
    texte_q4 = f"{"-" * 30}Question 4{"-" * 30}\n Quels sont les coordonnées polaires du GPS ?"

    file = str(input("What is the name of the .csv file (in the same directory as the script) \n"
                    "(Example : '28_Data') : ") + ".csv")

    satellite_reader(file, sat_data)
    print(texte_q1.center(90))
    nb_sat = int(input("How many satellites do you wanna consider on your project (recommandé - 5) : "))
    for i in range(nb_sat):
        sat_temp = int(input(f"What is the ID of the satellite nb. {i+1} : "))
        sat_ID.append(sat_temp)
    new_order = ordering(sat_ID)
    for i in range(len(new_order)):
             first = [sat_data[new_order[i][0] - 1]["x"], sat_data[new_order[i][0] - 1]["y"], sat_data[new_order[i][0] - 1]["z"]]
             second = [sat_data[new_order[i][1] - 1]["x"], sat_data[new_order[i][1] - 1]["y"], sat_data[new_order[i][1] - 1]["z"]]
             rep = calculate_angle(first, second)
             print("-" * 60)
             print(f"| L'angle entre le satellite {new_order[i][0]} et le satellite {new_order[i][1]} est : "
                   f"{round(rep, 6) if rep > 15 else "Trop petit"} |")
    print(texte_q2.center(90))
    excel_list = np_calculate_matrix(sat_ID, nb_sat, sat_data)
    print(f"Les coordonnées X, Y et Z où se trouve le GPS sont : {np.round(excel_list[0][0:3], 0)} (en mètres)")
    print(texte_q3.center(90))
    print(f"Le décalage horloge du GPS est : {np.round(excel_list[0][3], 4)} secondes")
    print(texte_q4.center(90))
    print(calculate_coordinates_polar(excel_list))
    print(googlemaps_finder(calculate_coordinates_polar(excel_list)))