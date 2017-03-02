#!/bin/bash

echo "Listening for desktop lock/unlock events..."

dbus-monitor --session "type='signal',interface='com.ubuntu.Upstart0_6'" | \
(
  while true; do
    read X
    if echo $X | grep "desktop-lock" &> /dev/null; then
      punch-clock SCREEN_LOCKED
    elif echo $X | grep "desktop-unlock" &> /dev/null; then
      punch-clock SCREEN_UNLOCKED
    fi
  done
)