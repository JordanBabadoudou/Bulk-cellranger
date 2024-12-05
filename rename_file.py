# -*- coding: utf-8 -*-
import os
import re

# Définir le répertoire contenant les répertoires à examiner
root_directory = '/home/jordan23/scratch/def-ytanaka/jordan23/Patient_scRNA-main/text/'

# Parcourir les répertoires dans le répertoire racine
for subdir, _, _ in os.walk(root_directory):
    # Compter le nombre de fichiers fastq dans le répertoire
    fastq_files = [f for f in os.listdir(subdir) if f.endswith('.fastq.gz')]
    num_fastq_files = len(fastq_files)

    # Si le répertoire contient moins de 3 fichiers fastq
    if num_fastq_files <= 3:
        parent_dir = os.path.basename(subdir)

        # Récupérer le préfixe L00X pour le nom du répertoire parent
        l00_prefix = re.findall(r'_L0\d+', parent_dir)
        l00_prefix = l00_prefix[0] if l00_prefix else ""

        # Trier les fichiers fastq par taille croissante
        fastq_files.sort(key=lambda x: os.path.getsize(os.path.join(subdir, x)))

        # Corriger le nom du parent
        if '_' in parent_dir:
            name_dir, _ = parent_dir.split('_', 1)
        else:
            name_dir = parent_dir

        # Parcourir les fichiers fastq dans le répertoire
        for i, fastq_file in enumerate(fastq_files):
            # Déterminer le suffixe en fonction du nom du fichier et de la taille
            if i == 0:  # Le plus petit fichier
                suffix = "I1"
            elif i == len(fastq_files) - 1:  # Le plus grand fichier
                suffix = "R2"
            else:
                suffix = "R1"

            # Construire le nouveau nom de fichier
            new_filename = f"{name_dir}_S1{l00_prefix}_{suffix}_001.fastq.gz"

            # Construire le chemin complet du fichier d'origine et du nouveau fichier
            old_filepath = os.path.join(subdir, fastq_file)
            new_filepath = os.path.join(subdir, new_filename)

            # Renommer le fichier
            os.rename(old_filepath, new_filepath)
            print(f"Fichier {fastq_file} renommé en {new_filename} dans {subdir}")

    else:
        print("Nombre de fichiers supérieur à la taille requise")
