import worktime
from worktime import *

def workscreen():
    worktime.workperiod()

def continuescreen():
    worktime.continuescreen()

if __name__ == "__main__":
    workscreen()
    if continuescreen():
        print('yes move on pls')

#NOT USED

