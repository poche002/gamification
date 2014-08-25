from pecan              import conf  # noqa
from sqlalchemy         import create_engine, MetaData
from sqlalchemy.orm     import sessionmaker, scoped_session
from test_project.model import model




def init_model():
    """
    This is a stub method which is called at application startup time.

    If you need to bind to a parsed database configuration, set up tables or
    ORM classes, or perform any database initialization, this is the
    recommended place to do it.

    For more information working with databases, and some common recipes,
    see http://pecan.readthedocs.org/en/latest/databases.html
    """
    #conf.sqlalchemy.engine = _engine_from_config(conf.sqlalchemy)
    pass

