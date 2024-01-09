import json

# Votre chaîne de données
data = """
AB17.184-003;RT96G;M ;CSRN;00119;05-002-02;184-003;;;;;;;OUI;0
AB17.187-005.Mic cree mais non affecte a un faisceau
AB17.187-006.Mic cree mais non affecte a un faisceau
AB17.187-009;RT96G;M ;CSRN;00119;05-015-02;187-009;;;;;;;OUI;0
AB17.187-014.Mic cree mais non affecte a un faisceau
AB17.187-017;XJ37G;M ;CSRF;00122;05-006-03;187-017;;;;;;;OUI;1
AB17.187-036.Mic cree mais non affecte a un faisceau
AB17.192-004;YK061;M ;CSRN;00062;04-002-03;192-004;;;;;;;OUI;1
AB17.193-000.Mic cree mais non affecte a un faisceau
AB17.194-010.Mic cree mais non affecte a un faisceau
AB17.194-011.Mic cree mais non affecte a un faisceau
AB17.199-011;XJ37G;M ;CSRF;00122;04-008-01;199-011;;;;;;;OUI;1
AB17.200-002;XJ37G;M ;CSRF;00122;03-001-04;200-002;;;;;;;OUI;1
AB17.200-010.Mic cree mais non affecte a un faisceau
AB17.206-007;MPNA0;E ;IMMF;00002;03-026-04;206-007;;;;;;;NON;
AB17.207-000;FMN01;TD;MPNC;00058;03-029-01;207-000;;;;;;;;
AB17.207-001.Mic cree mais non affecte a un faisceau
AB17.207-004;YK031;M ;CSRN;00062;03-006-01;207-004;;;;;;;OUI;1
AB17.208-004;YK051;M ;CSRN;00062;02-002-03;208-004;;;;;;;OUI;1
AB17.209-009;RT96G;M ;CSRN;00119;02-008-01;209-009;;;;;;;OUI;0
AB17.215-013;RT96G;M ;CSRN;00119;02-004-01;215-013;;;;;;;OUI;0
AB17.215-024.Mic cree mais non affecte a un faisceau
AB17.215-025.Mic cree mais non affecte a un faisceau
AB17.215-036;XJ37G;M ;CSRF;00122;02-015-01;215-036;;;;;;;OUI;1
AB17.215-060.Mic cree mais non affecte a un faisceau
AB17.215-061.Mic cree mais non affecte a un faisceau
AB17.216-000.Mic cree mais non affecte a un faisceau
AB17.216-002;YK031;M ;CSRN;00062;01-001-03;216-002;;;;;;;OUI;1
AB17.216-005;YK061;M ;CSRN;00062;01-002-03;216-005;;;;;;;OUI;1
AB17.216-008.Mic cree mais non affecte a un faisceau
AB17.217-006.Mic cree mais non affecte a un faisceau
AB17.217-013.Mic cree mais non affecte a un faisceau
AB17.218-000.Mic cree mais non affecte a un faisceau
AB17.218-004;YK051;M ;CSRN;00062;01-010-01;218-004;;;;;;;OUI;1
AB17.218-012.Mic cree mais non affecte a un faisceau
AB17.221-013.Mic cree mais non affecte a un faisceau
AB17.221-014.Mic cree mais non affecte a un faisceau
AB17.223-000.Mic cree mais non affecte a un faisceau
"""
# Divisez la chaîne en lignes
lines = data.strip().split('\n')

# Initialisez une liste pour stocker les éléments du fichier JSON
json_data = []

# Parcourez chaque ligne
for line in lines:
    # Divisez chaque ligne par ';'
    parts = line.split(';')

    # Vérifiez si la ligne se termine par "Mic cree mais non affecte a un faisceau"
    if len(parts) == 1 and parts[0].endswith('Mic cree mais non affecte a un faisceau'):
        continue  # Passez à la prochaine ligne s'il y a une correspondance

    # Vérifiez si la ligne contient le caractère '-'
    if '-' not in parts[0]:
        continue  # Passez à la prochaine ligne si le caractère '-' n'est pas présent

    # Séparez la partie 0 par '.'
    ab17, aflr_part = parts[0].split('.')[:2]

    # Utilisez directement la partie 1 de la partie 0
    aflr = aflr_part

    extremité = parts[1]  # La première partie de la deuxième partie
    cirdem = "OUI" if parts[-1] == '0' else 'NON'

    # Créez un dictionnaire pour chaque ligne
    entry = {
        ab17: {
            "aflr": aflr,
            "extremite": extremité,
            "cirdem": cirdem
        }
    }

    # Ajoutez le dictionnaire à la liste
    json_data.append(entry)

# Générez un fichier JSON
with open('output.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=2)

print("Fichier JSON généré avec succès.")