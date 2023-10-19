from flask import Flask, render_template, request, send_from_directory , url_for 
import re
import json



with open('templates/data/type.json','r', encoding='utf-8') as type_file:
    type_data = json.load(type_file)

with open('templates/data/categorie.json','r', encoding='utf-8') as categorie_file:
    categorie_data = json.load(categorie_file)

with open('templates/data/marque.json','r', encoding='utf-8') as marque_file:
    marque_data = json.load(marque_file)

with open('templates/data/etat.json','r', encoding='utf-8') as etat_file:
    infos_etat = json.load(etat_file)
    
with open('templates/data/anoil_ura.json','r', encoding='utf-8') as anoil_file:
    anoil_ura = json.load(anoil_file)
    
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['JSON_AS_ASCII'] = False

@app.route('/static/Nunito/static_nunito/<path:filename>')
def serve_font(filename):
    return send_from_directory('static/Nunito/static_nunito', filename, mimetype='font/ttf')

valeurs_ut = [
    
    "UT00<br>Rn0<br>Rn2/96<br>Rn84",
    "UT01<br>Rn8<br>Rn6/100<br>Rn88",
    "UT02<br>Rn16<br>Rn10/104<br>Rn92",
    "UT03<br>Rn24<br>Rn14/108<br>Rn96",
    "UT04<br>Rn32<br>Rn18/112<br>Rn100",
    "UT05<br>Rn40<br>Rn22/116<br>Rn104",
    "UT06<br>Rn48<br>Rn26/120<br>Rn108",
    "UT07<br>Rn56<br>Rn30/124<br>Rn112",
    "UT08<br>Rn82<br>Rn34/128<br>Rn116",
    "UT09<br>Rn90<br>Rn38/132<br>Rn120",
    "UT10<br>Rn98<br>Rn42/136<br>Rn124",
    "UT11<br>Rn106<br>Rn46/140<br>Rn128",
    "UT12<br>Rn114<br>Rn50/144<br>Rn132",
    "UT13<br>Rn122<br>Rn54/148<br>Rn136",
    "UT14<br>Rn130<br>Rn58/152<br>Rn140",
    "UT15<br>Rn138<br>Rn62/156<br>Rn144",
    "UT16<br>Rn64<br>Rn66/93<br>Rn148",
    "TYCN<br>CN1G<br>CNHD CNpaire/impaire<br>CNEHD",
]

def remove_leading_zeros(s):
    return re.sub(r'^0+', '', s)

def extract_codes(text, prefix):
    # Find the part of the text after the prefix
    start_idx = text.find(prefix)
    if start_idx == -1:
        return []
    
    # Find the end of the code part by searching for the next prefix
    end_idx = text.find(prefix, start_idx + len(prefix))
    if end_idx == -1:
        end_idx = len(text)
    
    code_part = text[start_idx + len(prefix):end_idx]
    
    # Remove spaces from the code_part
    code_part = code_part.replace(" ", "")

    # Extract individual codes separated by '+'
    codes = re.findall(r'[A-Z0-9]+', code_part)
    return codes


def get_matches_for_codes(codes, data):
    matches = []
    for code in codes:
        for item in data:
            if item['code'] == code:
                matches.append(f"{item['code']}='{item['description']}'")
    return matches            

def affichage_des_ne_du_couple(numerour,numero_du_couple):
    resultat_list = []
    resultat_list.append([f"NE={numerour}-{str(j).zfill(2)}-{8 * 0 + numero_du_couple}" for j in range(8)])
    for i in range(1, 16):
        ligne = [f"NE={numerour}-{str(j).zfill(2)}-{8 * i + numero_du_couple}" for j in range(8)]
        resultat_list.append(ligne)
    return resultat_list

def is_valid_input(ne_input):
    pattern = r'^\d{1,3}-\d{1,2}-\d{1,3}$'
    return re.match(pattern, ne_input) is not None

@app.route('/')
def home():
    return render_template('Accueil.html')

@app.route('/Fetut')
def Fetut():
    return render_template('Fetut.html',valeurs_ut=valeurs_ut)

@app.route('/Felri')
def Felri():
    return render_template('Felri.html')

@app.route('/StatsEAO')
def StatsEAO():
    return render_template('Statistiques_EAO.html')

@app.route('/NeOfis')
def NeOfis():
    return render_template('NeOfis.html')

@app.route('/Abfase')
def Abfase():
    return render_template('Abfase.html')

@app.route('/Type')
def Type():
    return render_template('Type.html')

@app.route('/Anoil')
def Anoil():
    return render_template('Odiag.html')

@app.route('/Fetut', methods=['POST'])
def executer_programme():

    valeur_entree = request.form.get('donnees')  
    correspondances_de_mot_numero_2 = {
        '0': ["Non bloquée par TPOS", "Pas de diag", "Protocole non connu (téléchargement)", "UT Non équipé"],
        '1': ["Bloquée par TPOS","", "Protocole connu", "Carte en service"],
        '2': ["", "Présence de diag","","Téléchargement en cours"],
        '3': ["","","","Initialisation en cours"],
        '4': ["","","","Carte non initialisée"]
    }
    
    valeur_cartes = []
    presence_de_diag =[]
    presence_de_chargement_de_la_carte =[]
    ancienne_valeur_de_mot_numero = None
    resultats_par_numa = {}
    current_numa = None
    dernier_mot = None

    lines = valeur_entree.split('\n') if valeur_entree is not None else []


    for line in lines:
        match_numa = re.search(r'NUMA = (\d+)', line)
        match_mot = re.search(r'MOT\s+\((\d+)\)', line)
        match_hex = re.search(r'=\s*H\'([A-F0-9]+)\'', line)

        if match_numa:
            current_numa = int(match_numa.group(1))
            if current_numa not in resultats_par_numa:
                resultats_par_numa[current_numa] = []
        elif current_numa is not None and match_mot and match_hex:
            mot_numero = int(match_mot.group(1))
            valeur_hex = match_hex.group(1)
            
            resultats = resultats_par_numa[current_numa]

            if ancienne_valeur_de_mot_numero is not None and ancienne_valeur_de_mot_numero == mot_numero:
                valeur_cartes.append("abs")
                presence_de_diag.append("abs")
            ancienne_valeur_de_mot_numero = mot_numero
        
            if dernier_mot == 2 and mot_numero == 4 :
                valeur_cartes.append("Carte en BUG")
            dernier_mot = mot_numero
            
            if mot_numero == 2:
                
                for i in range(4):
                    valeur = int(valeur_hex[i])
                    
                    if str(valeur) in correspondances_de_mot_numero_2:
                        resultats.append(correspondances_de_mot_numero_2[str(valeur)][i])
                        
                    if i== 1 and valeur == 2:
                        presence_de_diag.append(correspondances_de_mot_numero_2['2'][1])
                        
                    if i == 1 and valeur == 0:
                        presence_de_diag.append(correspondances_de_mot_numero_2['0'][1])
                        
                    if i == 3 and valeur == 2:
                        presence_de_chargement_de_la_carte.append(correspondances_de_mot_numero_2['2'][3])

                    
                    
            elif mot_numero == 3:
                if str(valeur_hex[-3:])=="100":
                    valeur_cartes.append("chargée")
                if str(valeur_hex[-3:])== "101":
                    valeur_cartes.append("NOK")
                if int(valeur_hex[1]) == 0:
                    resultats.append("Non présent en liste de polling")
                elif int(valeur_hex[1]) == 1:
                    resultats.append("Présent en liste de polling")

                if int(valeur_hex[3]) == 0:
                    resultats.append("UT accessible")
                elif int(valeur_hex[3]) == 1:
                    resultats.append("UT inaccessible")
                elif int(valeur_hex[3]) == 2:
                    resultats.append("UT inaccessible reprise en cours...")
                elif int(valeur_hex[3]) == 3:
                    resultats.append("UT inaccessible")
                elif int(valeur_hex[3]) == 4:
                    resultats.append("Présent en liste de polling")

            elif mot_numero == 4:
                carte = {
                    "03": "TABA16",
                    "04": "TABA16+FIL C",
                    "05": "TABAD",
                    "06": "TABAD+FIL C",
                    "07": "TABAE",
                    "08": "TADL",
                    "09": "TDQF",
                    "0F": "TABN1 G(TN4F)",
                    "10": "TABN1 G(TNAT)",
                    "11": "TANAE",
                    "12": "TADP",
                    "13": "TABN2G (TN4F)",
                    "14": "TADPB",
                    "80": "TFLC",
                    "81": "TPLA",
                    "82": "TFILM",
                    "83": "TRF8",
                    "84": "TPOL",
                    "85": "TUTP"
                }.get(valeur_hex[-2:].upper())

                resultats.append(f"La carte est une : {carte}")
        if current_numa is not None:
            if len(presence_de_chargement_de_la_carte) < len(resultats_par_numa) - 1:
                presence_de_chargement_de_la_carte.append('b'+str(current_numa))
    
    return render_template('Fetut.html',valeurs_ut=valeurs_ut, resultat=resultats_par_numa, valeurs=valeur_cartes, presence_de_diags=presence_de_diag, chargement=presence_de_chargement_de_la_carte)

@app.route('/Felri', methods=['POST'])
def executer_programme_Felri():
    

    def ajouter_resultat(condition, message):
        if condition:
            resultat.append(message)

    def convertir_hex_vers_binaire(valeur_hex):
        binary_valeur = bin(int(valeur_hex, 16))[2:].zfill(8)
        return binary_valeur

    valeur_entree = request.form.get('donnees')
    resultat = []  
    lines = valeur_entree.split('\n') if valeur_entree is not None else [] 
    
    for line in lines:
        match_mot = re.search(r'MOT\s+\((\d+)\)', line)
        match_hex = re.search(r'=\s*H\'([A-F0-9]+)\'', line)
        
        if match_mot and match_hex:
            mot_numero = int(match_mot.group(1))
            valeur_hex = match_hex.group(1)
            
            if mot_numero == 1:
                valeur_hex_3 = int(valeur_hex[3])
                
                if valeur_hex_3 == 0:
                    resultat.append("NEQ non équipée")
                elif valeur_hex_3 == 1:
                    resultat.append("ES en service")
                elif valeur_hex_3 == 2:
                    resultat.append("INDO indisponible occupée")
                elif valeur_hex_3 == 3:
                    resultat.append("INDL indisponible libre")
                elif valeur_hex_3 == 4:
                    resultat.append("INDLS indisponible ocupée par une liaison spécialisée")
                elif valeur_hex_3 == 5:
                    resultat.append("BLO bloquée")
                
                binary_valeur = convertir_hex_vers_binaire(valeur_hex[:2])
                
                ajouter_resultat(int(binary_valeur[-1]) == 0, "Pas d'alarme détectée sur le MIC")
                ajouter_resultat(int(binary_valeur[-1]) == 1, "Alarme détectée sur le mic")
                
                ajouter_resultat(int(binary_valeur[6]) == 0, "LR OK (pas en faute)")
                
                if int(binary_valeur[6]) == 1:
                    resultat.append("LR en faute")
                    valeur_de_la_vt_en_faute = int(binary_valeur[1:6], 2)
                    resultat.append(f"La VT en faute est la : {str(valeur_de_la_vt_en_faute)}")
            
            elif mot_numero == 2:
                binary_valeur = convertir_hex_vers_binaire(valeur_hex[-2:])
                decimal_valeur = int(binary_valeur[-5:], 2)
                resultat.append(f"La LR est raccordée sur le CN : {str(decimal_valeur)}")
                
                binary_valeur = convertir_hex_vers_binaire(valeur_hex[:2])
                decimal_valeur = int(binary_valeur, 2)
                resultat.append(f"Il y a {str(decimal_valeur)} voie(s) de libre")
            
            elif mot_numero == 3:
                binary_valeur = convertir_hex_vers_binaire(valeur_hex[-2:])
                decimal_valeur = int(binary_valeur, 2)
                resultat.append(f"Le numéro de la première voie libre est : {str(decimal_valeur)} (si = 0 pas de voies libres)")
                
                binary_valeur = convertir_hex_vers_binaire(valeur_hex[:2])
                decimal_valeur = int(binary_valeur, 2)
                resultat.append(f"Le numéro de la dernière voie libre est : {str(decimal_valeur)} (si = 0 pas de voies libres)")
            
            elif mot_numero == 4:
                valeur_hex_1 = int(valeur_hex[1])
                
                ajouter_resultat(int(valeur_hex[-1]) == 0, "La liaison est une LR")
                ajouter_resultat(int(valeur_hex[-1]) == 1, "La liaison est un MIC")
                
                ajouter_resultat(valeur_hex_1 == 0, "Liaison à débit Normal (2Mbits)")
                ajouter_resultat(valeur_hex_1 == 1, "Liaison à débit intermédiaire")
    
    return render_template('Felri.html',resultat=resultat)   

@app.route('/NeOfis', methods=['POST'])
def executer_programme_NeOfis():
    resultat = None
    if request.method == 'POST':
        ne = request.form['ne']
        
        if not is_valid_input(ne):
            ne_error = "Format NE non valide. Le format doit être chiffre-chiffre-chiffre."
            return render_template('NeOfis.html', ne_error=ne_error)
        else:            
            partie = ne.split("-")
            numeroabo = int(partie[2])
            numerour = int(partie[0])
            if not 0 <= numeroabo <= 127:
                numeroabo_error = "NE non valide. La broche doit être comprise entre 0 et 127."
                return render_template('NeOfis.html', numeroabo_error=numeroabo_error)
            else:       
                resultat = numeroabo / 8
                arrondi = round(resultat, 3)
                chiffre_apres_virgule = int(arrondi * 1000) % 1000
                vc = {
                    0: 0,
                    125: 1,
                    250: 2,
                    375: 3,
                    500: 4,
                    625: 5,
                    750: 6,
                    875: 7
                }.get(chiffre_apres_virgule)
                
                resultat = affichage_des_ne_du_couple(numerour,vc)
                

            return render_template('NeOfis.html', resultat=resultat, couple=vc)    

@app.route('/type', methods=['POST'])
def executer_programme_Type():
    type_matches = []
    categorie_matches = []
    marque_matches = []
    no_matches_found = False
    type_code = []  # Initialisation par défaut
    categorie_codes = []  # Initialisation par défaut
    marque_codes = []  # Initialisation par défaut
    

    if request.method == 'POST':
        input_text = request.form['inputText_ty_cat']
        
        # Extract codes after "TY=" and "CAT="
        type_code = extract_codes(input_text, "TY=")
        categorie_codes = extract_codes(input_text, "CAT=")
        marque_codes = extract_codes(input_text, "MAR=")
       

        # Search for matches in type_data and categorie_data
        type_matches = get_matches_for_codes(type_code, type_data)
        categorie_matches = get_matches_for_codes(categorie_codes, categorie_data)
        marque_matches = get_matches_for_codes(marque_codes,marque_data)
        # Check if no matches were found
        if not type_matches and not categorie_matches:
            no_matches_found = True

    return render_template('Type.html',marque_matches=marque_matches, type_matches=type_matches, categorie_matches=categorie_matches, no_matches_found=no_matches_found)


     
@app.route('/StatsEAO', methods=['POST'])

def executer_Statistiques_EAO():

    data = {}
    current_model = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        current_model = process_user_input(user_input,data)
    return render_template('Statistiques_EAO.html', data=data, current_model=current_model)

            
def process_user_input(user_input, data):
    # Initialisez les dictionnaires pour stocker les données RN et ALV
    xej_data = {}
    eao_data = {}

    # Analysez les données de l'utilisateur et mettez à jour les dictionnaires
    lines = user_input.split('\n')
    current_model = None  # Pour suivre le modèle actuel (XEJ ou EAO)
    model_found = False  # Booléen pour indiquer si le modèle a été trouvé
    for i, line in enumerate(lines):
        if i == 0:  # Vérifiez la première ligne seulement
            if 'NOM=' in line:
                current_model = 'EAO'
                found_condition = True  # Condition trouvée
            else:
                current_model = 'XEJ'
                found_condition = True  # Condition trouvée

    # Si un modèle a été identifié, continuez à traiter les lignes
    if found_condition:
        for line in lines:
            if current_model == 'XEJ':
                match = re.search(r'NALV=(\d+).*RN=(\d+)', line)
                if match:
                    alv = match.group(1).lstrip('0')  # Supprime les zéros non significatifs à gauche
                    rn = match.group(2).lstrip('0')  # Supprime les zéros non significatifs à gauche
                    key = f'ALV{alv}_RN{rn}'
                    xej_data[key] = xej_data.get(key, 0) + 1

            elif current_model == 'EAO':
                # Traitement des lignes avec le modèle EAO
                match = re.search(r'NALV=(\d+).*RN=(\d+)', line)
                if match:
                    alv = match.group(1).lstrip('0')
                    rn = match.group(2).lstrip('0')
                    key = f'ALV{alv}_RN{rn}'
                    eao_data[key] = eao_data.get(key, 0) + 1

        # Mettez à jour le dictionnaire data en fonction du modèle choisi
        if current_model == 'XEJ':
            data.update(xej_data)
        elif current_model == 'EAO':
            data.update(eao_data)

    return current_model  # Retournez current_model à la fin de la fonction

@app.route('/Abfase', methods=['POST'])

def executer_Abfase():
    
    # Dictionnaires pour la correspondance entre le numéro de broche et le numéro UT
    dictionnaire_paire = {
        0: "000<=015",
        1: "016<=031",
        2: "032<=047",
        3: "048<=063",
        4: "064<=079",
        5: "080<=095",
        6: "096<=111",
        7: "112<=127"
    }

    dictionnaire_impaire = {
        8: "000<=015",
        9: "016<=031",
        10: "032<=047",
        11: "048<=063",
        12: "064<=079",
        13: "080<=095",
        14: "096<=111",
        15: "112<=127"
    }
    
    valeurs_ut_si_cn_paire = {
    "UT0": "Rn0 / Rn2 / Rn84 ",
    "UT1": "Rn8 / Rn6 / Rn88",
    "UT2": "Rn16 / Rn10 / Rn92",
    "UT3": "Rn24 / Rn14 / Rn96",
    "UT4": "Rn32 / Rn18 / Rn100",
    "UT5": "Rn40 / Rn22 / Rn104",
    "UT6": "Rn48 / Rn26 / Rn108",
    "UT7": "Rn56 / Rn30 / Rn112",
    "UT8": "Rn82 / Rn34 / Rn116",
    "UT9": "Rn90 / Rn38 / Rn120",
    "UT10": "Rn98 / Rn42 / Rn124",
    "UT11": "Rn106 / Rn46 / Rn128",
    "UT12": "Rn114 / Rn50 / Rn132",
    "UT13": "Rn122 / Rn54 / Rn136",
    "UT14": "Rn130 / Rn58 / Rn140",
    "UT15": "Rn138 / Rn62 / Rn144",
    "UT16": "Rn64 / Rn66 / Rn148"
    }

    valeurs_ut_si_cn_impaire = {
    "UT0": "Rn0 / Rn96 / Rn84 ",
    "UT1": "Rn8 / Rn100 / Rn88",
    "UT2": "Rn16 / Rn104 / Rn92",
    "UT3": "Rn24 / Rn108 / Rn96",
    "UT4": "Rn32 / Rn112 / Rn100",
    "UT5": "Rn40 / Rn116 / Rn104",
    "UT6": "Rn48 / Rn120 / Rn108",
    "UT7": "Rn56 / Rn124 / Rn112",
    "UT8": "Rn82 / Rn128 / Rn116",
    "UT9": "Rn90 / Rn132 / Rn120",
    "UT10": "Rn98 / Rn136 / Rn124",
    "UT11": "Rn106 / Rn140 / Rn128",
    "UT12": "Rn114 / Rn144 / Rn132",
    "UT13": "Rn122 / Rn148 / Rn136",
    "UT14": "Rn130 / Rn152 / Rn140",
    "UT15": "Rn138 / Rn156 / Rn144",
    "UT16": "Rn64 / Rn93 / Rn148"
    }

    
    # Définissez la fonction obtenir_numero_ut
    def obtenir_numero_ut(reglette, broche):
        if int(reglette) % 2 == 0:
            dictionnaire = dictionnaire_paire
        else:
            dictionnaire = dictionnaire_impaire

        for numero_ut, plage in dictionnaire.items():
            bornes = plage.split("<=")
            debut = int(bornes[0])
            fin = int(bornes[1])
            broche = int(broche)
            if debut <= broche <= fin:
                return numero_ut
        return "Inconnu"
    
    if request.method == 'POST':
        ne_data = request.form.get('ne')
    # Exemple d'analyse : recherche de la chaîne "NE =" suivie de "ETAT =" dans le texte
    matches = re.findall(r"NE\s*=\s*(\d+)-(\d+)-(\d+).*?ETAT\s*=\s*(.*)", ne_data)


    result_data = []  # Une liste pour stocker les résultats
    precedent_ur = None  # Variable pour stocker la valeur précédente d'UR
    precedent_cn = None  # Variable pour stocker la valeur précédente de CN
    precedent_ut = None  # Variable pour stocker la valeur précédente de UT
    data_attributes = {}  # Un dictionnaire pour stocker les attributs de données


    for match in matches:
        ur, reglette, broche, etat = match 

        # Accédez aux informations à partir du fichier JSON
        etat = etat.strip()
        etat_info = infos_etat.get(etat, {})
        
        # Utilisez les informations comme vous le souhaitez
        type_acces = etat_info.get("Type d'accès", "Information non disponible")
        signification = etat_info.get("Signification", "Information non disponible")
        intervenant = etat_info.get("Intervenant", "Information non disponible")
        
        # Créez un dictionnaire avec les données
        data_attributes[etat] = {
            "data-type-acces": type_acces,
            "data-signification": signification,
            "data-intervenant": intervenant
        }
        
        numero_ut = obtenir_numero_ut(reglette, broche)
        # Calculer le numéro de CN en fonction du numéro de réglette
        if reglette is not None:
            numero_cn = int(reglette) // 2
            if numero_cn % 2 != 0:
                numero_cn = numero_cn
        else:
            numero_cn = numero_cn - 1
        
        urtl = f"URTL:AFCN={ur}-{numero_cn},TYM=CSN,ENS=UT{numero_ut}"
    
        if precedent_cn == numero_cn and precedent_ut == numero_ut and precedent_ur == ur:
            if numero_cn % 2 == 0:
                rainures = valeurs_ut_si_cn_paire.get(f"UT{numero_ut}", "Aucune valeur trouvée")
            else:
                rainures = valeurs_ut_si_cn_impaire.get(f"UT{numero_ut}", "Aucune valeur trouvée")
            result_data.append({'NE': f'NE={ur}-{reglette}-{broche}', 'CN': f'CN:{numero_cn}-UT:{numero_ut}','ETAT':etat, 'Rainures': rainures})
        else:
            if numero_cn % 2 == 0:
                rainures = valeurs_ut_si_cn_paire.get(f"UT{numero_ut}", "Aucune valeur trouvée")
            else:
                rainures = valeurs_ut_si_cn_impaire.get(f"UT{numero_ut}", "Aucune valeur trouvée")
            result_data.append({'NE': f'NE={ur}-{reglette}-{broche}', 'CN': f'CN:{numero_cn}-UT:{numero_ut}','ETAT': etat, 'Rainures': rainures, 'URTL': urtl})

          
        precedent_ur = ur
        precedent_cn = numero_cn
        precedent_ut = numero_ut
        

    return render_template('Abfase.html', result=result_data, data_attributes=data_attributes)

@app.route('/Anoil', methods=['POST'])
def executer_Anoil():
    if request.method == 'POST':
        # Initialisation d'une liste pour stocker les résultats
        results = []
        
        # Initialisation d'un dictionnaire pour compter les occurrences
        occurrences = {}

        # Récupérer les données de l'utilisateur depuis le formulaire HTML
        donnees_utilisateur = request.form.get('ne')

        # Division des données en lignes
        lines = donnees_utilisateur.split('\n')

        # Parcourir chaque ligne et extraire ENS et P
        for line in lines:
            ens_match = re.search(r'ENS=(\d+)', line)
            p_match = re.search(r'P=\'(.*?)\'', line)

            if ens_match:
                ens = remove_leading_zeros(ens_match.group(1))
                if p_match:
                    p_hex = p_match.group(1)
                    # Extraire les deux derniers caractères
                    p_hex_last_two = p_hex[-2:]
                    # Convertir en décimal
                    p = str(int(p_hex_last_two, 16))
                else:
                    p = None
                
                # Recherche de la correspondance dans les données JSON
                correspondance = None
                if p:
                    for entry in anoil_ura['tableau'][1:]:
                        if entry[0] == ens and entry[1] == p:
                            correspondance = entry
                            break
                else:
                    for entry in anoil_ura['tableau'][1:]:
                        if entry[0] == ens:
                            correspondance = entry
                            break
                
                # Ajout des résultats
                if correspondance:
                    carte = correspondance[2]
                    urtl = correspondance[4]
                    position = correspondance[5]
                    information = correspondance[7]
                    
                    # Création d'une clé unique pour le résumé
                    key_str = f"{ens}_{p}"
                    
                    # Incrémentation du compteur d'occurrences
                    if key_str in occurrences:
                        occurrences[key_str] += 1
                    else:
                        occurrences[key_str] = 1

                    results.append({"ENS": ens, "P": p, "Carte": carte, "URTL": urtl, "Position": position, "Information": information, "Occurrences": occurrences[key_str]})

         # Trouver le nombre maximum d'occurrences pour chaque combinaison ENS-P
        max_occurrences = {}
        for result in results:
            key_str = f"{result['ENS']}_{result['P']}"
            if key_str in max_occurrences:
                max_occurrences[key_str] = max(max_occurrences[key_str], result['Occurrences'])
            else:
                max_occurrences[key_str] = result['Occurrences']

        # Filtrer les résultats pour ne conserver que ceux avec le nombre maximum d'occurrences
        filtered_results = [result for result in results if result['Occurrences'] == max_occurrences[f"{result['ENS']}_{result['P']}"]]

        # Trier les résultats par ordre croissant d'ENS et P
        sorted_results = sorted(filtered_results, key=lambda x: (int(x['ENS']), int(x['P']) if x['P'] is not None else 0))
        
        # Passer les résultats filtrés au modèle HTML
        return render_template('Odiag.html', results=sorted_results)

if __name__ == '__main__':
    app.run(debug=True)
