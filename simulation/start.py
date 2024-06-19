import sys
import os
import time
if __name__=="__main__":
    n=len(sys.argv)
    if n<2:
        print("no file path")
        exit()
    path=sys.argv[1]
    cmd="./waf --run 'scratch/third mix/"+path+"/config.txt' >mix/"+path+"/log.txt"
    if n>2:
        cmd="nohup "+cmd
    tm=time.localtime()
    print(tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec)
    print(cmd)
    os.system(cmd)