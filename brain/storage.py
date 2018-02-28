from chatterbot.storage import SQLStorageAdapter
from sqlalchemy import desc
from models import Base
from models import Statement, Conversation, Tag, Concept, ConceptAssociation

# This is the chatterbot's SQLStorageAdapter modified for Alan
# does not record Response objects

class AlanSQLStorageAdapter(SQLStorageAdapter):
    """A storage_adapter for alan"""

    def __init__(self, **kwargs):
        super(AlanSQLStorageAdapter, self).__init__(**kwargs)


    def store(self, statement):
        """
        Creates an statement entry in the database. Return the statement id.
        """

        # Get models
        Tag = self.get_model('tag')

        if statement:

            session = self.Session()

            # Create record
            record = Statement()

            # set statement text
            record.text = statement.text

            # set speaker name
            record.speaker = statement.extra_data["speaker"]

            # set extra data
            record.extra_data = dict(statement.extra_data)

            # and tags
            for _tag in statement.tags:
                tag = session.query(Tag).filter_by(name=_tag).first()

                if not tag:
                    # Create the record
                    tag = Tag(name=_tag)

                record.tags.append(tag)

            # store it
            session.add(record)
            session.flush()

            stored_statement_id = record.id

            self._session_finish(session)
            return stored_statement_id

    def add_to_conversation(self, conversation_id, statement, response):
        """
        Add the statement and response to the database and to the conversation.
        """
        session = self.Session()

        conversation = session.query(Conversation).get(conversation_id)

        statement_id = self.store(statement)
        response_id = self.store(response)

        statement_query = session.query(Statement).filter_by(id=statement_id)
        response_query = session.query(Statement).filter_by(id=response_id)

        conversation.statements.append(statement_query.first())
        conversation.statements.append(response_query.first())

        session.add(conversation)
        self._session_finish(session)

    def store_concept(self, concept):
        """
        Add the concept and return the concept id
        if the concept already exist, just return the id
        """
        concept = concept.lower()

        session = self.Session()

        query = session.query(Concept).filter_by(name=concept)
        record = query.first()

        if not record :
            record = Concept(name=concept)
            session.add(record)

        session.flush()
        record_id = record.id

        self._session_finish(session)
        return record_id

    def store_concept_association(self, concept_A, relation, concept_B):
        """
        Add concepts and relation to the association table
        Also store concept if needed
        """
        relation = relation.lower()

        session = self.Session()

        concept_A_id = self.store_concept(concept_A)
        concept_B_id = self.store_concept(concept_B)

        query = session.query(ConceptAssociation).filter_by(
            concept_A_id=concept_A_id,
            relation=relation,
            concept_B_id=concept_B_id)
        if not query.first():
            record = ConceptAssociation(
                concept_A_id=concept_A_id,
                relation=relation,
                concept_B_id=concept_B_id)
            session.add(record)

        self._session_finish(session)

    def create(self):
        """
        Populate the database with the tables.
        """
        Base.metadata.create_all(self.engine)

    def get_latest_statement(self, conversation_id=None, speaker=None, offset=0):
        """Return a Statement
        default for conversation_id is any
        default for speaker is anybody
        default for offset is 0 (0 is latest)
        """

        session = self.Session()
        statement = None

        query = session.query(Statement)

        if conversation_id:
            query = query.filter(Statement.conversations.any(id=conversation_id))
        if speaker:
            query = query.filter(Statement.speaker == speaker)

        query = query.order_by(Statement.id.desc())
        query = query.limit(1)
        query = query.offset(offset)
        query = query.first()

        if query:
            statement = query.get_statement()

        session.close()
        return statement

    def get_related_concept(self, concept, relation):
        """Return a Concept that have a relation with another concept
        Return None if nothing is found
        """

        session = self.Session()

        concept_A_id = self.store_concept(concept)
        query = session.query(ConceptAssociation)
        query = query.filter_by(concept_A_id=concept_A_id, relation=relation)
        association = query.first()
        if association:
            concept_B_id = association.concept_B_id
            query = session.query(Concept)
            query = query.filter_by(id=concept_B_id)
            concept_B = query.first()

            session.close()
            return concept_B.name

        session.close()
        return None


    def get_latest_response(self, conversation_id):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
        """

        return self.get_statement()

    def count_conv(self):
        pass
