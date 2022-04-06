# Importing the library
import time

import psutil
import main


# Calling psutil.cpu_precent() for 4 seconds
cpu_usage = psutil.cpu_percent(2)

while True:
    if cpu_usage < 25:
        print('The CPU usage is: ', cpu_usage, " (cpu is fine)")
        print("finally. program starts working")
        main.main_method()
        break
    else:
        print('The CPU usage is: ', cpu_usage, " (cpu is hot)")
        time.sleep(4)

        cpu_usage = psutil.cpu_percent(2)
        continue
