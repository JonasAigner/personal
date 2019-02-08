"""Timer class to easily make a Timer in python

Autor: Hiheat
Github: Hiheat

Made with python 3.7.1
"""


class Timer():
	
	def __init__(self, timing, speed=1):
		self.time_value = 0
		self.stop_time = timing
		self.speed = speed
		
	def __call__(self):
		self.time_value += self.speed
		if self.time_value >= self.stop_time:
			self.time_value = 0
			return True
		return self.time_value
		
		

