# these files dont have the #!/bin/bash since they are
# called by lambda by an eval. Since that, these files
# can also use the variables in lambda file

echo -e "${START_COLOR}Starting DB...${NO_COLOR}"

# load the global config and keys
source .env
source global.conf
# load the config
source db/local.conf
# activate the venv
source venv/bin/activate
# and run the app
python3 db/app.py

echo -e "${END_COLOR}Stopping DB...${NO_COLOR}"