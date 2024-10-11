# these files dont have the #!/bin/bash since they are
# called by lambda by an eval. Since that, these files
# can also use the variables in lambda file

echo -e "${START_COLOR}Starting Lambda AI...${NO_COLOR}"

# load the global config and keys
source .keys
source global.conf
# load the config
source lambda/local.conf
# activate the venv
source venv/bin/activate
# and run the app
python3 lambda/app.py

echo -e "${END_COLOR}Stopping Lambda...${NO_COLOR}"