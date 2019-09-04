from threading import Thread
import time

class DeviceStatusManager ( Thread ):

	def __init__(self, agents):
		Thread.__init__(self)
		self.agents = agents
		self.running = True
			

	def run ( self ):

		while self.running:
			time.sleep(1)
			for agent in self.agents:
				#print 'refresh status'
				agent.refreshStatus()


	def stop(self):
		self.running = False

