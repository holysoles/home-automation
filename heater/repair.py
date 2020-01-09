#Script for repairing hc-05 bt module to pi when it disconnects

import os

os.system('sudo rfcomm connect hci0 FC:A8:9A:0A:03:A7 &')
