# coding: utf8
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import argparse
from alan import Alan

# curl -d '' localhost:80/new
# curl -d '{"msg":"Bonjour Alan","conversation_id":138}' localhost:8080/talk

ADRESS = ('10.104.3.66', 80)
settings_files = []

class Serv(BaseHTTPRequestHandler):


    alans = {}
    shared_logic_adapters = []
    shared_logic_identifiers = ['mvochatbot']

    def log(self, conversation_id, txt):
        self.log_message("({}) {}".format(conversation_id, txt))

    def new(self):
        """Create a new instance of Alan and return the associed conversation_id"""
        alan = Alan(
            settings_files=settings_files,
            preconfigured_logic_adapters=self.shared_logic_adapters)
    
        # manage shared_logic_adapters
        if len(self.shared_logic_adapters) == 0:
            for identifier in self.shared_logic_identifiers:
                adapter = alan.logic.get_adapter(identifier)
                if adapter :
                    self.shared_logic_adapters.append(adapter)

        conversation_id = alan.conversation_id
        self.alans[conversation_id] = alan
        return {
            'conversation_id' : str(conversation_id),
            'alan_status' : alan.status()
            }


    def talk(self, msg, conversation_id):
        """Take a msg and a conversation_id and return the response"""
        try:
            alan = self.alans[conversation_id]
        except KeyError:
            return {'err': "La conversation {} n'existe pas où elle a été fermée.".format(conversation_id)}
        response = alan.talk(msg)

        command = None
        if "command" in response.extra_data:
            command = response.extra_data["command"]
        return {
            'text':response.text,
            'command': command
            }

    def do_GET(self):
        if self.path == '/':
            self.path = '/www/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):

        reply = None

        if self.path == '/talk':
            # Get post body
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            post_body = json.loads(post_body.decode('utf-8'))
            msg = post_body["msg"]
            conversation_id = int(post_body["conversation_id"])
            # Log posted msg
            self.log(conversation_id, "receiving = {}".format(msg))
            reply = self.talk(msg, conversation_id)
            self.log(conversation_id, "sending = {}".format(reply))

        elif self.path == '/new':
            reply = self.new()
            self.log(reply, "new conversation")


        if reply:
            self.send_response(200)
        else:
            self.send_response(400)
            reply = {'err': "Bad request..."}

        self.end_headers()
        self.wfile.write(bytes(json.dumps(reply), 'utf-8'))

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        BaseHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', nargs='+', help="Settings file json files without file extension separed with spaces", default=["server"])
    args = ap.parse_args()
    settings_files = args.s

    httpd = HTTPServer(ADRESS, Serv)
    print("serving on {}".format(ADRESS))
    httpd.serve_forever()
