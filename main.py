import csv
from math import sqrt, acos, degrees
import numpy as np

VITESSE_LUMIERE = 299792458
RAYON_TERRE = 6367444.65712259

def satellite_reader(name_file=None):
    """This function converts the standard .csv from homework to actual values for calculations"""
    with open(name_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # Extraire les données des satellites
            if len(row) > 0 and row[0].isdigit():
                satellite_data.append({
                    'nb': int(row[0]),
                    't': float(row[1].replace(',', '.')),
                    't_prime': float(row[2].replace(',', '.')),
                    'x': float(row[3].replace(',', '.')),
                    'y': float(row[4].replace(',', '.')),
                    'z': float(row[5].replace(',', '.'))
                })
    return satellite_data

def np_satellite_reader(name_file=None):
    satellites = np.loadtxt(name_file, delimiter=";", skiprows=3)
    return satellites

def ordering(id_test):
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

def calculate_coordinates_cart(order=None):
    """Question 2 - Calculer, à partir de 5 satellites, les coordonnées cartésiens du point GPS"""
    if order is None:
        order = []
    matrix = np.array([])
    pass

def calculate_desync(order=[]):
    """Question 3 - Calculer le décalage de l'horloge récepteur des satellites"""

def calculate_coordinates_polar(order=[]):
    """Question 4 - Calculer, à partir de 5 satellites, les coordonnées polaires du point GPS"""
    pass

def googlemaps_finder(long, lat):
    """Question 5 - Utiliser le module googlemaps pour obtenir la description du lieu affiché"""

def satellite_cartesian(nb):
    """Question 6 - Permet d'avoir la hauteur d'un des satellites sélectionné"""
    pass

if __name__ == "__main__":
    satellite_data = []
    sat_ID = []
    texte_q1 = f"{"-" * 30}Question 1{"-" * 30}\n Quel est l'angle entre chaque satellite ?"
    texte_q2 = f"{"-" * 30}Question 2{"-" * 30}\n Quel sont les coordonnés affiché par le satellite ?"

    file = str(input("What is the name of the .csv file (in the same directory as the script) \n"
                    "(Example : '28_Data') : ") + ".csv")
    module = bool(input("Do you wanna use the vanilla calculator (0) or the experimental one (1) :"))

    if module is False:
        satellite_reader(file)
        print(texte_q1.center(90))
        nb_sat = int(input("How many satellites do you wanna consider on your project : "))
        for i in range(nb_sat):
            sat_temp = int(input(f"What is the ID of the satellite nb. {i+1} : "))
            sat_ID.append(sat_temp)
        order = ordering(sat_ID)
        for i in range(len(sat_ID)):
            for j in range(len(sat_ID)):
                if i < j:
                    first = [satellite_data[i]["x"], satellite_data[i]["y"], satellite_data[i]["z"]]
                    #first = [satellite_data[2, i], satellite_data[3, i], satellite_data[4, i]]
                    second = [satellite_data[j]["x"], satellite_data[j]["y"], satellite_data[j]["z"]]
                    #second = [satellite_data[2, j], satellite_data[3, j], satellite_data[4, j]]
                    rep = calculate_angle(first, second)
                    print("-" * 60)
                    print(f"| L'angle entre le satellite {i + 1} et le satellite {j + 1} est : "
                          f"{round(rep, 6) if rep > 15 else "Trop petit"} |")

    else:
        np_satellite_reader(file)
        print(texte_q1.center(90))
        nb_sat = int(input("How many satellites do you wanna consider on your project : "))
        for i in range(nb_sat):
            sat_temp = int(input(f"What is the ID of the satellite nb. {i + 1} : "))
            sat_ID.append(sat_temp)
        order = ordering(sat_ID)