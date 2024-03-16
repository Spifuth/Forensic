import subprocess
import yaml
import sys
import re

def run_command(command):
    # Execute a command line command and return the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        raise Exception(f"Command failed: {command}\n{error.decode()}")
    return output.decode()

def list_partitions(image_path):
    # Use mmls to list the partitions of the disk image
    command = f"mmls -r {image_path}"
    output = run_command(command)
    # regex that extract paritions informations 
    partition_pattern = re.compile(r"\d{3}:\s+(?P<Slot>\S+)\s+(?P<Start>\d+)\s+(?P<End>\d+)\s+(?P<Length>\d+)\s+(?P<Description>.+)")

    partitions = []
    for line in output.splitlines():
        match = partition_pattern.match(line)
        if match:
            partition_info = match.groupdict()
            partitions.append({
                "start" : partition_info['Start'],
                "size"  : partition_info['Length'],
                "type"  : partition_info['Description'],
                "name"  : ""
            })
    return partitions

def find_files(image_path, partition):
    # Use fls to list and filter the files of interest in the partition
    command = f"fls -o {partition['start']} -f ntfs -r {image_path} > output.txt"
    run_command(command)
    files = []
    with open(f"output.txt", "r") as f:
        while True:
            data = f.readline()
            if not data:
                break
            splited_data = data.split()
            n = len(splited_data)
            # ['+', '-/r', '*', '35277-128-5:', 'fil.pak.DATA']
            for item in splited_data:
                splited_item = item.split("-")
                # Add file only
                if len(splited_item) == 3:
                    file_id = splited_item[0]
                    if  "r/r"  in splited_data:
                        files.append({
                            "id" : file_id,
                            "name" : splited_data[n - 1]
                        })
    return files

def extract_file(image_path, file, partition, output_dir):
    # Use icat to extract the files based on their IDs
    # icat -o 0000673792 -r disk.E01 35643
    command = f"icat -o {partition['start']} {image_path} {file['id']} > {output_dir}/{file['name']}"
    run_command(command)

def extract_registry_and_user_hives(image_path, output_dir):
    # Extract registry hives
    registry_hives = [
        'SystemRoot\\System32\\Config\\SYSTEM',
        'SystemRoot\\System32\\Config\\SOFTWARE',
        'SystemRoot\\System32\\Config\\SECURITY',
        'SystemRoot\\System32\\Config\\SAM',
        'SystemRoot\\System32\\Config\\DEFAULT',
    ]

    partitions = list_partitions(image_path)
    for partition in partitions:
        if "data" in partition['type']:
            files = find_files(image_path, partition)
            for file in files:
                print(f"Extracting: {file}...\n")
                extract_file(image_path, file, partition, output_dir)
    return 

    # Extract user hives
    user_hives = [
        'Users\\*\\NTUSER.DAT',
        'Users\\*\\ntuser.dat.LOG1',
        'Users\\*\\ntuser.dat.LOG2',
    ]

    print(f"PARITION: {partitions}")
    # for partition in partitions:
    #     files = find_files(image_path, partition)
    #     for file in files:
    #         if file["name"] in user_hives:
    #             print(f"File: {file}")
    #             extract_files(image_path, [file["start"]], partition, output_dir)

def extract_browser_data(image_path, output_dir):
    browser_data_paths = [
        'Users\\*\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default',
        'Users\\*\\AppData\\Local\\Microsoft\\Windows\\INetCache',
        'Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\Default',
        'Users\\*\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*.default',
    ]

    partitions = list_partitions(image_path)
    for partition in partitions:
        files = find_files(partition)
        for path in browser_data_paths:
            for file in files:
                if file["name"].startswith(path):
                    extract_files([file["start"]], partition, output_dir)

def extract_logs(image_path, output_dir):
    log_paths = [
        'SystemRoot\\System32\\winevt\\Logs\\Security.evtx',
        'SystemRoot\\System32\\winevt\\Logs\\System.evtx',
    ]

    partitions = list_partitions(image_path)
    for partition in partitions:
        files = find_files(partition)
        for path in log_paths:
            for file in files:
                if file["name"] == path:
                    extract_files([file["start"]], partition, output_dir)

def extract_mft(image_path, output_dir):
    mft_path = 'SystemRoot\\$MFT'

    partitions = list_partitions(image_path)
    for partition in partitions:
        files = find_files(partition)
        for file in files:
            if file["name"] == mft_path:
                extract_files([file["start"]], partition, output_dir)

def main():
    # Orchestrez le processus d'extraction et de traitement des fichiers
    image_path = sys.argv[1]
    output_dir = sys.argv[2]

    # res = list_partitions(image_path)
    # print(f"Res: {res}")

    extract_registry_and_user_hives(image_path, output_dir)
    # extract_browser_data(image_path, output_dir)
    # extract_logs(image_path, output_dir)
    # extract_mft(image_path, output_dir)

if __name__ == "__main__":
    main()
