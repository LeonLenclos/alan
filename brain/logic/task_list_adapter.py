from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

from random import choice
from utils import compare

import time

class TaskListAdapter(AlanLogicAdapter):
    """This logic adapter is usefull for task lists"""

    def __init__(self, **kwargs):
        """Required kwarg :

        trigger
        A list of strings.

        task_list
        A list of strings
        """
        super().__init__(**kwargs)

        # Getting trigger
        try:
            self.trigger = kwargs['trigger']
        except KeyError:
            raise KeyError('trigger is a required argument')
        if type(self.trigger) != list:
            raise TypeError("trigger must be a list")

        # Getting task_list
        try:
            self.task_list = kwargs['task_list']
        except KeyError:
            raise KeyError('task_list is a required argument')
        if type(self.task_list) != list:
            raise TypeError("task_list must be a list")

        self.actif = False
        self.i = 0
        self.start_time = 0

    def can_process(self, statement):
        return self.actif or statement.text.lower() in [s.lower() for s in self.trigger]

    def stop(self):
        self.actif = False
        self.i = 0

    def process(self, statement):
        if not self.actif:
            self.actif = True
            self.start_time = time.time()

        try:
            minutes = int(time.time() - self.start_time) // 60
            seconds = int(time.time() - self.start_time)  % 60
            statement_out = Statement(self.task_list[self.i].format(minutes=minutes, seconds=seconds))
            confidence = 1
            self.i += 1
        except IndexError:
            self.stop()
            statement_out = Statement("...")
            confidence = 0

        if "stop" in statement.text.lower():
            self.stop()
            statement_out = Statement("...")
            confidence = 0

        statement_out.confidence = self.get_confidence(confidence)
        return statement_out
