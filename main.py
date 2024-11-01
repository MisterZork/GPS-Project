import csv
from math import sqrt, acos, degrees
import numpy as np

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

def np_calculate_angle(matrix, id):
    product = float(matrix[id[0], 2] * matrix[id[1], 2]
                    + matrix[id[0], 3] * matrix[id[1], 3]
                    + matrix[id[0], 4] * matrix[id[1], 4])
    module_product = float(sqrt(pow(matrix[id[0], 2], 2) + pow(matrix[id[0], 3], 2) + pow(matrix[id[4], 2], 2))
                           * sqrt(pow(matrix[id[1], 2], 2) + pow(matrix[id[1], 3], 2) + pow(matrix[id[1], 4], 2)))
    cos = (product / module_product)
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

def calculate_desync(order):
    """Question 3 - Calculer le décalage de l'horloge récepteur des satellites"""
    pass #TODO - Find, with the resulting matrice, where is the correct answer

def calculate_coordinates_polar(order):
    """Question 4 - Calculer, à partir de 5 satellites, les coordonnées polaires du point GPS"""
    pass #TODO - With The XYZ Vector, find

def googlemaps_finder(long, lat):
    """Question 5 - Utiliser le module googlemaps pour obtenir la description du lieu affiché"""

def satellite_cartesian(nb):
    """Question 6 - Permet d'avoir la hauteur d'un des satellites sélectionné"""
    pass

if __name__ == "__main__":
    sat_data = []
    sat_ID = []
    texte_q1 = f"{"-" * 30}Question 1{"-" * 30}\n Quel est l'angle entre chaque satellite ?"
    texte_q2 = f"{"-" * 30}Question 2{"-" * 30}\n Quel sont les coordonnés affiché par le satellite ?"

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
    print(f"Les coordonnées X, Y et Z où se trouve le GPS sont : {np.round(excel_list[0:3], 6)} (en mètres)")
    print(calculate_desync.__doc__.center(90))

