import os
import sys
import signal
import time

pid = os.fork()

if pid == 0:
    i = 1
    while True:
        print(i)
        time.sleep(1)
        i = i + 1
    sys.exit()
else:
    while True:
        c = sys.stdin.read(1)
        #c2 = sys.stdin.read(2)
        if c == ' ':
            #print(c2)
            os.kill( pid, signal.SIGTERM )
            sys.exit()
        else:
            i = 0
            print("使用方法")