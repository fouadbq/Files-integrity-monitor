from os import walk, path, geteuid

from sys import argv,exit

from datetime import datetime

from shutil import copy

from time import sleep

from colorama import Fore, Style

from json import dump, load

from getpass import getuser

import hashlib, csv, signal

# calculate  the hash using the SHA-256 algorithm
def Hash_File(file_path):

    # Open and read the file ( in binary mode )

    with open(file_path, 'rb') as f:

        # Read the file content  in chunks

        chunk = f.read(1024)

        # Instanciating a new SHA-256

        sha256 = hashlib.sha256()

        # Loop through the file contents and update the hash object

        while len(chunk) > 0:

            sha256.update(chunk)

            chunk = f.read(1024)

    return sha256.hexdigest()

#Generate the name and path of the backup file
def Get_BackUp_FilePath(file_path):
    return 'Monitoring_Repo/BackUp_Files_Repo/'+path.splitext(path.basename(file_path))[0]+'_bck'+path.splitext(path.basename(file_path))[1]


def Initialize_Monitoring_Repo(Root):

    # Get a list of all file paths in the specified directory and its subdirectories

    files_paths = [path.join(root, file) for root, _ , files in walk(Root) for file in files]

    # to avoid duplication of checksum files   in case there was an already created one

    if path.getsize('Monitoring_Repo/checksums.csv') > 0:

        print('A checksum register already exists in this directory, would you like to overwrite it ?')

        option = input('\t>> Press < y >  to confirm  or < c > to cancel :\t')

        if option == 'y':

            with open('Monitoring_Repo/checksums.csv', 'w', newline='') :    pass

        elif option == 'c':

            return

        else:

            print('Unvalid input, try again !')

    # Open the Updates_Repo.csv file in append mode

    with open('Monitoring_Repo/checksums.csv', 'a', newline='') as Repo:

        # Create a CSV writer object

        writer = csv.writer(Repo, delimiter=',')

        # For each file path in the list, write a row to the Updates_Repo.csv file containing the current timestamp, the file path, and its hash value

        for file_path in files_paths:

            writer.writerow([datetime.now(), file_path, Hash_File(file_path)])

            # Create a backup file for the file being monitored

            backup_path = Get_BackUp_FilePath(file_path)

            with open(backup_path, 'w') as backup_file:

                pass

            copy(file_path, backup_path)

    # Create an empty Alteration_History.json file

    with open('Monitoring_Repo/Alteration_History.json', 'w'):

        pass


def Update_Register(Root):

    print('Are you sure you want to overwrite the Monitoring repository files ?')

    option = input('Press < y > to continue the updating  or < n >  to skip ')

    if option == 'y':

        paths_list = []

        with open('Monitoring_Repo/checksums.csv', 'r') as checksum_register_file:

            checksum_register = list(csv.reader(checksum_register_file))

        for root, dirs, files in walk(Root):

            for file in files:

                paths_list.append(path.join(root, file))

        for file_path in paths_list:

            for row in checksum_register:

                backup_path = Get_BackUp_FilePath(file_path)

                if file_path in row:

                    checksum_register[checksum_register.index(

                        row)] = [datetime.now(), file_path, Hash_File(file_path)]

                else:

                    # create the a new backup file

                    with open(backup_path, 'w'):

                        pass

                # Copy the updated file into the backup repositpry    shutil.copy(source, destination)

                copy(file_path, backup_path)

        with open('Monitoring_Repo/checksums.csv', 'w', newline='') as csvfile:

            writer = csv.writer(csvfile, delimiter=',')

            for row in checksum_register:

                writer.writerow(row)

        with open('Monitoring_Repo/Alteration_History.json', 'w') as Hist_Record:

            dump([], Hist_Record, indent=4)

    elif option == 'n':

        return


def Locate_Changes(initial_file_path):

    backup_path = Get_BackUp_FilePath(initial_file_path)

    with open(initial_file_path, 'r') as initial_file, open(backup_path, 'r') as backup_file:

        initial_file_content = initial_file.readlines()

        backup_file_content = backup_file.readlines()

    # Create a dictionary where to store the changes detected in each file

    Alteration_Record = {}

    changes = []

    # Compare the content of each file with the backup file's content 

    # The enumerate function is used to keep track of the number of each line

    for i, (read_line, backup_line) in enumerate(zip(initial_file_content, backup_file_content)):

        # If the lines are different, add the change to the dictionary

        if read_line != backup_line:

            change = {
                'line_number': i,
                'last_update': read_line.strip(),
                'last_backup_record': backup_line.strip()
            }

            changes.append(change)

    Alteration_Record = {
        'file': initial_file_path,
        'alteration_time': str(datetime.now()),
        'changes_history': changes
    }

    # Load the existing JSON data from the file

    Hist_Record_data = []

    if path.getsize('Monitoring_Repo/Alteration_History.json') > 0:

        with open('Monitoring_Repo/Alteration_History.json', 'r') as Hist_Record:

            Hist_Record_data = load(Hist_Record)

    # Check if the Alteration_Record already exists in the JSON data (i.e: if the current changes were already recorded )

    existing_record = None

    for record in Hist_Record_data:

        if Alteration_Record['file'] == record['file'] and (all(change in record['changes_history'] for change in Alteration_Record['changes_history']) or all(change in Alteration_Record['changes_history'] for change in record['changes_history'])):

            existing_record = record

            break

    # Add the Alteration_Record to the JSON data if it does not already exist

    if not existing_record:

        Hist_Record_data.append(Alteration_Record)

    # Write the changes to a JSON file

    with open('Monitoring_Repo/Alteration_History.json', 'w') as Hist_Record:

        dump(Hist_Record_data, Hist_Record, indent=4)


# Clear the changes history record and update the checksums file


def Clear_History(file_path):

    # Remove the recorded changes on the given file from the Alteration_History file

    updated_record = []

    with open('Monitoring_Repo/Alteration_History.json', 'r') as Hist_Record:

        Hist_Record = load(Hist_Record)

    for record in Hist_Record:

        if record['file'] != file_path:

            updated_record.append(record)

    with open('Monitoring_Repo/Alteration_History.json', 'w') as Hist_Record:

        dump(updated_record, Hist_Record, indent=4)

    # Update checksums record

    with open('Monitoring_Repo/checksums.csv', 'r') as Repo:

        checksums_record = list(csv.reader(Repo))

    for checksum_row in checksums_record:

        if file_path in checksum_row:

            checksums_record[checksums_record.index(checksum_row)] = [

                datetime.now(), file_path, Hash_File(file_path)]

    with open('Monitoring_Repo/checksums.csv', 'w', newline='') as checksum_repo:

        writer = csv.writer(checksum_repo, delimiter=',')

        for row in checksums_record:

            writer.writerow(row)


def Display_Details(file_path):

    with open('Monitoring_Repo/Alteration_History.json', 'r') as Hist_Record:

        Hist_Record_data = load(Hist_Record)

    Related_Alteration_Record = []

    for record in Hist_Record_data:

        if file_path == record['file']:

            Related_Alteration_Record.append(record)

    Related_Alteration_Record = sorted(

        Related_Alteration_Record, key=lambda x: x['alteration_time'])

    for alteration in Related_Alteration_Record:

        # Display summary of where the chasnges took place

        print(Fore.RED + '\n\t>> Change detected in ' + Fore.YELLOW + file_path + ' at : '+alteration['alteration_time']+' by : '+getuser()+'\n' + Style.RESET_ALL)

        print('\tDetected changes list : \n')

        for change in alteration['changes_history']:

            print('\t\t- Line number        : ' + Fore.YELLOW + str(change['line_number'])   + Style.RESET_ALL)

            print('\t\t- Last update        : ' + Fore.YELLOW + change['last_update']        + Style.RESET_ALL)

            print('\t\t- Last backup record : ' + Fore.YELLOW + change['last_backup_record'] + Style.RESET_ALL)

    key = input('\nApprove changes  < y >   |    Discard chenges  < d >    |    Pass  < p >   :   ')

    if key == 'p':
        sleep(5)

    elif key == 'y' or key == 'd':

        # In case the modifications were  legitimate and approved, update the backup file and discard recorded changes

        if key == 'y':

            # Update the backup file

            copy(file_path, Get_BackUp_FilePath(file_path))

        # In case the modifications were not legitimate nor approved, recover backup version

        elif key == 'd':

            # Copy the backup file to the original file path

            copy(Get_BackUp_FilePath(file_path), file_path)

        # Updte the checksum register

        Clear_History(file_path)

    else:

        print(Fore.RED+'\n- Unvalid input ! \n \t\t Try  :  < y > to Approve changes  |      < d >  to Discard chenges  |      < p >  to Skip '+Style.RESET_ALL)

        sleep(5)


def handle_timeout(signum, frame):
    pass


def Scan(Root):

    print('\n\nScaning ...\n\n')

    Altered_Files = []

    files_paths = [path.join(root, file)    for root, _ , files in walk(Root) for file in files]
    
    """
            In this section each file in the specified directory is checked by calcualatin its hash and then comparing it with the hash in the checksums
        file which containes the last approved changes by the owner user (root in our case).
            In case if any changes  were detected the Locate_Changes function  is called to identify the altered data.  
    """
    with open('Monitoring_Repo/checksums.csv', 'r') as Repo:

        files_records = [row for row in csv.reader(Repo)]

        for file_path in files_paths:

            for record in files_records:

                if file_path == record[1] and Hash_File(file_path) != record[2]:

                    print(Fore.RED + '\n>> New modification in the file '+Fore.YELLOW +f'{path.basename(file_path)} '+Fore.RED + ' has been detected  ' + Style.RESET_ALL)
                    Altered_Files.append(file_path)

                    Locate_Changes(file_path)
                    
    
    # Set a signal handler for SIGALRM, which is raised when the specified period is reached
    signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(int(argv[3]))
        

    if len(Altered_Files) != 0:

        try:

            key = input('\nTo see the alterations details enter  < ' + Fore.YELLOW+'m'+Style.RESET_ALL+' >  :    ')

            if key == 'm':

                for file in Altered_Files:

                    print('\n####################################################################################################################\n')

                    print('-->  '+Fore.RED+file + Style.RESET_ALL+'\n')

                    Display_Details(file)

        except TimeoutError:

            pass

    else:

        sleep(20)


def Display_Help_Page():

    print("""

        Usage: python Monitor.py [option] [Scans period]


        Options:

        -i        initialize the monitoring repository.

        -u        update the data of the monitoring repository.

        -s        starts the scaning of the directory specified in arguments.

        -h        display this help page.

        * The two options < u > and < s > are valid only if the initialization is already done.

        Description:
            This program monitors a directory for changes and keeps a record of the changes in a repository. Which allows to preserve
        the integrity of system files, and recover the date in case unauthorized modifications have taken place.

        Examples of usage:

            >> sudo python  Monitor.py  -i  /directory_path  10

            >> sudo python  Monitor.py  -s  /directory_path  10

    """)


if __name__ == '__main__':

    # Check if user is running the program as root

    if geteuid() == 0:

        if len(argv) == 4:

            if argv[1] == '-i' or argv[1] == '-s' or argv[1] == '-u':
                
                # Initialize the database with fingerprints of each file and creation of backup files

                if argv[1] == '-i':

                    Initialize_Monitoring_Repo(argv[2])
                    
                # Update the whole database with the backup files

                elif argv[1] == '-u' or argv[1] == '-s':

                    if path.isfile('Monitoring_Repo/Alteration_History.json') and path.isfile('Monitoring_Repo/checksums.csv') :
                        
                        if argv[1] == '-u':
                            Update_Register(argv[2])

                    else:

                        print("Error: The files required for the program are not present ( Do initialize the program first ).")
                        print("Solution: sudo python Monitor.py -i root time_between_each_check")
                        exit()

                # Start the  scans
                while True:
                    Scan(argv[2])

            else:

                print("Error: wrong option selected.")
                print("Usage: sudo python Monitor.py -s root time_between_each_check")

        elif argv[1] == '-h':

            Display_Help_Page()

        else:

            print("Error: Insufficient arguments.")
            print("Usage: sudo python Monitor.py -s root_directory time_between_each_check")

    elif argv[1] == '-h':

        Display_Help_Page()

    else:
        print('Root privileges are required to run this script !!')
