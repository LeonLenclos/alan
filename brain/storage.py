from chatterbot.storage import SQLStorageAdapter

# This is the chatterbot's SQLStorageAdapter modified for Alan
# The idea is to record each statement even if same already exist
# So it is not clean at all.

# does not record Response objects
# conversation not really well recorded yet


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

    def update(self, statement):
        """
        Creates an entry in the database.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        if statement:
            session = self.Session()

            record = Statement()
            record.text = statement.text
            record.extra_data = dict(statement.extra_data)

            for _tag in statement.tags:
                tag = session.query(Tag).filter_by(name=_tag).first()

                if not tag:
                    # Create the record
                    tag = Tag(name=_tag)

                record.tags.append(tag)

            session.add(record)

            self._session_finish(session)

    def create(self):
        """
        Populate the database with the tables.
        """
        from models import Base
        Base.metadata.create_all(self.engine)


    def get_latest_response(self, conversation_id):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
        """
        Statement = self.get_model('statement')

        session = self.Session()
        statement = None


        query = session.query(Statement)
        query = query.filter(Statement.conversations.any(id=conversation_id))
        query = query.order_by(Statement.id).limit(2).first()

        if query:
            statement = query.get_statement()

        session.close()

        return statement
