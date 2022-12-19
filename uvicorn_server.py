import multiprocessing
from fastapi import FastAPI
from uvicorn import Config, Server, run

class UvicornServer(multiprocessing.Process):
	def __init__(self):
		super().__init__()

	def stop(self):
		self.terminate()

	def run(sef, *args, **kwargs):
		run('main:app', app_dir=r'C:\fastapi\app', reload=True) 