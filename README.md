![Logo](https://user-images.githubusercontent.com/120426068/222900572-80ed8c60-7fdc-4f0c-a8d6-b733f61813b1.png)


# Files-integrity-monitor


    This program monitors a directory for changes and keeps a record of the changes in a repository. Which allows to preserve
    the integrity of system files, and recover the date in case unauthorized modifications have taken place.




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

[Documentation](https://linktodocumentation)

When running the script for the first time, a new Monitoring Repository folder will be created in the root directory of the project. This folder contains the following files:
