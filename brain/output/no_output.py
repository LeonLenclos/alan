from chatterbot.output import OutputAdapter

class NoOutput(OutputAdapter):

    def process_response(self, *args, **kwargs):
        pass