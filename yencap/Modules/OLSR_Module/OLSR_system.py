import os, string
from constants import C

class OLSR_System():
    
    def __init__(self):
        self.pid = -1
        
    def find_running_instance(self):
        raw_pid = os.popen('pidof olsrd').read().lstrip().rstrip()
        if raw_pid != '':
            self.pid = string.atoi(raw_pid)
        else:
            self.pid = -1
        
    def stop_running_instance(self):
        os.kill(self.pid, 9)
        return
        
    def spawn_olsr_process(self):
        print "process id = %s" %os.spawnl(os.P_NOWAIT, C.OLSR_DAEMON_NAME)
        return
    
    def start_new_olsr_instance(self):
        self.find_running_instance()
        if self.pid != -1:
            self.stop_running_instance()
            self.spawn_olsr_process()
            self.pid = -1
        else:
            self.spawn_olsr_process()