import os
import shutil

def swap_fastq_files(root_dir):
    # Parcourir tous les répertoires et sous-répertoires
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Vérifier les fichiers _R1_001.fastq.gz et _R2_001.fastq.gz
            if file.endswith('_R1_001.fastq.gz'):
                r1_path = os.path.join(subdir, file)
                r2_path = r1_path.replace('_R1_001.fastq.gz', '_R2_001.fastq.gz')

                if os.path.exists(r2_path):
                    # Renommer temporairement pour éviter les conflits de nom
                    temp_r1_path = r1_path + '.temp'
                    shutil.move(r1_path, temp_r1_path)
                    shutil.move(r2_path, r1_path)
                    shutil.move(temp_r1_path, r2_path)
                    
                    print(f"Swapped: {r1_path} <-> {r2_path}")

# Spécifiez le répertoire racine à partir duquel commencer la recherche
root_directory = '/home/jordan23/scratch/def-ytanaka/jordan23/Patient_scRNA-main/test/Reefer'
swap_fastq_files(root_directory)
