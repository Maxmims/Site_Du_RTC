import copy

# Votre structure JSON d'origine
original_data = {
    "ALV3": {
        "RN1": ["03-001", "03-002", "03-003", "03-004", "03-005", "03-006", "03-007", "03-008",
                "03-001", "03-002", "03-003", "03-004", "03-005", "03-006", "03-007", "03-008"]
    }
}

# Fonction pour modifier les valeurs de RN
def modify_rn_values(data):
    updated_data = copy.deepcopy(data)
    prev_rn_values = None
    for rn_key in sorted(updated_data["ALV3"]):
        rn_values = updated_data["ALV3"][rn_key]
        if prev_rn_values is not None:
            for i in range(len(rn_values)):
                prefix, last_value = rn_values[i].split('-')
                new_last_value = str(int(last_value) + i).zfill(3)
                rn_values[i] = f"{prefix}-{new_last_value}"
        prev_rn_values = rn_values
    return updated_data

# Appel de la fonction pour modifier les valeurs
modified_data = modify_rn_values(original_data)

# Affichage du résultat modifié
print(modified_data)


