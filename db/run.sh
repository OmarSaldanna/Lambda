#!/bin/bash

echo -e "${GREEN}Starting DB...${NC}"
source .env && source venv/bin/activate && python3 db/app.py
echo -e "${RED}Stopping DB...${NC}"
exit 0