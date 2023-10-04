from db.mymodel import session, Teacher, Student, StudyGroup, Subject, Mark
from sqlalchemy import func, desc
from random import choice


def select_1() -> list[tuple()]:
    return session.query(Student.name, func.round(func.avg(Mark.mark), 2)
                         .label("AVG Mark"))\
                   .select_from(Mark).join(Student)\
                   .group_by(Student.id)\
                   .order_by(desc("AVG Mark")).limit(5).all()


def select_2(subject_name: str) -> list[tuple()]:
    return session.query(Subject.name, Student.name,
                         func.round(func.avg(Mark.mark), 2).label("AVG Mark"))\
                   .select_from(Student).join(Mark).join(Subject)\
                   .filter(Subject.name == subject_name)\
                   .group_by(Subject.name, Student.name)\
                   .order_by(desc("AVG Mark")).limit(1).all()


def select_3(subject_name: str) -> list[tuple()]:
    return session.query(Subject.name, StudyGroup.code,
                         func.round(func.avg(Mark.mark), 2).label("AVG Mark"))\
                   .select_from(Subject).join(Mark).join(Student).join(StudyGroup)\
                   .filter(Subject.name == subject_name)\
                   .group_by(Subject.name, StudyGroup.code)\
                   .order_by(StudyGroup.code).all()


def select_4():
    return session.query(func.round(func.avg(Mark.mark), 2).label("AVG Mark"))\
                   .select_from(Mark).scalar()


def select_5(teacher_name: str) -> list[tuple()]:
    return session.query(Teacher.name, Subject.name)\
                   .select_from(Teacher).join(Subject)\
                   .filter(Teacher.name == teacher_name)\
                   .order_by(Subject.name).all()


def select_6(group_code: str) -> list[tuple()]:
    return session.query(StudyGroup.code, Student.name)\
                   .select_from(StudyGroup).join(Student)\
                   .filter(StudyGroup.code == group_code)\
                   .order_by(Student.name).all()


def select_7(group_code: str, subject_name: str) -> list[tuple()]:
    return session.query(StudyGroup.code, Subject.name, Student.name,
                         Mark.mark, Mark.date_mark)\
                   .select_from(StudyGroup).join(Student).join(Mark).join(Subject)\
                   .filter(StudyGroup.code == group_code,
                           Subject.name == subject_name)\
                   .order_by(Student.name, Mark.date_mark).all()


def select_8(teacher_name: str) -> list[tuple()]:
    return session.query(Teacher.name, func.round(func.avg(Mark.mark), 2))\
                   .select_from(Teacher).join(Subject).join(Mark)\
                   .filter(Teacher.name == teacher_name)\
                   .group_by(Teacher.name).all()


def select_9(student_name: str) -> list[tuple()]:
    return session.query(Student.name, Subject.name)\
                   .select_from(Student).join(Mark).join(Subject)\
                   .filter(Student.name == student_name)\
                   .order_by(Student.name).all()


def select_10(student_name: str, teacher_name: str) -> list[tuple()]:
    return session.query(Student.name, Teacher.name, Subject.name)\
                   .select_from(Teacher).join(Subject).join(Mark).join(Student)\
                   .filter(Teacher.name == teacher_name,
                           Student.name == student_name)\
                   .distinct().order_by(Subject.name).all()


def select_11(student_name: str, teacher_name: str) -> list[tuple()]:
    return session.query(Student.name, Teacher.name,
                         func.round(func.avg(Mark.mark), 2).label("AVG Mark"))\
                   .select_from(Teacher).join(Subject).join(Mark).join(Student)\
                   .filter(Teacher.name == teacher_name,
                           Student.name == student_name)\
                   .group_by(Student.name, Teacher.name).all()


def select_12(group_code: str, subject_name: str) -> list[tuple()]:
    max_date = session.query(Mark.date_mark)\
                   .select_from(StudyGroup).join(Student).join(Mark).join(Subject)\
                   .filter(StudyGroup.code == group_code,
                           Subject.name == subject_name)\
                   .order_by(Mark.date_mark.desc()).limit(1).scalar()
    return session.query(StudyGroup.code, Subject.name, Mark.date_mark, Student.name,
                         Mark.mark)\
                   .select_from(StudyGroup).join(Student).join(Mark).join(Subject)\
                   .filter(StudyGroup.code == group_code,
                           Subject.name == subject_name,
                           Mark.date_mark == max_date)\
                   .order_by(Student.name, Mark.date_mark).all()


def get_random_subject() -> str:
    subject_names = session.query(Subject.name).all()
    return choice(subject_names)[0]


def get_random_student() -> str:
    student_names = session.query(Student.name).all()
    return choice(student_names)[0]


def get_random_teacher() -> str:
    teacher_names = session.query(Teacher.name).all()
    return choice(teacher_names)[0]


def get_random_group() -> str:
    group_codes = session.query(StudyGroup.code).all()
    return choice(group_codes)[0]


if __name__ == "__main__":
    print(*select_1(), sep="\n")
    print(*select_2(subject_name=get_random_subject()))
    print(*select_3(subject_name=get_random_subject()), sep="\n")
    print(select_4())
    print(*select_5(teacher_name=get_random_teacher()), sep="\n")
    print(*select_6(group_code=get_random_group()), sep="\n")
    print(*select_7(get_random_group(), get_random_subject()), sep="\n")
    print(*select_8(teacher_name=get_random_teacher()))
    print(*select_9(student_name=get_random_student()), sep="\n")
    print(*select_10(get_random_student(), get_random_teacher()), sep="\n")
    print(*select_11(get_random_student(), get_random_teacher()), sep="\n")
    print(*select_12(get_random_group(), get_random_subject()), sep="\n")
