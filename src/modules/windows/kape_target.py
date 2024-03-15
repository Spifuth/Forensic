def extract_kape_files(kape_file_path, image_path):
    extracted_files = []
    
    try:
        with open(kape_file_path, 'r') as file:
            kape_data = file.read()
            
            # Supprimer les commentaires dans le fichier Kape
            kape_data = '\n'.join([line for line in kape_data.split('\n') if not line.strip().startswith('#')])
            
            # Charger les données Kape
            kape_data = yaml.safe_load(kape_data)
            
            # Parcourir chaque cible dans le fichier Kape
            for target in kape_data['Targets']:
                category = target['Category']
                file_mask = target['FileMask']
                
                # Construire le chemin complet à extraire en utilisant le chemin de l'image et le chemin spécifié dans le fichier Kape
                path = target['Path'].replace("%user%", os.environ['USERNAME'])
                full_path = os.path.join(image_path, path)
                
                # Vérifier si le chemin existe
                if os.path.exists(full_path):
                    # Récupérer les fichiers correspondants au masque spécifié
                    files = [f for f in os.listdir(full_path) if f.startswith(file_mask)]
                    extracted_files.extend([os.path.join(path, f) for f in files])
                    
    except Exception as e:
        print("Erreur lors de l'extraction des fichiers Kape :", e)
    
    return extracted_files
