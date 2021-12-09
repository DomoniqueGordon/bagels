import logging
import sqlalchemy as sa

from sqlalchemy.orm import session, sessionmaker
from sqlalchemy import select, update

from database.models.base import Base, Games, SecretNumbers, Guesses
from sqlalchemy import func


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DBConn:
    def __init__(self, **kwargs):
        self.host = "localhost"
        self.username = "bagels"
        self.password = "bagels"
        self.database = "bagels"
        self.port = 3307
        self.log = logger
    
    @property
    def _conn_str(self) -> str:
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}"

    def get_engine(self):
        return sa.create_engine(self._conn_str, echo=True)
    
    def get_session(self):
        engine = self.get_engine()
        Session = session.sessionmaker(bind=engine)
        return Session()
    
    

class DBSetup(DBConn):
    def _create_tables(self):
        engine = self.get_engine()
        engine.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        Base.metadata.create_all(engine)
    
    def reset(self):
        engine = self.get_engine()
        Base.metadata.drop_all(engine)
        engine.execute(f"DROP DATABASE IF EXISTS {self.database}")

    def setup(self):
        self._create_tables()


class ApplicationDatabase(DBSetup):
    def add_row(self, row):
        session = self.get_session()
        session.add(row)
        session.commit()
    
    def run_query(self, query):
        session = self.get_session()
        session.execute(query)
        session.commit()

    def start_game(self, number=123):
        self.end_game()
        game = Games(secret_numbers=[SecretNumbers(number=number)])
        self.add_row(game)

    def end_game(self, outcome="L"):
        query = update(Games).where(Games.active==1).values(active=0, outcome=outcome, ended_at=func.now())
        self.run_query(query)
        self.log.warning("Game has been ended.")

    def add_guess(self, number=123):
        session = self.get_session()
        query = session.query(func.max(Games.id))
        id = session.execute(query).fetchone()[0]
        game_id = id
        guess = Guesses(number=number, game_id=game_id)
        self.add_row(guess)
    
    




if __name__ == '__main__':
    db = ApplicationDatabase()
    #db.reset()
    #db.setup()
    db.start_game()
    #db.end_game()
