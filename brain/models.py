from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from chatterbot.ext.sqlalchemy_app.types import UnicodeString
from chatterbot.conversation.statement import StatementMixin

TAG_NAME_MAX_LENGTH, STATEMENT_TEXT_MAX_LENGTH = 50, 400

class ModelBase(object):
    """
    An augmented base class for SqlAlchemy models.
    """

    @declared_attr
    def __tablename__(cls):
        """
        Return the lowercase class name as the name of the table.
        """
        return cls.__name__.lower()

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


Base = declarative_base(cls=ModelBase)


tag_association_table = Table(
    'tag_association',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('statement_id', Integer, ForeignKey('statement.id'))
)


class Tag(Base):
    """
    A tag that describes a statement.
    """

    name = Column(UnicodeString(TAG_NAME_MAX_LENGTH))


class Statement(Base, StatementMixin):
    """
    A Statement represents a sentence or phrase.
    """

    text = Column(UnicodeString(STATEMENT_TEXT_MAX_LENGTH))

    tags = relationship(
        'Tag',
        secondary=lambda: tag_association_table,
        backref='statements'
    )

    extra_data = Column(PickleType)

    def get_tags(self):
        """
        Return a list of tags for this statement.
        """
        return [tag.name for tag in self.tags]

    def get_statement(self):
        from chatterbot.conversation import Statement as StatementObject
        from chatterbot.conversation import Response as ResponseObject

        statement = StatementObject(
            self.text,
            tags=[tag.name for tag in self.tags],
            extra_data=self.extra_data
        )
        return statement


conversation_association_table = Table(
    'conversation_association',
    Base.metadata,
    Column('conversation_id', Integer, ForeignKey('conversation.id')),
    Column('statement_id', Integer, ForeignKey('statement.id'))
)


class Conversation(Base):
    """
    A conversation.
    """

    statements = relationship(
        'Statement',
        secondary=lambda: conversation_association_table,
        backref='conversations'
    )
