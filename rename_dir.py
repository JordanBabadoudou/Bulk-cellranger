import os
import pandas as pd

# Charger le fichier associant les IDs aux noms d'expérience
df = pd.read_csv("/home/jordan23/scratch/def-ytanaka/jordan23/Patient_scRNA-main/dir_restart.csv", delimiter="\t")

# Créer un dictionnaire pour faire correspondre les IDs aux noms d'expérience
id_to_experiment = dict(zip(df['ID'], df['Experiment accession']))

# Définir le répertoire contenant vos dossiers à renommer
directory = '/home/jordan23/scratch/def-ytanaka/jordan23/Patient_scRNA-main/text'

experience_counts = {}

# Parcourir les dossiers dans le répertoire
for folder_name in os.listdir(directory):
    # Extraire l'ID du dossier
    folder_id = folder_name.split('_')[0]

    # Vérifier si cet ID existe dans le dictionnaire
    if folder_id in id_to_experiment:
        # Récupérer le nom d'expérience correspondant à cet ID
        experiment_name = id_to_experiment[folder_id]

	# Vérifier si ce nom d'expérience existe déjà dans le répertoire
        if experiment_name in experience_counts:
            # S'il existe, incrémenter le compteur
            experience_counts[experiment_name] += 1
        else:
            # Sinon, initialiser le compteur à 1
            experience_counts[experiment_name] = 1

        # Construire le nouveau nom du dossier avec le nom d'expérience et le compteur
        new_folder_name = f"{experiment_name}_L00{experience_counts[experiment_name]}"

        # Renommer le dossier
        os.rename(os.path.join(directory, folder_name), os.path.join(directory, new_folder_name))
        print(f"Dossier {folder_name} renommé en {new_folder_name}")
    else:
        print(f"Aucune correspondance trouvée pour l'ID {folder_id}")

