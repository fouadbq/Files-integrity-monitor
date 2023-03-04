![Capture d'écran 2023-03-04 153033](https://user-images.githubusercontent.com/120426068/222917504-48e3e6be-a161-4be9-b57e-c1f4ab7ca587.png)

# Files-integrity-monitor


        This program monitors a directory for changes and keeps a record of the changes in a repository. Which\
    allows to preserve the integrity of system files, and recover the date in case unauthorized modifications \have taken place.




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
sudo python  Monitor.py  -i  /directory_path  <sacning period>
```


## Documentation

&nbsp;&nbsp;&nbsp;When running the script for the first time, it will generate new files in the specified root directory holding the <br/>
fingerprints of each file within this directory along with the traces of any changes  that would occur later on. These <br/>
files are as follows: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>>*__checksums.csv__*: This file contains the hash values of all files in the specified directory and its subdirectories,<br/> 
along with the date and time of the last modification.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>>*__BackUp_Files_Repo__*: This folder contains backup copies of all files being monitored, named using the <br/>
pattern <filename>_bck<extension><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>>*__Alteration_History.json__*: This file contains the history of all changes made to the files being monitored.<br/>
### Usage
&nbsp;&nbsp;&nbsp;To initialize the Monitoring Repository, run the script with the command :
```bash
sudo python  Monitor.py  -i  /directory_path  <sacning period>
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>This will create the Monitoring Repository files in the root directory of the project, along with the required files and folders.

&nbsp;&nbsp;&nbsp;To update the Monitoring Repository with the latest changes, run the script with the command 
```bash
sudo python  Monitor.py  -u  /directory_path  <sacning period>
``` 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>This will update the checksums.csv file and overwrite  backup copies of all modified files and initialize non recorded files in case there were any.\
&nbsp;To avoid losing any important data in this situation, it is important to check the changes records before making any updates.

&nbsp;&nbsp;&nbsp;To restart the monitoring, run the script with the command :
```bash
sudo python  Monitor.py  -s  /directory_path  <sacning period>
```  
:warning:&nbsp;&nbsp;It is important to keep in mind that in case if the program was not initialized the two commmands -Update and -Scan won't work since the required files (*__checksums.csv__* , *__BackUp_Files_Repo__*, *__Alteration_History.json__*) have not yet been created.<br/><br/>
        
&nbsp;&nbsp;&nbsp;__Replace "/directory_path" with the path to the directory you want to monitor and "sacning period" with the duration of the scans in all of the aforementioned commands.__<br/><br/>
        

## Feedback

If you have any feedback, please do reach out to me at fouadelbaqqaly@gmail.com


