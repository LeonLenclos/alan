#!/usr/bin/env python3.5
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

To get the most recent conversation id :
POST /last
It will return a JSON : {'conversation_id':123}

To talk with alan :
POST /talk {msg:"Human message...", conversation_id:1234}
It will return a JSON : {'text':"Alan message", 'command':"a command"}

POST request can also return an error in a JSON : {'err':"The error."} 
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import time
import argparse
# from threading import Timer


from alan import Alan

CONVERSATION_LIFETIME = 36000 # 10 hours
LOG_ALL_ADAPTERS = False

class Serv(BaseHTTPRequestHandler):

    # A dict containing all alan instances. Keys are conversation id
    alans = {}
    # A dict containing the dates they will die. Keys are conversation id
    alans_death = {}
    # A list of logic adapter objects that must be shared between alan instances
    # shared_logic_adapters = []
    # # A list of logic adapter identifier for adapter that must be shared
    # shared_logic_identifiers = ['mvochatbot']
    # # A dict containing the timers for cough up. Keys are conversation id
    # alan_cough_timers = {}

    def log_request(self, code): 
        pass
    
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
            # preconfigured_logic_adapters=self.shared_logic_adapters,
            log_not_processing=LOG_ALL_ADAPTERS)
    
        # manage shared_logic_adapters
        # if len(self.shared_logic_adapters) == 0:
        #     for identifier in self.shared_logic_identifiers:
        #         adapter = alan.logic.get_adapter(identifier)
        #         if adapter :
        #             self.shared_logic_adapters.append(adapter)

        # get conversation_id and store the instance in alans
        conversation_id = alan.conversation_id
        self.alans[conversation_id] = alan
        self.alans_death[conversation_id] = time.time() + CONVERSATION_LIFETIME

        # HACK !!! (bof bof bof)
        alan.talk('chut')

        # return the conversation_id and the alan status
        return {
            'conversation_id' : str(conversation_id),
            'alan_status' : alan.status()
        }

    def last(self):
        """Return last instance of Alan
        return a dict with conversation_id and alan_status
        """    
        conversation_id = 0
        status = None

        # take the alan instance in alans with the greatest conv id
        for id, alan in self.alans.items():
            if id > conversation_id:
                conversation_id = id
                status = alan.status()

        # return the conversation_id and the alan status
        return {
            'conversation_id' : conversation_id,
            'alan_status' : status
            }


    def update_input(self, conversation_id, msg, finished):
        alan = self.alans[conversation_id]
        alan.update_input(msg, finished)

    def talk_alone(self, conversation_id):

        alan = self.alans[conversation_id]
        alan.talk_alone()

    def get_conv(self, conversation_id):
        """
        Return the conversation as a list of dict.
        each dict has 3 keys : 'speaker'(str), 'msg'(str), 'finished'(bool)
        """
        try:
            alan = self.alans[conversation_id]
            return alan.conversation
        except KeyError:
            return None
    def talk(self, msg, conversation_id):
        """Take a msg and a conversation_id and return the response as a dict with text and command"""
        # Try to get the alan instance with the passed conversation_id
        try:
            alan = self.alans[conversation_id]
        except KeyError:
            return {'err': "La conversation {} n'existe pas où elle a été fermée.".format(conversation_id)}

        self.alans_death[conversation_id] = time.time() + CONVERSATION_LIFETIME

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
            dev_html = open('www/dev.html', encoding='utf-8').read()
            try:
                todos = open(os.path.expanduser('~/alantodo.txt')).read()
            except FileNotFoundError:
                todos = 'Aucun todo...'
            return dev_html.format(
                title="todo",
                content="<pre>{}</pre>".format(todos),
                status=dev_status()
            )

        def get_dev():
            dev_html = open('www/dev.html', encoding='utf-8').read()
            return dev_html.format(
                title="dev",
                content = "",
                status=dev_status()
                )

        def get_logs_list():
            dev_html = open('www/dev.html', encoding='utf-8').read()
            li_format = '<li><a href="{fi}">{fi}</a></li>'
            log_list = [li_format.format(fi=fi) for fi in os.listdir('log') ]
            log_list.sort()
            log_list.reverse()
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
                file_to_open = open('www/index.html', encoding='utf-8').read()
            elif self.path == '/dev':
                file_to_open = get_dev()
            elif self.path == '/todo':
                file_to_open = get_todo()
            elif self.path == '/logs':
                file_to_open = get_logs_list()
            elif self.path.startswith('/conv'):  
                file_to_open = get_log(open("log" + self.path, encoding='utf-8').read())
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

        # CLOSE DEAD CONVERSATIONS
        for conversation_id in self.alans.copy().keys():
            if self.alans_death[conversation_id] < time.time():
                self.alans[conversation_id].log(
                    'SERVER : Closing conversation (lifetime elapsed).', True)
                self.alans[conversation_id].quit()
                del self.alans[conversation_id]
                del self.alans_death[conversation_id]

        # Get post body
        content_len = int(self.headers.get('content-length', 0))
        if content_len:
            post_body = self.rfile.read(content_len)
            post_body = json.loads(post_body.decode('utf-8'))
            # Last conv id
            if "conversation_id" in post_body and int(post_body["conversation_id"]) < 0:
                post_body["conversation_id"] = self.last()['conversation_id']


        # TALK
        if self.path == '/talk':
            # Get post body
            msg = post_body["msg"]
            conversation_id = int(post_body["conversation_id"])
            # log receiving data&
            self.log(conversation_id, "receiving = {}".format(msg))
            # get reply
            reply = self.talk(msg, conversation_id)
            # log sending data
            self.log(conversation_id, "sending = {}".format(reply))

        # UPDATE INPUT
        if self.path == '/update_input':
            # Get post body
            msg = post_body["msg"]
            finished = bool(post_body["finished"])
            conversation_id = int(post_body["conversation_id"])

            # log receiving data
            self.log(conversation_id, "update_input = {} {}".format(msg, '[finished]' if finished else ''))
            # update
            reply = self.update_input(conversation_id, msg, finished)

        # TALK ALONE
        if self.path == '/talk_alone':
            # Get post body
            conversation_id = int(post_body["conversation_id"])

            # log receiving data
            self.log(conversation_id, "talk_alone")
            # update
            self.talk_alone(conversation_id)
            reply = {}

        # GET CONV
        if self.path == '/get_conv':
            # Get post body
            conversation_id = int(post_body["conversation_id"])

            # log sending data
            self.log(conversation_id, "get_conv")

            # update
            reply = self.get_conv(conversation_id)


        # NEW
        elif self.path == '/new':
            # get reply
            reply = self.new()
            # log new conversation
            self.log(reply, "new conversation")

        # LAST
        elif self.path == '/last':
            # get reply
            reply = self.last()
            # log new conversation
            self.log(reply, "last conversation")

        # return asked data
        if reply is not None:
            self.send_response(200)
        else:
            self.send_response(400)
            reply = {'err': "Bad request..."}
        
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(reply), 'utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()
    
    def end_headers (self):
        #WATNING: check if this is really useful ! 
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Headers", "Authorization")
        BaseHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', nargs='+', help="Settings file json files without file extension separed with spaces", default=["server_no_mvo"])
    ap.add_argument('-a', help="Settings ip adress", default="localhost")
    ap.add_argument('-p', help="Settings port", type=int, default=8000)
    ap.add_argument('-l', action='store_true', help="Log all adapter not only processing ones.")
    args = ap.parse_args()
    settings_files = args.s
    adress = (args.a, args.p)
    LOG_ALL_ADAPTERS = args.l
    # start serving
    httpd = HTTPServer(adress, Serv)
    print("serving on {}".format(adress))
    httpd.serve_forever()
