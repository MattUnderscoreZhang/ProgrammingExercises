from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# we define database tables, and classes which will be mapped to those tables
# these two taks are usually performed together with a system called declarative extensions
Base = declarative_base()

# we can define any number of mapped classes from base
# here we define the table and mapped class at the same time
class User(Base):
    __tablename__ = 'users'
    # tables require one or more columns marked as primary_key
    # https://docs.sqlalchemy.org/en/14/faq/ormconfiguration.html#faq-mapper-primary-key
    # integer primary key should auto increment
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    fullname = Column(String(64))
    nickname = Column(String(64))
    def __repr__(self) -> str:
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}')>"

# we can check the table definition by using the metadata attribute of the base class
# User.__table__

# we create an engine that represents the core interface to the database
# it uses a dialect that handles the database details and the DBAPI in use
# the engine has not tried to connect to the database yet
# when engine.execute() or engine.connect() is called, the engine will establish a connection
# we don't typically use the engine directly though
# echo=True will log all the generated SQL to stdout
engine = create_engine('sqlite:///:memory:', echo=True)

# to connect to a postgres database, we would use psycopg2
# https://stackoverflow.com/questions/9353822/connecting-postgresql-with-sqlalchemy
# engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')

# create all tables defined by our metadata
print("Creating tables")
Base.metadata.create_all(engine)
print()

# ID should return None
bella = User(name='Bella', fullname='Bella Zhang', nickname='Belbie')
print("Bella:", bella)
print(bella.id)
print()

# have to create a session to talk to the database
Session = sessionmaker(bind=engine)
session = Session()

# instance is pending, but not yet in the database
# the database is not touched until we call session.commit() or until the data is used
session.add(bella)

# actually returns the same object
print("Adding Bella")
bella_search = session.query(User).filter_by(name='Bella')[0]
print("Bella search:", bella_search)
print(bella == bella_search)
print(bella.id)
print()

# add more users
session.add_all([
    User(name='Alice', fullname='Alice Smith', nickname='Al'),
    User(name='Cindy', fullname='Cindy Jones', nickname='Cindy'),
    User(name='Daisy', fullname='Daisy Brown', nickname='Daisy'),
])
print(session.new)
print()

print("Adding users")
print("Users:", session.query(User).all())
print()

print("Changing a user")
bella.nickname = "Beelzebella"
print(session.dirty)
print()

print("Users:", session.query(User).all())
print()

# manually commit the changes by flushing the session
# subsequent operations with this session will be in a new transaction and reacquire resources
session.commit()
