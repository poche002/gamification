from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from pecan import conf

Base = declarative_base()

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True)
    badge_id = Column(String)
    amount_necessary = Column(Integer)
    description = Column(String)
    image = Column(String)
    title = Column(String)
    data1 = Column(String)

    def __repr__(self):
        return "<Badge(amount_necessary'%s')>" % (self.amount_necessary)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    fullname = Column(String)
    password = Column(String)
    email = Column(String)

    def __repr__(self):
        return "<User(user_id='%s', fullname='%s', password='%s', email='%s')>" % (self.user_id, self.fullname, self.password, self.email)

class UserBadges(Base):
    __tablename__ = 'user_badges'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    badge_id = Column(Integer, ForeignKey('badges.id'), primary_key=True)
    cant_act = Column(Integer)

    user = relationship(User, backref='users')
    badge = relationship(Badge, backref='badges')

    def __init__(self, badge, user, cant_act=0):
        self.user = user
        self.badge = badge
        self.cant_act = cant_act


    def __repr__(self):
        return "<userBadge(amount_existing'%s')>" % (self.cant_act)



Session = scoped_session(sessionmaker())

def _engine_from_config(configuration):
    configuration = dict(configuration)
    url = configuration.pop('url')
    return create_engine(url, **configuration)

def init_model():
    conf.sqlalchemy.engine = _engine_from_config(conf.sqlalchemy)
    Base.metadata.create_all(conf.sqlalchemy.engine)

def start():
    Session.bind = conf.sqlalchemy.engine
    Base.metadata.bind = Session.bind

def start_read_only():
    start()

def commit():
    Session.commit()

def rollback():
    Session.rollback()

def clear():
    Session.remove()

def get_user(user_id):
    return Session.query(User).filter_by(user_id=user_id).first()

def get_badge(badge_id):
    return Session.query(Badge).filter_by(badge_id=badge_id).first()

def get_all_users():
    return Session.query(User).all()

def get_all_badges():
    return Session.query(Badge).all()

def create_user(user_id, fullname, password, email):
    new_user = User(user_id=user_id, fullname=fullname, password=password, email=email)
    Session.add(new_user)
    for badge_aux in Session.query(Badge).all():
        Session.add(UserBadges(user=new_user, badge=badge_aux, cant_act=0))


def create_badge(badge_id, amount_nec, desc, image, title, data1="null"):
    new_badge = Badge(badge_id=badge_id, amount_necessary=amount_nec, description=desc, image=image, title=title, data1=data1)
    Session.add(new_badge)
    for user_aux in Session.query(User).all():
        Session.add(UserBadges(user=user_aux, badge=new_badge, cant_act=0))

def delete_user(user_id):
    try:
        us_id = Session.query(User).filter_by(user_id=user_id).first().id
        Session.query(UserBadges).filter_by(user_id=us_id).delete()
        return Session.query(User).filter_by(user_id=user_id).delete()
    except AttributeError:
        return 0

def delete_badge(badge_id):
    try:
        ba_id = Session.query(Badge).filter_by(badge_id=badge_id).first().id
        Session.query(UserBadges).filter_by(badge_id=ba_id).delete()
        return Session.query(Badge).filter_by(badge_id=badge_id).delete()
    except AttributeError:
        return 0

def set_user(user_id_old, user_id, fullname, password, email):
    if Session.query(User).filter_by(user_id=user_id_old).first():
        Session.query(User).filter_by(user_id=user_id_old).first().fullname = fullname
        Session.query(User).filter_by(user_id=user_id_old).first().password = password
        Session.query(User).filter_by(user_id=user_id_old).first().email = email
        Session.query(User).filter_by(user_id=user_id_old).first().user_id = user_id
        return True
    else:
        return False

def set_badge(badge_id_old, badge_id, amount_necessary, description, image, title, data1):
    if Session.query(Badge).filter_by(badge_id=badge_id_old).first():
        Session.query(Badge).filter_by(badge_id=badge_id_old).first().amount_necessary = amount_necessary
        Session.query(Badge).filter_by(badge_id=badge_id_old).first().description = description
        Session.query(Badge).filter_by(badge_id=badge_id_old).first().image = image
        Session.query(Badge).filter_by(badge_id=badge_id_old).first().title = title
        Session.query(Badge).filter_by(badge_id=badge_id_old).first().data1 = data1
        Session.query(Badge).filter_by(badge_id=badge_id_old).first().badge_id = badge_id
        return True
    else:
        return False

def set_user_badge(user_id, badge_id, cant_sum):
    try:
        ba_id = Session.query(Badge).filter_by(badge_id=badge_id).first().id
        us_id = Session.query(User).filter_by(user_id=user_id).first().id
        user_badge = Session.query(UserBadges).filter_by(user_id=us_id, badge_id=ba_id).first()
        user_badge.cant_act = user_badge.cant_act+cant_sum
        return True
    except AttributeError:
        return False

