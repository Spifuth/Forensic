import subprocess
import re

def get_metadata(disk):
    mmls = subprocess.Popen(['mmls', disk], stdout=subprocess.PIPE)
    stdout, stderr = mmls.communicate()

    start = None
    for line in stdout.decode().splitlines():
        match = re.search(r'\s+Basic data partition', line)
        if match:
            start = int(line.split()[2])
            print(f'Start sector of Basic Data Partition: {start}')
            break
    
    return start

def extract_fls_data(disk, start, folder):
    fls = subprocess.Popen(['fls', '-o', str(start), disk], stdout=subprocess.PIPE)
    stdout, stderr = fls.communicate()

    windows_id = None
    for line in stdout.decode().splitlines():
        line_parts = line.split()
        file_type = line_parts[0]
        inode = line_parts[1].replace(':', '')
        name = line_parts[2]
        if name == folder:
            windows_id = inode
            print(f'Inode of the folder "{folder}": {windows_id}')
            break
    
    return windows_id
