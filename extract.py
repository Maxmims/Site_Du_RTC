import json

# Votre chaîne de données
data = """
LL76.126-000;YK061;M ;CSRN;00341;14-001-01;126-000;;;;;;;NON;1
LL76.126-001;YK051;M ;CSRN;00341;14-001-02;126-001;;;;;;;NON;1
LL76.126-014;YK051;M ;CSRN;00341;14-032-01;126-014;;;;;;;NON;1
LL76.127-006.Mic cree mais non affecte a un faisceau
LL76.128-000;YK051;M ;CSRN;00341;13-007-02;128-000;;;;;;;NON;1
LL76.128-001;YK031;M ;CSRN;00341;13-016-02;128-001;;;;;;;NON;1
LL76.128-005;SG04G;M ;CSRN;00460;13-015-02;128-005;;;;;;;OUI;0
LL76.128-009;YK031;M ;CSRN;00341;13-005-04;128-009;;;;;;;NON;1
LL76.128-013;YK031;M ;CSRN;00341;13-023-01;128-013;;;;;;;NON;1
LL76.129-000;SG04G;M ;CSRN;00460;13-004-04;129-000;;;;;;;OUI;0
LL76.129-007;YK031;M ;CSRN;00341;13-014-02;129-007;;;;;;;NON;1
LL76.129-008;YK031;M ;CSRN;00341;13-013-02;129-008;;;;;;;NON;1
LL76.129-014;YK051;M ;CSRN;00341;13-014-03;129-014;;;;;;;NON;1
LL76.130-002;YK031;M ;CSRN;00341;12-010-03;130-002;;;;;;;NON;1
LL76.130-004;YK061;M ;CSRN;00341;12-017-01;130-004;;;;;;;NON;1
LL76.130-012;LL04G;M ;CSRN;00460;12-018-01;130-012;;;;;;;OUI;0
LL76.130-013;SG04G;M ;CSRN;00460;12-018-02;130-013;;;;;;;OUI;0
LL76.130-015;SG04G;M ;CSRN;00460;12-028-04;130-015;;;;;;;OUI;0
LL76.131-001;YK061;M ;CSRN;00341;13-009-03;131-001;;;;;;;NON;1
LL76.131-003;YK061;M ;CSRN;00341;13-001-04;131-003;;;;;;;NON;1
LL76.131-005;SG04G;M ;CSRN;00460;13-013-01;131-005;;;;;;;OUI;0
LL76.131-006;IN01Y;M ;CSRN;00091;13-003-03;131-006;;;;;;;OUI;0
LL76.131-007;IN01X;M ;CSRN;00091;13-003-04;131-007;;;;;;;OUI;0
LL76.131-008;LL04G;M ;CSRN;00460;13-005-01;131-008;;;;;;;OUI;0
LL76.131-009;LL04G;M ;CSRN;00460;13-012-04;131-009;;;;;;;OUI;0
LL76.131-011;SG04G;M ;CSRN;00460;13-011-04;131-011;;;;;;;OUI;0
LL76.134-007;SG04G;M ;CSRN;00460;12-011-01;134-007;;;;;;;OUI;0
LL76.134-009;LL04G;M ;CSRN;00460;12-031-04;134-009;;;;;;;OUI;0
LL76.134-010;IN01X;M ;CSRN;00091;12-003-03;134-010;;;;;;;OUI;0
LL76.134-011;IN01Y;M ;CSRN;00091;12-003-04;134-011;;;;;;;OUI;0
LL76.134-015;LL04G;M ;CSRN;00460;12-012-02;134-015;;;;;;;OUI;0
LL76.135-002;SG04G;M ;CSRN;00460;12-002-03;135-002;;;;;;;OUI;0
LL76.135-003;SG04G;M ;CSRN;00460;12-008-02;135-003;;;;;;;OUI;0
LL76.135-005;LL04G;M ;CSRN;00460;12-003-01;135-005;;;;;;;OUI;0
LL76.135-006;SG04G;M ;CSRN;00460;12-004-03;135-006;;;;;;;OUI;0
LL76.135-007;LL04G;M ;CSRN;00460;12-010-04;135-007;;;;;;;OUI;0
LL76.135-009;SG04G;M ;CSRN;00460;12-005-02;135-009;;;;;;;OUI;0
LL76.135-012;YK061;M ;CSRN;00341;12-006-01;135-012;;;;;;;NON;1
LL76.135-015;SG04G;M ;CSRN;00460;12-006-04;135-015;;;;;;;OUI;0
LL76.136-000;FMN01;TD;MPNC;00058;SMT1G;136-000;;;;;;;OUI;
LL76.136-001;YK031;M ;CSRN;00341;SMT1G;136-001;;;;;;;NON;1
LL76.137-002;LL04G;M ;CSRN;00460;SMT1G;137-002;;;;;;;OUI;0
LL76.138-001;YK061;M ;CSRN;00341;SMT1G;138-001;;;;;;;NON;1
LL76.138-002;YK061;M ;CSRN;00341;SMT1G;138-002;;;;;;;NON;1
LL76.138-003.Mic cree mais non affecte a un faisceau
LL76.140-001;YK051;M ;CSRN;00341;SMT1G;140-001;;;;;;;NON;1
LL76.140-002;YK031;M ;CSRN;00341;SMT1G;140-002;;;;;;;NON;1
LL76.141-001;SG04G;M ;CSRN;00460;SMT1G;141-001;;;;;;;OUI;0
LL76.144-001;YK051;M ;CSRN;00341;SMT1G;144-001;;;;;;;NON;1
LL76.144-002;YK031;M ;CSRN;00341;SMT1G;144-002;;;;;;;NON;1
LL76.145-000;LL04G;M ;CSRN;00460;SMT1G;145-000;;;;;;;OUI;0
LL76.145-001;YK061;M ;CSRN;00341;SMT1G;145-001;;;;;;;NON;1
LL76.145-002;LL04G;M ;CSRN;00460;SMT1G;145-002;;;;;;;OUI;0
LL76.146-000.Mic cree mais non affecte a un faisceau
LL76.148-000;YK061;M ;CSRN;00341;SMT1G;148-000;;;;;;;NON;1
LL76.148-002.Mic cree mais non affecte a un faisceau
LL76.152-002;YK051;M ;CSRN;00341;SMT1G;152-002;;;;;;;NON;1
LL76.154-002.Mic cree mais non affecte a un faisceau
LL76.154-003.Mic cree mais non affecte a un faisceau
LL76.160-001.Mic cree mais non affecte a un faisceau
LL76.161-002;YK061;M ;CSRN;00341;SMT1G;161-002;;;;;;;NON;1
LL76.162-000;YK051;M ;CSRN;00341;SMT1G;162-000;;;;;;;NON;1
LL76.164-000.Mic cree mais non affecte a un faisceau
LL76.164-001.Mic cree mais non affecte a un faisceau
LL76.166-001.Mic cree mais non affecte a un faisceau
LL76.168-000.Mic cree mais non affecte a un faisceau
LL76.169-000.Mic cree mais non affecte a un faisceau
LL76.169-001;YK061;M ;CSRN;00341;SMT1G;169-001;;;;;;;NON;1
LL76.169-003;YK051;M ;CSRN;00341;SMT1G;169-003;;;;;;;NON;1
LL76.172-003.Mic cree mais non affecte a un faisceau
LL76.176-000;YK031;M ;CSRN;00341;SMT1G;176-000;;;;;;;NON;1
LL76.177-000.Mic cree mais non affecte a un faisceau
LL76.177-002.Mic cree mais non affecte a un faisceau
LL76.181-000;YK031;M ;CSRN;00341;SMT1G;181-000;;;;;;;NON;1
LL76.188-002;IN01X;M ;CSRN;00091;SMT1G;188-002;;;;;;;OUI;0
LL76.188-003;IN01Y;M ;CSRN;00091;SMT1G;188-003;;;;;;;OUI;0
LL76.189-002;SG04G;M ;CSRN;00460;SMT1G;189-002;;;;;;;OUI;0
LL76.192-000.Mic cree mais non affecte a un faisceau
LL76.192-002;IN01X;M ;CSRN;00091;SMT1G;192-002;;;;;;;OUI;0
LL76.192-003;IN01Y;M ;CSRN;00091;SMT1G;192-003;;;;;;;OUI;0
LL76.194-003.Mic cree mais non affecte a un faisceau
LL76.196-000;YK051;M ;CSRN;00341;SMT1G;196-000;;;;;;;NON;1
LL76.196-001.Mic cree mais non affecte a un faisceau
LL76.197-001.Mic cree mais non affecte a un faisceau
LL76.197-002;IN01X;M ;CSRN;00091;SMT1G;197-002;;;;;;;OUI;0
LL76.197-003;IN01Y;M ;CSRN;00091;SMT1G;197-003;;;;;;;OUI;0
LL76.200-000;YK051;M ;CSRN;00341;SMT1G;200-000;;;;;;;NON;1
LL76.209-002;SG04G;M ;CSRN;00460;SMT1G;209-002;;;;;;;OUI;0
LL76.212-000.Mic cree mais non affecte a un faisceau
LL76.216-000;FMN01;TD;MPNC;00058;SMT1G;216-000;;;;;;;OUI;


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