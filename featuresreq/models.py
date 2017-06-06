"""
Database models
"""
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.types import ChoiceType as Choice

session_factory = sessionmaker()


class Base(object):
    """Base Model class"""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

Base = declarative_base(cls=Base)


class Client(Base):
    name = sa.Column(sa.Unicode, nullable=False)


class FeatureRequest(Base):
    """Feature request"""
    PRODUCT_AREAS = (
        ('Policies', 'Policies'),
        ('Billing', 'Billing'),
        ('Claims', 'Claims'),
        ('Reports', 'Reports'),
    )

    title = sa.Column(sa.Unicode, nullable=False)
    description = sa.Column(sa.UnicodeText, nullable=False)
    client_id = sa.Column(sa.Integer, sa.ForeignKey(Client.id), nullable=False)
    priority = sa.Column(sa.Integer, nullable=False)
    target_date = sa.Column(sa.Date, nullable=False)
    product_area = sa.Column(Choice(PRODUCT_AREAS), nullable=False)

    client = relationship(Client, backref="feature_requests")

    __table_args__ = (
        sa.UniqueConstraint('client_id', 'priority', name='_feature_req_client_priority_uq'),
    )

