from chatterbot.storage import SQLStorageAdapter
from sqlalchemy import desc
from .models import Base
from .models import Statement, Conversation, Tag, Concept, ConceptAssociation, conversation_association_table

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
            record.speaker = statement.extra_data.get("speaker", None)

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

    def list_concept(self):
        """
        Return a list that contains the concept_name of all the concepts stored
        into the database
        """

        session = self.Session()

        query = session.query(Concept).filter_by()
        record=query.all()
        liste=[]
        for concept in record:
            liste.append(concept.name)



        session.flush()


        self._session_finish(session)
        return liste

    def store_concept_association(self, concept_A, relation, concept_B, negative=False):
        """
        Add concepts and relation to the association table
        Also store concept if needed
        """
        relation = relation.lower()

        session = self.Session()

        concept_A_id = self.store_concept(str.strip(concept_A))
        concept_B_id = self.store_concept(str.strip(concept_B))

        association = dict(concept_A_id=concept_A_id,
                           relation=relation,
                           negative=negative,
                           concept_B_id=concept_B_id)

        query = session.query(ConceptAssociation).filter_by(**association)
        if not query.first():
            record = ConceptAssociation(**association)
            session.add(record)

        self._session_finish(session)

    def create(self):
        """
        Populate the database with the tables.
        """
        Base.metadata.create_all(self.engine)

    def get_latest_statement(self,
                            conversation_id=None,
                            speaker=None,
                            offset=0,
                            text=None):
        """Return a Statement
        default for conversation_id any
        default for speaker is anybody
        default for index is 0 (0 is latest)
        default for text is any
        """

        session = self.Session()
        statement = None

        query = session.query(Statement)

        if conversation_id:
            query = query.filter(Statement.conversations.any(id=conversation_id))
        if speaker:
            query = query.filter(Statement.speaker == speaker)
        if text:
            query = query.filter(Statement.text == text)

        query = query.order_by(Statement.id.desc())
        query = query.limit(1)
        query = query.offset(offset)
        query = query.first()

        if query:
            statement = query.get_statement()

        session.close()
        return statement

    def get_latest_response_extra_data(self, extra_data=None, **kwargs):
        """Return the extra_data of a statement.
        Because it call get_latest_statement, kwargs are the same.
        You should pass also the kwarg extra_data for the key of the extra_data
        you want to receive.
        Default is None and return all the extra_data as a dict
        """
        statement = self.get_latest_statement(**kwargs)

        if statement:
            if extra_data:
                return statement.extra_data.get(extra_data, None)
            return statement.extra_data


    def get_related_concept(self, concept, relation, reverse=False, negative=False):
        """Return a Concept that have a relation with another concept
        Return None if nothing is found
        """

        session = self.Session()

        concept_in_id = self.store_concept(concept)
        query = session.query(ConceptAssociation)

        if reverse:
            query = query.filter_by(concept_B_id=concept_in_id,
                                    relation=relation,
                                    negative=negative)
        else:
            query = query.filter_by(concept_A_id=concept_in_id,
                                    relation=relation,
                                    negative=negative)

        association = query.first()

        if association:
            if reverse:
                concept_out_id = association.concept_A_id
            else:
                concept_out_id = association.concept_B_id

            query = session.query(Concept)
            query = query.filter_by(id=concept_out_id)
            concept_out = query.first()

            session.close()
            return concept_out.name

        session.close()
        return None

    def is_related_concept(self, concept_A, rel, concept_B):
        """Take two concept and a relation
        Return True is the relation is in the database
        Return False if it is in the db but reversed
        Return None if it is not in the db"""

        session = self.Session()

        concept_A_id = self.store_concept(concept_A)
        concept_B_id = self.store_concept(concept_B)

        query = session.query(ConceptAssociation)
        query = query.filter_by(concept_A_id=concept_A_id,
                                relation=rel,
                                concept_B_id=concept_B_id)

        association = query.first()
        if association:
            session.flush()
            negative = association.negative
            session.close()
            return not negative

        session.close()
        return None


    def count_conv(self, conversation_id):
        """
        Return the number of statement in a conversation.
        """
        session = self.Session()

        count = session.query(conversation_association_table)
        count = count.filter_by(conversation_id=conversation_id)
        count = count.count()
        session.close()

        return count
