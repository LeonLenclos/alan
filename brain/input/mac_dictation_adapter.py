from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement
from time import clock
from subprocess import check_output

class MacDictationAdapter(InputAdapter):
    """
    This is an adapter for audio input.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor = 0
        self.max_silent_duration = 0.5
        self.file_path = "tmp.txt"

    def process_input(self, *args, **kwargs):
        """
        Returns a statement object based on the input source.
        """
        start_speaking = False
        start_silent_time = None
        old_text = text = self.read_file()

        print("Start to speak")
        while True:
            # Read file
            text = self.read_file()
            # Compare with last loop text
            if text != old_text:
                old_text = text
                print(text[self.cursor:])
                start_silent_time = None
                if not start_speaking:
                    start_speaking = True
            elif start_speaking:
                if start_silent_time:
                    silent_duration = clock() - start_silent_time
                    str_time = "%3.2f" % silent_duration
                    print(str_time, end="\r")
                    if silent_duration > self.max_silent_duration:
                        break
                else :
                    start_silent_time = clock()


        speech = text
        self.cursor += len(text) -1
        print("End of speech :\ntext = %s (cursor = %s)" % (text, self.cursor))

        return Statement(speech)


    def process_input_statement(self, *args, **kwargs):
        """
        Return an existing statement object (if one exists).
        """
        input_statement = self.process_input(*args, **kwargs)
        return input_statement

    def read_file(self):
        with open(self.file_path, 'r') as f:
            text = f.read()
        # text =  check_output(['cat', self.file_path])
        return text[self.cursor:]
