from threading import Timer
from chatterbot.output import OutputAdapter

class WebOutput(OutputAdapter):
    """This is an output_adapter for the web interface."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_output = None
        self.display_count = 0
        self.timer = None   
        self.speed = kwargs.get("speed", 0.05)


    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        self.current_output = statement.text

        # ignore if the statement is *chut*
        print(statement.extra_data)
        print('\n*'*10)

        if "command" in statement.extra_data:
            if statement.extra_data["command"] == "chut":
                return statement

        self.update_output()
        return statement

    def update_output(self):
        """Update little by little the response in chatbot.conversation"""
        conv_el = {'speaker':'alan','msg':'','finished':False}
        try:
            if self.chatbot.conversation[-1]['speaker'] == 'human' \
            or self.chatbot.conversation[-1]['finished']:
                self.chatbot.conversation.append(conv_el)
        except IndexError:
            self.chatbot.conversation.append(conv_el)

        self.display_count += 1
        
        if self.display_count > len(self.current_output):
            self.chatbot.conversation[-1]['finished'] = True
            self.chatbot.conversation[-1]['msg'] = self.current_output
            self.display_count = 0
            self.timer = None
        else:
            self.chatbot.conversation[-1]['msg'] =  self.current_output[:self.display_count]
            self.timer = Timer(self.speed, self.update_output)
            self.timer.start()