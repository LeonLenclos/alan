from chatterbot.storage import SQLStorageAdapter

class AlanSQLStorageAdapter(SQLStorageAdapter):
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
        Statement = self.get_statement_model()
        Tag = self.get_model('tag')

        if statement:
            session = self.Session()

            record = Statement()
            record.text = statement.text
            record.extra_data = dict(statement.extra_data)
            print(record.test)

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
