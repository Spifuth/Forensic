def read_ewf(file_path):
    try:
        ewf_handle = pyewf.handle()
        ewf_handle.open(file_path)
        
        # Affichage des informations générales sur l'image
        print("Informations générales sur l'image :")
        print("Nom : ", ewf_handle.get_media_name())
        print("Taille : ", ewf_handle.get_media_size())
        print("Type : ", ewf_handle.get_media_type())
        print("Nombre de partitions : ", ewf_handle.get_number_of_partitions())
        
        # Affichage des informations sur chaque partition
        for i in range(ewf_handle.get_number_of_partitions()):
            partition_info = ewf_handle.get_partition_info(i)
            print("\nPartition", i+1, " :")
            print("Type : ", partition_info['type'])
            print("Offset : ", partition_info['start_offset'])
            print("Taille : ", partition_info['size'])
            
        # Fermeture du handle
        ewf_handle.close()
        
    except pyewf.EwfError as e:
        print("Erreur lors de la lecture de l'image EWF :", e)
