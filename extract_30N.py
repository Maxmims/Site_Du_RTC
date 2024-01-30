import openpyxl
import json

def excel_to_json(file_path):
    # Charger le fichier Excel
    workbook = openpyxl.load_workbook(file_path)
    
    # Accéder à la deuxième feuille (page)
    sheet = workbook.worksheets[1]

    # Initialiser un dictionnaire pour stocker les données JSON
    json_data = {}

    # Parcourir les lignes du fichier Excel à partir de la deuxième ligne (car la première ligne est généralement la ligne d'en-tête)
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Extraire les valeurs des colonnes A, B, C, D
        support = row[0]
        aflr = f"{str(row[1]).zfill(3)}-{str(row[2]).zfill(3)}"
        code = row[3]


        # Si le code n'est pas déjà dans le dictionnaire, ajoutez-le avec une liste vide comme valeur
        if code not in json_data:
            json_data[code] = []

        # Ajouter les données actuelles à la liste associée au code
        json_data[code].append({
            "aflr": aflr,
            "support": support
        })

    # Fermer le fichier Excel
    workbook.close()

    # Convertir le dictionnaire en format JSON
    json_result = json.dumps(json_data, indent=2)

    # Écrire le JSON dans un fichier
    with open("output.json", "w") as json_file:
        json_file.write(json_result)

# Appel de la fonction avec le chemin du fichier Excel en argument
excel_to_json("cartoo-tdbALLok.xlsx")
