import time

class Creature:
    def __init__(self,queue):
        self.num = 0
        self.queue = queue
        self.run()



    def run(self):
        while True:
            self.num += 1
            try:
                self.queue.put_nowait(self.num)
            except:
                pass
