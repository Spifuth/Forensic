import subprocess
import sys
import re

start = None
windows = None
system32 = None
config = None
users = None

def extract_mmls_data(line):
    global start
    match = re.search(r'\s+basic data partition', line, re.I)
    if match:
        start = int(line.split()[2])
        print(f'start sector of basic data partition: {start}')

def extract_fls_data_windows(line):
    global windows
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'windows':
        windows = inode
        print(f'Inode of the folder {name}: {windows}')

def extract_fls_data_system32(line):
    global system32
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'system32':
        system32 = inode
        print(f'Inode of the folder {name}: {system32}')

def extract_fls_data_config(line):
    global config
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'config':
        config = inode
        print(f'Inode of the folder {name}: {config}')

def extract_fls_data_users(line):
    global users
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'users':
        users = inode
        print(f'Inode of the folder {name}: {users}')

def extract_fls_data_all_users(line):
    global all_users
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    indoe = split()
    print(f'Inode of the user {name}: {inode}')
    return name

disk = sys.argv[1]

mmls = subprocess.Popen(['mmls', disk], stdout=subprocess.PIPE)
stdout, stderr = mmls.communicate()
for line in stdout.decode().splitlines():
    extract_mmls_data(line)

fls_windows = subprocess.Popen(['fls', '-o', str(start), disk], stdout=subprocess.PIPE)
stdout, stderr = fls_windows.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_windows(line)

fls_system32 = subprocess.Popen(['fls', '-o', str(start), disk, str(windows)], stdout=subprocess.PIPE)
stdout, stderr = fls_system32.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_system32(line)

fls_config = subprocess.Popen(['fls', '-o', str(start), disk, str(system32)], stdout=subprocess.PIPE)
stdout, stderr = fls_config.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_config(line)

fls_users = subprocess.Popen(['fls', '-o', str(start), disk], stdout=subprocess.PIPE)
stdout, stderr = fls_users.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_users(line)

fls_all_users = subprocess.Popen(['fls', '-o', str(start), disk, str(users)], stdout=subprocess.PIPE)
stdout, stderr = fls_all_users.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_all_users(line)
