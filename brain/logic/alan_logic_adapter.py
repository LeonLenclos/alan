
class AlanLogicAdapter(LogicAdapter):
    """AlanLogicAdapter is a superclass for Alan's logic adapters
    """

    def __init__(self, **kwargs):
        """Optional kwargs :

        max_confidence
        A float (from 0 to 1). Default is 1.
        The logici adapter should never return a greater confidence value.
        This value should not change.

        confidence_coefficient
        A float (from 0 to 1). Default is max_confidence.
        The confidence value should be multiply by this before being returned.
        This value may change.

        skill_descriptions
        A list of strings. Default is an empty list.
        Those strings are descriptions of the skill provided by the adapter.
        Basically they are replies to the question : "Why did you said that ?".
        """
        super().__init__(**kwargs)

        # getting max_confidence
        try:
            self.max_confidence = float(kwargs.get('max_confidence', 1))
        except ValueError:
            raise TypeError("max_confidence must be a number")

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

    def constrain_confidence(self, confidence):
        """Return a value constrained between 0 and max_confidence.
        """
        if confidence > self.max_confidence:
            return self.max_confidence
        if confidence < 0:
            return 0
        return confidence

    def scale_confidence(self, confidence):
        """Return a value multiplied by confidence_coefficient (and constrained)
        """
        confidence *= self.confidence_coefficient
        return self.constrain_confidence(confidence)
