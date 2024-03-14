import _winreg

def extract_userassist(registry_path):
    userassist_data = {}
    try:
        with _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, registry_path) as key:
            i = 0
            while True:
                try:
                    sub_key_name = _winreg.EnumValue(key, i)[0]
                    value = _winreg.QueryValueEx(key, sub_key_name)[0]
                    userassist_data[sub_key_name] = value
                    i += 1
                except WindowsError:
                    break
    except Exception as e:
        print("Erreur lors de l'extraction des données UserAssist :", e)
    return userassist_data
