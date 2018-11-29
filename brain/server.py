# coding: utf8

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

        # Change / to /index.html
        if self.path == '/':
            self.path = 'www/index.html'
        elif self.path == '/todo':
            self.path = '../todo'
        elif self.path.startswith('/log/'):  
            self.path = self.path[1:]
        else :
            self.path = 'www' + self.path

        # Try to open asked path
        try:
            file_to_open = open(self.path).read()
            self.send_response(200)
        except:
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
