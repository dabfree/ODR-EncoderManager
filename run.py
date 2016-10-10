import cherrypy
import argparse
import os
import sys

from config import Config
from auth import AuthController, require, is_login
from api import API

#import signal
#from signal import SIGKILL

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))


class Root():
	def __init__(self, config):
		self.conf = config
		self.auth = AuthController(self.conf.config['auth'])
		self.api = API()
	
	_cp_config = {
		'tools.sessions.on': True,
		'tools.auth.on': True
	}
	
	# This is available for all authenticated or not user
	@cherrypy.expose
	def index(self):
		raise cherrypy.HTTPRedirect('/home')
	
	@cherrypy.expose
	def home(self):
		tmpl = env.get_template("home.html")
		js = []
		return tmpl.render(tab='home', js=js, is_login=is_login())
	
	@cherrypy.expose
	def help(self):
		tmpl = env.get_template("help.html")
		js = []
		return tmpl.render(tab='help', js=js, is_login=is_login())
	
	@cherrypy.expose
	def about(self):
		tmpl = env.get_template("about.html")
		js = []
		return tmpl.render(tab='about', js=js, is_login=is_login())
	
	# This is only available for authenticated user
	@cherrypy.expose
	@require()
	def status(self):
		tmpl = env.get_template("status.html")
		js = ['/js/odr-status.js']
		return tmpl.render(tab='status', js=js, is_login=is_login())
	
	@cherrypy.expose
	@require()
	def config(self):
		tmpl = env.get_template("config.html")
		js = ['/js/odr-config.js']
		return tmpl.render(tab='config', js=js, is_login=is_login())


if __name__ == '__main__':
	# Get configuration file in argument
	parser = argparse.ArgumentParser(description='ODR Encoder Manager (WebGUI)')
	parser.add_argument('-c','--config', help='configuration filename',required=True)
	cli_args = parser.parse_args()
	
	# Check if configuration exist and is readable
	if os.path.isfile(cli_args.config) and os.access(cli_args.config, os.R_OK):
		print "Use configuration file %s" % (cli_args.config)
	else:
		print "Configuration file is missing or is not readable - %s" % (cli_args.config)
		sys.exit(1)
		
	# Load configuration
	config = Config(cli_args.config)

	# Start cherrypy
	if config.config['global']['daemon']:
		cherrypy.process.plugins.Daemonizer(cherrypy.engine).subscribe()
	
	cherrypy.config.update({
		'server.socket_host': config.config['global']['host'],
		'server.socket_port': int(config.config['global']['port']),
		'request.show_tracebacks' : True,
		'environment': 'production',
		'tools.sessions.on': True,
		#'tools.encode.on': True,
		#'tools.encode.encoding': "utf-8",
		'log.access_file' : os.path.join(config.config['global']['logs_directory'], 'access.log'),
		'log.error_file' : os.path.join(config.config['global']['logs_directory'], 'error.log'),
		'log.screen': False,
		})
	
	cherrypy.tree.mount(
		Root(config), config={
			'/':
					{ 
					},
			'/css':
					{ 
					'tools.staticdir.on': True,
					'tools.staticdir.dir': os.path.join(config.config['global']['static_directory'], u"css/")
					},
			'/js':
					{ 
					'tools.staticdir.on': True,
					'tools.staticdir.dir': os.path.join(config.config['global']['static_directory'], u"js/")
					},
			'/fonts':
					{ 
					'tools.staticdir.on': True,
					'tools.staticdir.dir': os.path.join(config.config['global']['static_directory'], u"fonts/")
					},
			'/favicon.ico':
					{ 
					'tools.staticfile.on': True,
					'tools.staticfile.filename': os.path.join(config.config['global']['static_directory'], u"fonts/favicon.ico")
					},
		}
	)
	
	#cherrypy.engine.signal_handler.handlers["SIGINT"] = handle_sigint
	
	cherrypy.engine.start()
	cherrypy.engine.block()
	
    #cherrypy.quickstart(Root())