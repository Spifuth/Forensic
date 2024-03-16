import subprocess
import yaml

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

def find_files(partition):
    # Use fls to list and filter the files of interest in the partition
    command = f"fls -f ewf -r -o {partition['start']} {image_path} > {partition['name']}_fls.txt"
    run_command(command)
    with open(f"{partition['name']}_fls.txt", "r") as f:
        output = f.read()
    files = []
    for line in output.splitlines():
        if "d." in line:
            # Skip directories
            continue
        file_name, size, start, _ = line.split()
        files.append({
            "name": file_name,
            "size": size,
            "start": start,
        })
    return files

def extract_files(file_ids, partition, output_dir):
    # Use icat to extract the files based on their IDs
    for file_id in file_ids:
        command = f"icat -f ewf -o {partition['start']} {image_path} {file_id} > {output_dir}/{file_id}"
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
        files = find_files(partition)
        for file in files:
            if file["name"] in registry_hives:
                extract_files([file["start"]], partition, output_dir)

    # Extract user hives
    user_hives = [
        'Users\\*\\NTUSER.DAT',
        'Users\\*\\ntuser.dat.LOG1',
        'Users\\*\\ntuser.dat.LOG2',
    ]

    for partition in partitions:
        files = find_files(partition)
        for file in files:
            if file["name"] in user_hives:
                extract_files([file["start"]], partition, output_dir)

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

    extract_registry_and_user_hives(image_path, output_dir)
    extract_browser_data(image_path, output_dir)
    extract_logs(image_path, output_dir)
    extract_mft(image_path, output_dir)

if __name__ == "__main__":
    main()
