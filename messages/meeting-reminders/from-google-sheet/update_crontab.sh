#!/bin/bash

# Wrapper around update_crontab.py setting up the environment

cd /home/llambre1
source .bashrc
cd Programs
source venv_generic/bin/activate
cd lunchbot/messages/meetings-reminders/from-google-sheet
python update_crontab.py
