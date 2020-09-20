#!/bin/bash

# For out-of-docker local development!

if [ ! -d ./.venv ]; then
	echo "[+] Setting up Virtualenv..."
    virtualenv .venv
fi

source ./.venv/bin/activate
pip install -r requirements.txt
python ./bot.py
