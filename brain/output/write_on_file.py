from chatterbot.output import OutputAdapter

class WriteOnFile(OutputAdapter):
    """This is an output_adapter just for writing phrases on a file."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_response(self, statement, session_id=None, file_name='conv.txt'):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :param file_name: The file name where to write.
        :returns: The response statement.
        """
        with open(file_name, 'a') as fi:
            print(statement.text, file=fi)
        return statement
