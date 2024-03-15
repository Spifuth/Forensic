import subprocess
import yaml
import os
import sys

def run_command(command):
    # Execute a command line command and return the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        raise Exception(f"Command failed: {command}\n{error.decode()}")
    return output.decode()

def list_partitions(image_path):
    # Use mmls to list the partitions of the disk image
    command = f"mmls -f ewf {image_path}"
    output = run_command(command)
    partitions = []
    for line in output.splitlines():
        if "Ewf" in line:
            start, size, type_str, name = line.split()
            partitions.append({
                "start": start,
                "size": size,
                "type": type_str,
                "name": name,
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
    # Orchestrate the extraction and processing process
    image_path = sys.argv[1]
    output_dir = sys.argv[2]

    extract_registry_and_user_hives(image_path, output_dir)
    extract_browser_data(image_path, output_dir)
    extract_logs(image_path, output_dir)
    extract_mft(image_path, output_dir)

def display_help():
    print("Usage: python forensic.py <image_path> <output_dir>")
    print("Extracts and processes data from a disk image.")
    print("Arguments:")
    print("  image_path: Path to the disk image.")
    print("  output_dir: Directory to store the extracted files.")

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ["-h", "--help"]:
        display_help()
    else:
        main()
