from chatterbot.storage import SQLStorageAdapter
from sqlalchemy import desc
from models import Base

# This is the chatterbot's SQLStorageAdapter modified for Alan
# does not record Response objects



class AlanSQLStorageAdapter(SQLStorageAdapter):
    """A storage_adapter for alan"""

    def __init__(self, **kwargs):
        super(AlanSQLStorageAdapter, self).__init__(**kwargs)

    def get_statement_model(self):
        """
        Return the statement model.
        """
        from models import Statement
        return Statement

    def get_conversation_model(self):
        """
        Return the conversation model.
        """
        from models import Conversation
        return Conversation

    def get_tag_model(self):
        """
        Return the conversation model.
        """
        from models import Tag
        return Tag

    def store(self, statement):
        """
        Creates an statement entry in the database. Return the statement id.
        """

        # Get models
        Statement = self.get_model('statement')
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

        Statement = self.get_model('statement')
        Conversation = self.get_model('conversation')

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


    def create(self):
        """
        Populate the database with the tables.
        """
        Base.metadata.create_all(self.engine)

    def get_latest_statement(self, conversation_id=None, speaker=None, offset=0):
        """Return a Statement
        default for conversation_id any
        default for speaker is anybody
        default for index is 0 (0 is latest)
        """
        Statement = self.get_model('statement')

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



    def get_latest_response(self, conversation_id):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
        """

        return self.get_statement()
