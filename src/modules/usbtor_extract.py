def extract_usbstor(registry_path):
    usbstor_data = {}
    try:
        with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
            i = 0
            while True:
                try:
                    sub_key_name = _winreg.EnumValue(key, i)[0]
                    value = _winreg.QueryValueEx(key, sub_key_name)[0]
                    usbstor_data[sub_key_name] = value
                    i += 1
                except WindowsError:
                    break
    except Exception as e:
        print("Erreur lors de l'extraction des données USBSTOR :", e)
    return usbstor_data
