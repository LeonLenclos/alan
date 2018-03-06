from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
import utils
import re

class AimeAdapter(AlanLogicAdapter):
    """This adapter answer to questions about what someone or something loves,
     that is questions concerning the 'aime' relation like 'Est ce que concept_A
    aime concept_B'.
    If he don't know if he loves the concept that is asked for, Alan choose
    randomly if he loves it or not. If he don't know if concept_A loves
    concept_B he asks for it with aimeask adaptor"""

    def __init__(self, **kwargs):
        """Required kwarg :

        questions
        A list of strings.
        The question that must be answered with this adapter.

        relation
        A list of strings.
        The nature of the questions that must be answered with this adapter

        ask
        A list of strings
        The question used to ask for a relation for an unknown concept.
        Ask will include a specifier for the concept which is asked :
        "Pourrais tu me dire en quelques mots ce qu'est %(concept_A)s."
         """


        super().__init__(**kwargs)

        # Getting relation
        try:
            self.relation = kwargs['relation']
        except KeyError:
            raise KeyError('relation is a required argument')
        if type(self.relation) != str:
            raise TypeError("relation must be a string")



    def can_process(self, statement):
        # Process only if the latest statement in the conversation
        # contain the relation
        return (self.relation in statement.text)

    def process(self, statement):
        relation=self.relation
        if ("aime[s]*-" or "aime[s]*[- ]tu " or "aime[s]*[- ]t[- ]il") in
                                                            statement.text:
            if "aime[s]*[ -]tu " in statement.text :
                concept_A="tu"
                concept_B=re.sub(".*aime[- ]tu ","",statement.text)
                concept_B=utils.remove_punctuation(concept_B, False)
            elif "aime[s]*[- ]t[- ]il" in statement.context:
                concept_A=statement.text.split("aime[s]*[- ]t[- ]il")[0])
                concept_B=statement.text.split("aime[s]*[- ]t[- ]il")[1])
            else:
                statment_out = Statement(""response"")
                statment_out.confidence = self.get_confidence(0)
                return statment_out

        else:
            concept_A=statement.text.split(self.relation)[0]
            concept_A=utils.remove_punctuation(concept_A, False)
            # Here, we also remove the "est ce que" expression
            concept_A = re.sub("([eE]st[ -]ce[ -]que)","",statement.text)
            concept_B=statement.text.split(self.relation)[1]
            concept_B=utils.remove_punctuation(concept_B, False)
            # Here, we also remove the "est ce que" expression
            concept_A = re.sub("([eE]st[ -]ce[ -]que)","",statement.text)

        # The following block allow the kezako adapter to answer to the "Qu'est
        # ce que..." and "Qu'est ce qu'..." questions.
        # Because this questions can have another meaning if a verb follow the
        # question e.g in "Qu'est ce que tu fais"
        # If you uncomment the block, don't forget to add this two questions to
        # the questions into the settings.json file
        #   #Remove the chain " ce que " from concept_A (because of "Qu'est ce
        #    que..." questions)
        #   concept_A = re.sub("^( ce que )","",concept_A)
        #   #Remove the chain " ce qu' " from concept_A (because of "Qu'est ce
        #    qu'..." qu'est)
        #   concept_A = re.sub("^( ce qu')","",concept_A)

        # Get the distance between input statement and questions list
        confidence = 1

        # ici on change met la fonction de leon pour changer des trucs



        # If concept_A is related by the relation to another concept, put
        # this concept into concept_B
        if self.chatbot.storage.get_related_concept(concept_A, self.relation)
        == concept_B :
            concept_A = concept_A.lower().capitalize()
            # Answer the question
            response = concept_A+" "+relation+" "+concept_B+"."
        concept_C = self.chatbot.storage.get_related_concept(concept_A,
                                                    self.relation, reverse=True)



                                                    
        # If concept_A is related by the relation to another concept, put
        # this concept into concept_B
        if concept_B :
            # Answer the question
            response = "%(A)s %(rel)s %(B)s."
            if concept_C :
                response += " D'ailleurs comme %(C)s %(rel)s %(A)s, %(C)s %(rel)s aussi %(B)s."
        # If a concept is related to concept_A by the relation, put
        # this concept into concept_C
        elif  concept_C:
            # Answer and ask
            response = ("%(C)s %(rel)s %(A)s mais je ne sais pas vraiment ce que %(A)s %(rel)s. "
            +self.ask)
        # Else ask for a concept related to concept_A
        else:
            # Answer and ask
            response = ("Je ne sais pas ce qu'est %(A)s "
                     + self.ask)

        response = response % {"A":concept_A, "B":concept_B, "C":concept_C, "rel":self.relation }
        # Verify that concept_A is non-empty or to big (more than 4 words),
        #  if it is then change confidence to 0
        if len(concept_A) == 0 or len(concept_A.split(" "))>4:
            confidence=0


        statment_out = Statement(response.capitalize())
        statment_out.confidence = self.get_confidence(confidence)

        return statment_out

            return statment_out
