#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run this script (as root) to run the server.

Usage :

To access the chat page :
GET /
GET /index.html

To create a new conversation :
POST /new
It will return a JSON : {'conversation_id':123}

To talk with alan :
POST /talk {msg:"Human message...", conversation_id:1234}
It will return a JSON : {'text':"Alan message", 'command':"a command"}

POST request can also return an error in a JSON : {'err':"The error."} 
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import argparse

from alan import Alan


class Serv(BaseHTTPRequestHandler):

    # A dict containing all alan instances. Keys are conversation numer
    alans = {}
    # A list of logic adapter objects that must be shared between alan instances
    shared_logic_adapters = []
    # A list of logic adapter identifier for adapter that must be shared
    shared_logic_identifiers = ['mvochatbot']

    def log(self, conversation_id, txt):
        """log a pretty message with the conversation id"""
        self.log_message("({}) {}".format(conversation_id, txt))

    def new(self):
        """Create a new instance of Alan
        return a dict with conversation_id and alan_status
        """
        # create alan instance
        alan = Alan(
            settings_files=settings_files,
            preconfigured_logic_adapters=self.shared_logic_adapters)
    
        # manage shared_logic_adapters
        if len(self.shared_logic_adapters) == 0:
            for identifier in self.shared_logic_identifiers:
                adapter = alan.logic.get_adapter(identifier)
                if adapter :
                    self.shared_logic_adapters.append(adapter)

        # get conversation_id and store the instance in alans
        conversation_id = alan.conversation_id
        self.alans[conversation_id] = alan

        # return the conversation_id and the alan status
        return {
            'conversation_id' : str(conversation_id),
            'alan_status' : alan.status()
            }


    def talk(self, msg, conversation_id):
        """Take a msg and a conversation_id and return the response as a dict with text and command"""
        # Try to get the alan instance with the passed conversation_id
        try:
            alan = self.alans[conversation_id]
        except KeyError:
            return {'err': "La conversation {} n'existe pas où elle a été fermée.".format(conversation_id)}

        # Get the response
        response = alan.talk(msg)

        # Get command
        command = None
        if "command" in response.extra_data:
            command = response.extra_data["command"]

        # return the text and the command
        return {
            'text':response.text,
            'command': command
            }

    def do_GET(self):
        """Handler for GET request"""


        def dev_status ():
            return "{} conversations ouvertes".format(len(self.alans))
        def get_todo():
            dev_html = open('www/dev.html').read()
            todo_file = open(os.path.expanduser('~/alantodo.txt')).read()
            return dev_html.format(
                title="todo",
                content="<pre>{}</pre>".format(todo_file),
                status=dev_status()
                )
        def get_dev():
            dev_html = open('www/dev.html').read()
            return dev_html.format(
                title="dev",
                content = "",
                status=dev_status()
                )

        def get_logs_list():
            dev_html = open('www/dev.html').read()
            li_format = '<li><a href="{fi}">{fi}</a></li>'
            log_list = [li_format.format(fi=fi) for fi in os.listdir('log')]
            log_list.sort()
            return dev_html.format(
                title="logs",
                content = '<ul>{}</ul>'.format(''.join(log_list)),
                status=dev_status()
                )

        def get_log(log_content):
            dev_html = open('www/dev.html').read()
            return dev_html.format(
                title="log",
                content = "<pre>{}</pre>".format(log_content),
                status=dev_status()
                )

        # Try to open asked path
        try:
            if self.path == '/':
                file_to_open = open('www/index.html').read()
            elif self.path == '/dev':
                file_to_open = get_dev()
            elif self.path == '/todo':
                file_to_open = get_todo()
            elif self.path == '/logs':
                file_to_open = get_logs_list()
            elif self.path.startswith('/conv'):  
                file_to_open = get_log(open("log" + self.path).read())
            else :
                file_to_open = open('www'+self.path).read()

            self.send_response(200)

        except FileNotFoundError:
            file_to_open = "File not found"
            self.send_response(404)

        # Return asked page
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        """Handler for POST request"""

        reply = None

        # TALK
        if self.path == '/talk':
            # Get post body
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            post_body = json.loads(post_body.decode('utf-8'))
            msg = post_body["msg"]
            conversation_id = int(post_body["conversation_id"])
            # log receiving data
            self.log(conversation_id, "receiving = {}".format(msg))
            # get reply
            reply = self.talk(msg, conversation_id)
            # log sending data
            self.log(conversation_id, "sending = {}".format(reply))

        # NEW
        elif self.path == '/new':
            # get reply
            reply = self.new()
            # log new conversation
            self.log(reply, "new conversation")

        # return asked data
        if reply:
            self.send_response(200)
        else:
            self.send_response(400)
            reply = {'err': "Bad request..."}
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(reply), 'utf-8'))

    def end_headers (self):
        #TODO: check if this is really useful ! 
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        BaseHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', nargs='+', help="Settings file json files without file extension separed with spaces", default=["server"])
    ap.add_argument('-a', help="Settings ip adress", default="localhost")
    ap.add_argument('-p', help="Settings port", type=int, default=80)
    args = ap.parse_args()
    settings_files = args.s
    adress = (args.a, args.p)

    # start serving
    httpd = HTTPServer(adress, Serv)
    print("serving on {}".format(adress))
    httpd.serve_forever()
