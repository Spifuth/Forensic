def extract_system32_config_contents(image_path):
    system32_config_contents = []
    system32_config_path = os.path.join(image_path, "Windows\\system32\\config")
    try:
        for root, dirs, files in os.walk(system32_config_path):
            for file in files:
                system32_config_contents.append(os.path.join(root, file))
    except Exception as e:
        print("Erreur lors de l'extraction du contenu de system32\\config :", e)
    return system32_config_contents
