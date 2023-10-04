from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import configparser
import pathlib

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'user')
password = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

url = f'postgresql://{username}:{password}@{domain}:5432/{db_name}'
Base = declarative_base()
engine = create_engine(url, echo=True, pool_size=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(40), nullable=False)
    # subjects = relationship('Subject', back_populates='teachers')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    phone = Column(String(40), nullable=False)
    # study_groups = relationship('StudyGroup', back_populates='students')
    # marks = relationship('Mark', back_populates='students')


class StudyGroup(Base):
    __tablename__ = 'study_groups'
    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    student = relationship(Student, backref='study_group')

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id'))
    teacher = relationship(Teacher, backref='subject')
    # marks = relationship('Mark', back_populates='subjects')


class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    mark = Column(Integer, nullable=False)
    date_mark = Column(Date, nullable=False)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship(Student, backref='marks')
    subject = relationship(Subject, backref='marks')
