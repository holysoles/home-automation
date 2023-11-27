# home-automation
A Python service for a Raspberry Pi to interact with various devices to expose them to a smarthome infrastructure.

## Repo contents

- launcher.sh
  - bash script that is set with crontab to run on reset, launches mc.py with nohup in the background
- mc.py
  - main script, used to sub channel changes, currently coming through pubnub, which receives pub posts through IFTTT
- samsung.conf
  -  backup LIRC config file for samsung tv infrared remote commands

## Dependencies
- [LIRC]([url](https://lirc.org/)https://lirc.org/)

## Additional Notes
- dependent scripts are executed with `sudo`, which was initially done due to both grant the needed GPIO access privileges. This should be used with extreme caution and probably removed in favor of:
  -  ensuring the `pi` user has been added to the `gpio` group to allow running without elevation.
  -  BlueZ/bluetooth device permissions for non-root read/write access
- The PubNub keys documented here are no longer valid and should be internalized if used
