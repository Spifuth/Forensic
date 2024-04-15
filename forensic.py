import subprocess
import sys
import re

start = None
windows = None
system32 = None
config = None
users = None
SYSTEM = None
SOFTWARE = None
SECURITY = None
SAM = None
DEFAULT = None
NTUSER = None
NTUSERLOG1 = None
NTUSERLOG2 = None
AppData = None
Local = None
Microsoft = None
Google = None
Mozilla = None
Firefox = None
Chrome = None
Windows = None
Edge = None
User_data = None
InetCache = None
Profiles = None
winevt = None
Logs = None
Security_evtx = None
System_evtx = None
Roaming = None


registry_hives = [
    'SystemRoot\\System32\\Config\\SYSTEM',
    'SystemRoot\\System32\\Config\\SOFTWARE',
    'SystemRoot\\System32\\Config\\SECURITY',
    'SystemRoot\\System32\\Config\\SAM',
    'SystemRoot\\System32\\Config\\DEFAULT',
]
user_hives = [
    'Users\\*\\NTUSER.DAT',
    'Users\\*\\ntuser.dat.LOG1',
    'Users\\*\\ntuser.dat.LOG2',
]
browser_data_paths = [
    'Users\\*\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default',
    'Users\\*\\AppData\\Local\\Microsoft\\Windows\\INetCache',
    'Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\Default',
    'Users\\*\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*.default',
]
log_paths = [
    'SystemRoot\\System32\\winevt\\Logs\\Security.evtx',
    'SystemRoot\\System32\\winevt\\Logs\\System.evtx',
]

def extract_mmls_data(line):
    global start
    match = re.search(r'\s+basic data partition', line, re.I)
    if match:
        start = int(line.split()[2])
        print(f'Start Sector of Data Partition: {start}')

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

def extract_fls_data_ntuser(line):
    global ntuser
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'ntuser.dat':
        ntuser = inode
        print(f'NTUSER')


def extract_fls_data_ntuserlog1(line):
    global ntuserlog1
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'ntuser.dat.LOG1':
        ntuserlog1 = inode
        print(f'NTUSERLOG1')

def extract_fls_data_ntuserlog2(line):
    global ntuserlog2
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'ntuser.dat.LOG2':
        ntuserlog2 = inode
        print(f'NTUSERLOG2')

def extract_fls_data_system(line):
    global SYSTEM
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'system':
        SYSTEM = inode
        print(f'SYSTEM')

def extract_fls_data_software(line):
    global SOFTWARE
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'software':
        SOFTWARE = inode
        print(f'SOFTWARE')

def extract_fls_data_security(line):
    global SECURITY
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'security':
        SECURITY = inode
        print(f'SECURITY')

def extract_fls_data_sam(line):
    global SAM
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'sam':
        SAM = inode
        print(f'SAM')

def extract_fls_data_default(line):
    global DEFAULT
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'default':
        DEFAULT = inode
        print(f'DEFAULT')

def extract_fls_data_appdata(line):
    global AppData
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'appdata':
        AppData = inode
        print(f'AppData')

def extract_fls_data_local(line):
    global Local
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'local':
        Local = inode
        print(f'Local')

def extract_fls_data_microsoft(line):
    global Microsoft
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'microsoft':
        Microsoft = inode
        print(f'Microsoft')

def extract_fls_data_google(line):
    global Google
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'google':
        Google = inode
        print(f'Google')

def extract_fls_data_mozilla(line):
    global Mozilla
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'Mozilla':
        Mozilla = inode
        print(f'Mozilla')

def extract_fls_data_firefox(line):
    global Firefox
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'firefox':
        Firefox= inode
        print(f'Firefox')

def extract_fls_data_Chrome(line):
    global Chrome
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'chrome':
        Chrome = inode
        print(f'Chrome')

def extract_fls_data_windows(line):
    global Windows
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'windows':
        Windows = inode
        print(f'Windows')

def extract_fls_data_edge(line):
    global Edge
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'edge':
        Edge = inode
        print(f'Edge')

def extract_fls_data_user_data(line):
    global User_Data
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'user data':
        User_Data = inode
        print(f'User Data')

def extract_fls_data_inetcache(line):
    global INetCache
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'inetcache':
        INetCache = inode
        print(f'INetCache')

def extract_fls_data_profiles(line):
    global Profiles
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'profiles':
        Profiles = inode
        print(f'Profiles')

def extract_fls_data_winevt(line):
    global winevt
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'winevt':
        winevt = inode
        print(f'winevt')

def extract_fls_data_logs(line):
    global Logs
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'logs':
        Logs = inode
        print(f'Logs')

def extract_fls_data_security_evtx(line):
    global security_evtx
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'security.evtx':
        security_evtx = inode
        print(f'Security.evtx')

def extract_fls_data_system_evtx(line):
    global system_evtx
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'system.evtx':
        system_evtx = inode
        print(f'DEFAULT')

def extract_fls_data_roaming(line):
    global Roaming
    line_parts = line.split()
    file_type = line_parts[0]
    inode = line_parts[1].replace(':', '')
    name = line_parts[2]
    if name.lower() == 'roaming':
        Roaming = inode
        print(f'Roaming')

def retrieve_file(disk, inode, output_filename):
    subprocess.run(['icat', disk, inode], stdout=open(output_filename, 'wb'))

def retrieve_hive_files(disk, hives):
    for hive in hives:
        # Replace * with the correct user name
        hive_path = hive.replace('*', users)
        # Extract inode for the hive file
        fls_hive = subprocess.Popen(['fls', '-o', str(start), disk, str(hive_path)], stdout=subprocess.PIPE)
        stdout, stderr = fls_hive.communicate()
        for line in stdout.decode().splitlines():
            inode = line.split()[1].replace(':', '')
            output_filename = {hive.split}
            print(f"Retrieving {output_filename}...")
            retrieve_file(disk, inode, output_filename)
            print(f"{output_filename} retrieved successfully.")

user_names = []

disk = sys.argv[1]

# Extract MMLS data
mmls = subprocess.Popen(['mmls', disk], stdout=subprocess.PIPE)
stdout, stderr = mmls.communicate()
for line in stdout.decode().splitlines():
    extract_mmls_data(line)

# Extract FLS data for Windows
fls_windows = subprocess.Popen(['fls', '-o', str(start), disk], stdout=subprocess.PIPE)
stdout, stderr = fls_windows.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_windows(line)

# Extract FLS data for System32
fls_system32 = subprocess.Popen(['fls', '-o', str(start), str(windows), disk], stdout=subprocess.PIPE)
stdout, stderr = fls_system32.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_system32(line)

# Extract FLS data for Config
fls_config = subprocess.Popen(['fls', '-o', str(start), str(system32), disk], stdout=subprocess.PIPE)
stdout, stderr = fls_config.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_config(line)

# Extract FLS data for Users
fls_users = subprocess.Popen(['fls', '-o', str(start), disk], stdout=subprocess.PIPE)
stdout, stderr = fls_users.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_users(line)

# Extract FLS data for NTUSER.DAT
fls_ntuser_dat = subprocess.Popen(['fls', '-o', str(start), disk, str(users)], stdout=subprocess.PIPE)
stdout, stderr = fls_ntuser_dat.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_ntuser(line)
    
# Extract FLS data for NTUSER.DAT.LOG1
fls_ntuser_dat_log1 = subprocess.Popen(['fls', '-o', str(start), disk, str(users)], stdout=subprocess.PIPE)
stdout, stderr = fls_ntuser_dat_log1.communicate()
for line in stdout.decode().splitlines():   
    extract_fls_data_ntuserlog1(line)

# Extract FLS data for NTUSER.DAT.LOG2
fls_ntuser_dat_log2 = subprocess.Popen(['fls', '-o', str(start), disk, str(users)], stdout=subprocess.PIPE)
stdout, stderr = fls_ntuser_dat_log2.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_ntuserlog2(line)

# Extract FLS data for SYSTEM
fls_SYSTEM = subprocess.Popen(['fls', '-o', str(start), disk, str(config)], stdout=subprocess.PIPE)
stdout, stderr = fls_SYSTEM.communicate()
for line in stdout.decode().splitlines():
    extract_fls_SYSTEM(line)

# Extract FLS data for SOFTWARE
fls_SOFTWARE = subprocess.Popen(['fls', '-o', str(start), disk, str(config)], stdout=subprocess.PIPE)
stdout, stderr = fls_SOFTWARE.communicate()
for line in stdout.decode().splitlines():
    extract_fls_SOFTWARE(line)


# Extract FLS data for SECURITY
fls_SECURITY = subprocess.Popen(['fls', '-o', str(start), disk, str(config)], stdout=subprocess.PIPE)
stdout, stderr = fls_SECURITY.communicate()
for line in stdout.decode().splitlines():
    extract_fls_SECURITY(line)

# Extract FLS data for SAM
fls_SAM = subprocess.Popen(['fls', '-o', str(start), disk, str(config)], stdout=subprocess.PIPE)
stdout, stderr = fls_SAM.communicate()
for line in stdout.decode().splitlines():
    extract_fls_SAM(line)

# Extract FLS data for DEFAULT
fls_default = subprocess.Popen(['fls', '-o', str(start), disk, str(config)], stdout=subprocess.PIPE)
stdout, stderr = fls_default.communicate()
for line in stdout.decode().splitlines():
    extract_fls_default(line)

# Extract FLS data for APPDATA
fls_AppData = subprocess.Popen(['fls', '-o', str(start), disk, str(users)], stdout=subprocess.PIPE)
stdout, stderr = fls_AppData.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_appdata(line)

# Extract FLS data for LOCAL
fls_Local = subprocess.Popen(['fls', '-o', str(start), disk, str(AppData)], stdout=subprocess.PIPE)
stdout, stderr = fls_Local.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Local(line)

# Extract FLS data for MICROSOFT
fls_Microsoft = subprocess.Popen(['fls', '-o', str(start), disk, str(Local)], stdout=subprocess.PIPE)
stdout, stderr = fls_Microsoft.communicate()
for line in stdout.decode().splitlines():
    extract_fls_SOFTWARE(line)

# Extract FLS data for GOOGLE
fls_Google = subprocess.Popen(['fls', '-o', str(start), disk, str(Local)], stdout=subprocess.PIPE)
stdout, stderr = fls_Google.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Google(line)

# Extract FLS data for MOZILLA
fls_Mozilla = subprocess.Popen(['fls', '-o', str(start), disk, str(Local)], stdout=subprocess.PIPE)
stdout, stderr = fls_Mozilla.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Mozilla(line)

# Extract FLS data for FIREFOX
fls_Firefox = subprocess.Popen(['fls', '-o', str(start), disk, str(Mozilla)], stdout=subprocess.PIPE)
stdout, stderr = fls_Firefox.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Firefox(line)

# Extract FLS data for CHROME
fls_Chrome = subprocess.Popen(['fls', '-o', str(start), disk, str(Google)], stdout=subprocess.PIPE)
stdout, stderr = fls_Chrome.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Chrome(line)

# Extract FLS data for WINDOWS
fls_Windows = subprocess.Popen(['fls', '-o', str(start), disk, str(Microsoft)], stdout=subprocess.PIPE)
stdout, stderr = fls_Windows.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Windows(line)

# Extract FLS data for EDGE
fls_Edge = subprocess.Popen(['fls', '-o', str(start), disk, str(Microsoft)], stdout=subprocess.PIPE)
stdout, stderr = fls_Edge.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Edge(line)

# Extract FLS data for USER_DATA
fls_USER_DATA = subprocess.Popen(['fls', '-o', str(start), disk, str(Edge)], stdout=subprocess.PIPE)
stdout, stderr = fls_USER_DATA.communicate()
for line in stdout.decode().splitlines():
    extract_fls_user_data(line)

# Extract FLS data for INETCACHE
fls_InetCache = subprocess.Popen(['fls', '-o', str(start), disk, str(Windows)], stdout=subprocess.PIPE)
stdout, stderr = fls_InetCache.communicate()
for line in stdout.decode().splitlines():
    extract_fls_data_inetcache(line)

# Extract FLS data for PROFILES
fls_Profiles = subprocess.Popen(['fls', '-o', str(start), disk, str(Firefox)], stdout=subprocess.PIPE)
stdout, stderr = fls_Profiles.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Profiles(line)

# Extract FLS data for WINEVT
fls_winevt = subprocess.Popen(['fls', '-o', str(start), disk, str(system32)], stdout=subprocess.PIPE)
stdout, stderr = fls_winevt.communicate()
for line in stdout.decode().splitlines():
    extract_fls_winevt(line)

# Extract FLS data for LOGS
fls_Logs = subprocess.Popen(['fls', '-o', str(start), disk, str(winevt)], stdout=subprocess.PIPE)
stdout, stderr = fls_Logs.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Logs(line)

# Extract FLS data for SECURITY_EVTX
fls_Security_evtx = subprocess.Popen(['fls', '-o', str(start), disk, str(Logs)], stdout=subprocess.PIPE)
stdout, stderr = fls_Security_evtx.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Security_evtx(line)

# Extract FLS data for SYSTEM_EVTX
fls_System_evtx = subprocess.Popen(['fls', '-o', str(start), disk, str(Logs)], stdout=subprocess.PIPE)
stdout, stderr = fls_System_evtx.communicate()
for line in stdout.decode().splitlines():
    extract_fls_System_evtx(line)

# Extract FLS data for ROAMING
fls_Roaming = subprocess.Popen(['fls', '-o', str(start), disk, str(AppData)], stdout=subprocess.PIPE)
stdout, stderr = fls_Roaming.communicate()
for line in stdout.decode().splitlines():
    extract_fls_Roaming(line)

# List all users
print("Available users:")
for i, (name, _) in enumerate(user_names):
    print(f"{i+1}. {name}")

# Prompt user to select a user
user_choice = input("Enter the number of the user to retrieve hive files: ")
user_choice = int(user_choice)

if user_choice < 1 or user_choice > len(user_names):
    print("Invalid choice")
else:
    selected_user = user_names[user_choice - 1]
    print(f"Retrieving hive files for the selected user {selected_user[0]}...")
    retrieve_hive_files(disk, registry_hives + user_hives)
    print("Hive files retrieved successfully.")
