from sqlalchemy import Table, Column
from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy import PickleType, Unicode, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base


from chatterbot.conversation import Statement as StatementObject
from chatterbot.conversation import Response as ResponseObject

import sys

# A AMELIORER
if sys.version_info[1] == 5:
    from chatterbot.conversation.statement import StatementMixin
else :
    from chatterbot.conversation import StatementMixin

TAG_NAME_MAX_LENGTH = 50
SPEAKER_NAME_MAX_LENGTH = 50
LOGIC_ADAPER_NAME_MAX_LENGTH = 50
STATEMENT_TEXT_MAX_LENGTH = 400
CONCEPT_TEXT_MAX_LENGTH = STATEMENT_TEXT_MAX_LENGTH
CONCEPT_RELATION_TEXT_MAX_LENGTH = 100

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

    name = Column(Unicode(TAG_NAME_MAX_LENGTH))


class Statement(Base, StatementMixin):
    """
    A Statement represents a sentence or phrase.
    """

    text = Column(Unicode(STATEMENT_TEXT_MAX_LENGTH))

    tags = relationship(
        'Tag',
        secondary=lambda: tag_association_table,
        backref='statements'
    )

    speaker = Column(Unicode(SPEAKER_NAME_MAX_LENGTH))

    extra_data = Column(PickleType)

    def get_tags(self):
        """
        Return a list of tags for this statement.
        """
        return [tag.name for tag in self.tags]

    def get_statement(self):
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

class ConceptAssociation(Base):
    concept_A_id = Column(Integer())
    relation = Column(Unicode(CONCEPT_RELATION_TEXT_MAX_LENGTH))
    negative = Column(Boolean, default=False)
    concept_B_id = Column(Integer())

class Concept(Base):
    name = Column(Unicode(CONCEPT_TEXT_MAX_LENGTH))
