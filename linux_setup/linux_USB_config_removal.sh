#!/bin/bash
# Removes udev rules, libhs_datalog_v1.so, libhs_datalog_v2.so lib and hsdatalog user group
# NOTE: unplug the board before running the script
echo "NOTE: unplug the board before running the script"

# Ask user to confirm the board is unplugged
read -p "Have you unplugged the board? [Y/n]: " -n 1 -r
echo    # Move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ ! -z $REPLY ]]; then
    echo "Please unplug the board before running this script. Exiting..."
    exit 1
fi

sudo rm /usr/lib/libhs_datalog_v1.so
sudo rm /usr/lib/libhs_datalog_v2.so
echo "libhs_datalog_v1.so and libhs_datalog_v2.so libraries removed from /usr/lib"

sudo sed -i '/hsdatalog/d' /etc/group
echo "hsdatalog entry removed from /etc/group file"

sudo rm /etc/udev/rules.d/30-hsdatalog.rules
echo "30-hsdatalog.rules file removed from /etc/udev/rules.d"

sudo udevadm control --reload
echo "udev reloaded"

