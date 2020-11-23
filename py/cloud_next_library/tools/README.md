# Running tools

__Note:__ The YouTube Data API v3 has tight quotas. I need to request some
          quota from it because right now it's saying I don't have any.

## Install pip3 and virtualenv

```
sudo apt update
sudo apt install python3-pip
sudo apt install python3-venv
```

## Setup virtualenv

```
python3 -m venv env
```

## Start virtualenv

```
source env/bin/activate
```

## Install Google Cloud Python Cloud Libs

```
pip install -r requirements.txt
```

## Run the tool

__Note:__ There are instructions for installing this with Python 2.7 in the 
          master README.md in the parent directory.

```
python3 ./retrieve_youtube_metadata.py -k "<api key here>"

## Exit virtualenv

```
deactivate
```

