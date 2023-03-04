![Logo](https://user-images.githubusercontent.com/120426068/222900572-80ed8c60-7fdc-4f0c-a8d6-b733f61813b1.png)


# Files-integrity-monitor


        This program monitors a directory for changes and keeps a record of the changes in a repository. Which
    allows to preserve the integrity of system files, and recover the date in case unauthorized modifications have taken place.




## Run Locally

Clone the project

```bash
  git https://github.com/fouadbq/Files-integrity-monitor.git
```

Install the required packages on your local machine

```bash
pip install -r requirements.txt
```

 Navigate to the directory you want to monitor.


```bash
cd /directory_path
```

Start the monitor

```bash
sudo python  Monitor.py  -i  /directory_path  10
```


## Documentation

    When running the script for the first time, it will generate new files in the specified root directory holding the fingerprints of each file within this directory along with the traces of any changes  that would occur later on. These files are as follows:
            * checksums.csv : This file contains the hash values of all files in the specified directory and its subdirectories, along with the date and time of the            last modification.
            * BackUp_Files_Repo: This folder contains backup copies of all files being monitored, named using the pattern <filename>_bck<extension>
            * Alteration_History.json: This file contains the history of all changes made to the files being monitored.
