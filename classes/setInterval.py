from threading import Timer
import time

class setInterval :
    def __init__(self,interval,task,end=0) :
        self.interval = interval
        self.startTime = time.time()
        self.endTime = end
        self.setInterval(task)

    def setInterval(self,task) :
        self.runningTime = time.time()-self.startTime
        print('running time {:.1f}s'.format(float(self.runningTime)))
        isStop = task()
        isStop = False
        if not self.endTime==0 and self.runningTime>=float(self.endTime):
            isStop = True
        if not isStop:
            Timer(self.interval, self.setInterval, [task]).start()