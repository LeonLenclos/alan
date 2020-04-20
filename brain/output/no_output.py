from chatterbot.output import OutputAdapter

class NoOutput(OutputAdapter):

    def process_response(self, statement, callback, *args, **kwargs):
        callback()