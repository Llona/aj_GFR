from threading import Timer
from os import system
import subprocess
import re
import os

a = 10000
# system ("adb shell input swipe 398 329 340 330 10000")
p = subprocess.Popen("adb shell input swipe 398 329 340 330 10000", shell=True)#, shell=False, universal_newlines=True,
                     # stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# p.communicate()


def run_wait(command):
    r = os.popen(command)
    text = r.read()
    r.close()
    return text

process_str = run_wait("adb shell ps -u shell -f")
print(process_str)
m = re.search('.*cmd input swipe .* '+str(a), process_str)
print("get string:")
if m:
    print(m.group(0))