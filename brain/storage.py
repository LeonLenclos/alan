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

    def get_response_model(self):
        """
        Return the response model.
        """
        from models import Response
        return Response

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
        Response = self.get_model('response')
        Tag = self.get_model('tag')

        if statement:
            session = self.Session()

            record = Statement(text=statement.text)
            record.extra_data = dict(statement.extra_data)

            for _tag in statement.tags:
                tag = session.query(Tag).filter_by(name=_tag).first()

                if not tag:
                    # Create the record
                    tag = Tag(name=_tag)

                record.tags.append(tag)

            # Get or create the response records as needed
            for response in statement.in_response_to:
                _response = session.query(Response).filter_by(
                    text=response.text,
                    statement_text=statement.text
                ).first()

                if _response:
                    _response.occurrence += 1
                else:
                    # Create the record
                    _response = Response(
                        text=response.text,
                        statement_text=statement.text,
                        occurrence=response.occurrence
                    )

                record.in_response_to.append(_response)

            session.add(record)

            self._session_finish(session)
