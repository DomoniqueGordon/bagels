import sqlalchemy as sa

from sqlalchemy.orm import declared_attr, declarative_base, relationship, declarative_mixin
from sqlalchemy.sql import func


Base = declarative_base()

@declarative_mixin
class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {"schema": "bagels"}
    id = sa.Column(sa.INTEGER, primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP, server_default=func.now())


class Games(BaseMixin, Base):
    guess_count = sa.Column(sa.BIGINT)


class SecretNumbers(BaseMixin, Base):
    __tablename__ = "secret_numbers"
    game_id = sa.Column(sa.INTEGER, sa.ForeignKey("bagels.games.id"))
    number = sa.Column(sa.INTEGER)
    games = relationship("Games", backref="secret_numbers")



if __name__ == "__main__":
    conn_string = "mysql+pymysql://bagels:bagels@localhost:3307/bagels"
    engine = sa.create_engine(conn_string, echo=True)
    Base.metadata.create_all(engine)