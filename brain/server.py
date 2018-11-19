from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from alan import Alan
ADRESS = ('localhost', 8080)

# curl -d '' localhost:8080/new
# curl -d '{"msg":"Bonjour Alan","conversation_id":138}' localhost:8080/talk

class Serv(BaseHTTPRequestHandler):


    alans = {}

    def new(self):
        """Create a new instance of Alan and return the associed conversation_id"""
        alan = Alan()
        conversation_id = alan.conversation_id
        self.alans[conversation_id] = alan
        return str(conversation_id)

    def talk(self, msg, conversation_id):
        """Take a msg and a conversation_id and return the response"""
        try:
            alan = self.alans[conversation_id]
        except KeyError:
            return "La conversation {} n'existe pas où elle a été fermée.".format(conversation_id)

        return alan.get_response(msg).text

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
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
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            post_body = json.loads(post_body.decode('utf-8'))
            msg = post_body["msg"]
            conversation_id = post_body["conversation_id"]
            reply = self.talk(msg, conversation_id)

        elif self.path == '/new':
            reply = self.new()


        if reply:
            self.send_response(200)
        else:
            self.send_response(400)
            reply = "Mauvaise requête ('<_ ' )"
        self.end_headers()
        self.wfile.write(bytes(reply + "\n", 'utf-8'))


httpd = HTTPServer(ADRESS, Serv)
print("serving on {}".format(ADRESS))
httpd.serve_forever()
