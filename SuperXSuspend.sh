#!/bin/bash
#Version: 2.0.10.05.2025
#Author: Hasan Y. Karaahmet
#Copyright ©2024 All rights are public domain.
#Requires SoX installed for sound to work. Use: sudo apt-get install sox
#This script notifies the user, makes a little sound and suspends the system.
#Tested OK on Ubuntu. Bind to a key combo from Settings > Keyboard Shortcuts
#Repo: https://github.com/hykaraahmet/scripts


notify-send "Super+X SUSPENDING... See ya!"
#Alerts user. GUI only.

play -q -n synth 0.1 sin 600 2>/dev/null && play -q -n synth 0.1 sin 400 2>/dev/null && play -q -n synth 0.1 sin 200 2>/dev/null || echo -e "\a"
#Generates a little sound effect.

sleep 2
#Waits 2 seconds.

systemctl suspend || { notify-send "Failed to suspend!"; exit 1; }
#Suspends the system (saves current state to RAM) with a little error handling.


