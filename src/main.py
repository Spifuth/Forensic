import subprocess
import sys

from modules import *

def main():
    disk = input("Entrez le chemin de l'image disque : ").strip()
    folder = input("Entrez le nom du dossier à rechercher : ").strip()

    # Récupérer les métadonnées du fichier et les informations sur les partitions potentielles
    start = get_metadata(disk)

    # Extraire les données de fls
    windows_id = extract_fls_data(disk, start, folder)

if __name__ == "__main__":
<<<<<<< HEAD
    file_path = "chemin/vers/votre/image.E01"
    fetchmeta.read_ewf(file_path)


#Coucou je suis la
=======
    main()
>>>>>>> b8551b2 (structuration)
