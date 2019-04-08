from chatterbot.output import OutputAdapter
from chatterbot import utils

class MainOutputAdapter(OutputAdapter):
    """MainOutputAdapter allow chatbot to use multiple outputs."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adapters = []

    def process_response(self, statement, conversation_id=None, **kwargs):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :param file_name: The file name where to write.
        :returns: The response statement.
        """
        for adapter in self.get_adapters():
            adapter.process_response(statement, **kwargs)
        return statement

    def get_adapters(self):
        """
        Return a list of all logic adapters being used.
        """
        return self.adapters

    def music(self):
        for adapter in self.get_adapters():
            music = getattr(adapter, 'music', None)
            if callable(music):
                music(adapter)
                return

    def add_adapter(self, adapter, **kwargs):
        """
        Appends a logic adapter to the list of logic adapters being used.
        :param adapter: The logic adapter to be added.
        :type adapter: `LogicAdapter`
        """
        utils.validate_adapter_class(adapter, OutputAdapter)
        adapter = utils.initialize_class(adapter, **kwargs, chatbot=self.chatbot)
        self.adapters.append(adapter)
