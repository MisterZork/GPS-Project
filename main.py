import csv
from math import sqrt, acos, degrees

satellite_data = []
VITESSE_LUMIERE = 299792458
RAYON_TERRE = 6367444.65712259

def satellite_reader(name_file=None):
    """This function converts the standard .csv from homework to actual values for calculations"""
    if name_file :
        quit("ERROR 1 - NO FILE FOUND")
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

def calculate_angle(ang1, ang2):
    """Question 1 - Calculer l'angle entre deux satellites"""
    product = float(ang1[0]*ang2[0] + ang1[1]*ang2[1] + ang1[2]*ang2[2])
    module_product = float(sqrt(pow(ang1[0], 2)  + pow(ang1[1], 2) + pow(ang1[2], 2))
                           * sqrt(pow(ang2[0], 2) + pow(ang2[1], 2) + pow(ang2[2], 2)))
    cos = (product/module_product)
    answer = degrees(acos(cos))
    return answer

def calculate_coordinates_cart(order=[]):
    """Question 2 - Calculer, à partir de 5 satellites, les coordonnées cartésiens du point GPS"""
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
    file = str(input("What is the name of the .csv file (in the same directory as the script) \n"
                     "(Example : '28_Data.csv') : "))
    satellite_reader(file)
    for i in range(len(satellite_data)):
        for j in range(len(satellite_data)):
            if i != j:
                first = [satellite_data[i]["x"], satellite_data[i]["y"], satellite_data[i]["z"]]
                second = [satellite_data[j]["x"], satellite_data[j]["y"], satellite_data[j]["z"]]
                rep = calculate_angle(first, second)
                print(f"L'angle entre le satellite {i + 1} et le satellite {j + 1} est :"
                      f"{round(rep, 6) if rep > 15 else "Trop petit"}")


