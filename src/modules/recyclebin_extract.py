import os

def extract_recycle_bin_contents(image_path):
    recycle_bin_contents = []
    recycle_bin_path = os.path.join(image_path, "C:\\$Recycle.Bin")
    try:
        for root, dirs, files in os.walk(recycle_bin_path):
            for file in files:
                recycle_bin_contents.append(os.path.join(root, file))
    except Exception as e:
        print("Erreur lors de l'extraction du contenu de la corbeille :", e)
    return recycle_bin_contents
