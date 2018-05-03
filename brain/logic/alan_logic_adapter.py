from chatterbot.logic import LogicAdapter
from random import choice

class AlanLogicAdapter(LogicAdapter):
    """AlanLogicAdapter is a superclass for Alan's logic adapters
    """

    def __init__(self, **kwargs):
        """Optional kwargs :

        max_confidence
        A float (from 0 to 1). Default is 1.
        The logic adapter should never return a greater confidence value.
        This value should not change.

        min_confidence
        A float (from 0 to max_confidence). Default is 0.
        The logic adapter should never return a lower confidence value.
        This value should not change.

        confidence_coefficient
        A float (from 0 to 1). Default is max_confidence.
        The confidence value should be multiply by this before being returned.
        This value may change.

        skill_descriptions
        A list of strings. Default is an empty list.
        Those strings are descriptions of the skill provided by the adapter.
        Basically they are replies to the question : "Why did you said that ?".

        coefficient_method
        A string. Default is None.
        The name of the method that will be called each time alan is speaking

        allowed_to_repeat
        A boolean. Default is False.
        Is the logic adapter allowed to repeat himself during a conversation
        """
        super().__init__(**kwargs)

        # getting max_confidence
        try:
            self.max_confidence = float(kwargs.get('max_confidence', 1))
        except ValueError:
            raise TypeError("max_confidence must be a number")

        # getting min_confidence
        try:
            self.min_confidence = float(kwargs.get('min_confidence', 0))
        except ValueError:
            raise TypeError("min_confidence must be a number,you are doing n importe quoi")

        # getting confidence_coefficient
        try:
            coef = kwargs.get('confidence_coefficient', self.max_confidence)
            self.confidence_coefficient = float(coef)
        except ValueError:
            raise TypeError("confidence_coefficient must be a number")

        # getting skill_descriptions
        self.skill_descriptions = kwargs.get('skill_description', [])
        if type(self.skill_descriptions) != list:
            raise TypeError("skill_descriptions must be a list")

        # getting name
        self.identifier = kwargs.get('identifier', None)
        if type(self.identifier) != str:
            raise TypeError("identifier must be a string")

        # getting confidence_coefficient
        process_done_method = kwargs.get('process_done_method', None)
        if process_done_method:
            if process_done_method == "sawtooth":
                self.process_done = self.sawtooth
            elif process_done_method == "one_shot":
                self.process_done = self.one_shot
            elif process_done_method == "reinforcement":
                self.process_done = self.reinforcement
            elif process_done_method == "greetings":
                self.process_done = self.greetings
            else:
                raise ValueError("%s is not an AlanLogicAdapter method"
                                % process_done_method)

        # getting allowed_to_repeat
        self.allowed_to_repeat = kwargs.get('allowed_to_repeat', False)
        if type(self.allowed_to_repeat) != bool:
            raise TypeError("identifier must be a bool")


    def get_confidence_coefficient(self):
        """getter for confidence_coefficient"""
        return self._confidence_coefficient

    def set_confidence_coefficient(self, value):
        """setter for confidence_coefficient"""
        if value < 0: value = 0
        elif value > 1: value = 1
        self._confidence_coefficient = value

    confidence_coefficient = property(get_confidence_coefficient,
                                      set_confidence_coefficient)

    def constrain_confidence(self, confidence=1):
        """Return a value constrained between min_confidence and max_confidence.
        """
        if confidence > self.max_confidence:
            return self.max_confidence
        if confidence < self.min_confidence:
            return self.min_confidence
        return confidence

    def get_confidence(self, confidence=1):
        """Return a value multiplied by confidence_coefficient (and constrained)
        """
        confidence *= self.confidence_coefficient
        return self.constrain_confidence(confidence)

    def justification(self):
        """Return a justification (skill_description)"""
        return choice(self.skill_descriptions)

    def process_done(self, is_selected=False):
        """should be overwritted
        Will be called each time alan need a response.
        Will be called with, is_selected=True when le LogicAdapter is selected/
        """
        pass

    def sawtooth(self, is_selected=False):
        """increase the confidence coefficient
        when adapter is selected set it to 0
        """
        self.confidence_coefficient += 0.05
        if is_selected:
            self.confidence_coefficient = 0

    def reinforcement(self, is_selected=False):
        """increase the confidence coef to max confidence coef when adapter is
        selected. If Alan respond with another adapter two consecutive times,
        the confidence is set to min confidence until the adapter is selected
         again"""
        if not hasattr(self, 'count') :
            self.count = 1
        if is_selected:
            self.confidence_coefficient = self.max_confidence
            self.count = 1
        else :
            if self.count < 2 :
                self.count += 1
            else :
                self.confidence_coefficient = self.min_confidence

    def one_shot(self, is_selected=False):
        """decrease the confidence coef to min confidence coef when the adapter
         was selected and stop been selected."""
        if not hasattr(self, 'count') :
            self.count = 1
        if is_selected:
            if self.count == 1:
                self.confidence_coefficient = self.max_confidence
                self.count = 2
        else :
            if self.count == 2 :
                self.confidence_coefficient = self.min_confidence

    def greetings(self, is_selected=False):
        """increase the confidence coef to max confidence coef when adapter is
        selected. If Alan respond with another adapter two consecutive times,
        the confidence is set to min confidence and stay it"""
        if not hasattr(self, 'count') :
            self.count = 1
        if is_selected:
            if self.count == 1:
                self.confidence_coefficient = self.max_confidence
            self.count = 2
        else :
            if self.count > 1 :
                if self.count > 2 :
                    self.confidence_coefficient = self.min_confidence
                self.count += 1
