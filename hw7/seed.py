from faker import Faker
from datetime import datetime, timedelta
from random import randint, choice, sample, randrange, shuffle
from db.mymodel import session, Teacher, Student, StudyGroup, Subject, Mark

STUDENTS_MIN = 30
STUDENTS_MAX = 50
NUMBER_GROUPS = 3
SUBJECTS_MIN = 5
SUBJECTS_MAX = 8
TEACHERS_MIN = 3
TEACHERS_MAX = 5
MARKS_MAX = 20
MARK_MIN = 2
MARK_MAX = 5
DATE_MIN = "2023-01-23"
DATE_MAX = "2023-05-19"

SUBJECTS = [
    'Algebra',
    'Biology',
    'Drawing',
    'Chemistry',
    'Geography',
    'Geometry',
    'History',
    'Literature',
    'Mathematics',
    'Music',
    'Physical education',
    'Physics',
    'Technology'
]


def get_date_pool(date_min: str = DATE_MIN, date_max: str = DATE_MAX) -> list[str]:
    date_pool = []
    d = datetime.strptime(date_min, "%Y-%m-%d").date()
    date_finish = datetime.strptime(date_max, "%Y-%m-%d").date()
    while d <= date_finish:
        if d.weekday() < 5:
            date_pool.append(d)
#            date_pool.append(d.strftime("%Y-%m-%d"))
        d = d + timedelta(days=1)
    return date_pool


def generate_fake_data(n_students, n_teachers, n_subjects, n_groups, n_marks, date_pool) -> tuple():
    fake_subjects = []
    fake_students = []
    fake_teachers = []
    fake_groups = []
    fake_marks = []
    students_groups = {}
    for i in range(n_groups):
        students_groups[i] = []
    fake_data = Faker()
    for i in range(n_students):
        fake_students.append((fake_data.name(), fake_data.phone_number(), fake_data.email()))
        students_groups[randrange(n_groups)].append(i + 1)
        for _ in range(randint(n_subjects, n_marks)):
            mark = randint(MARK_MIN, MARK_MAX)
            subject_id = randrange(n_subjects) + 1
            student_id = i + 1
            date_mark = choice(date_pool)
            fake_marks.append((mark, subject_id, student_id, date_mark))
    for _ in range(n_teachers):
        fake_teachers.append((fake_data.name(), fake_data.phone_number(), fake_data.email()))
    teachers_for_subjects = [i % n_teachers for i in range(n_subjects)]
    shuffle(teachers_for_subjects)
    for subject in sample(SUBJECTS, min(n_subjects, len(SUBJECTS))):
        teacher_id = teachers_for_subjects[len(fake_subjects)]
        fake_subjects.append((subject, teacher_id + 1))
    for i in range(n_groups):
        for student_id in students_groups[i]:
            fake_groups.append((chr(ord("A") + i), student_id))
    return fake_students, fake_teachers, fake_subjects, fake_groups, fake_marks


def insert_data_to_db(_students, _teachers, _subjects, _groups, _marks) -> None:
    for s in _students:
        new_student = Student(name=s[0], phone=s[1])
        session.add(new_student)
    for t in _teachers:
        new_teacher = Teacher(name=t[0], phone=t[1], email=t[2])
        session.add(new_teacher)
    for s in _subjects:
        new_subject = Subject(name=s[0], teacher_id=s[1])
        session.add(new_subject)
    for g in _groups:
        new_group = StudyGroup(code=g[0], student_id=g[1])
        session.add(new_group)
    for m in _marks:
        new_mark = Mark(
            mark=m[0],
            subject_id=m[1],
            student_id=m[2],
            date_mark=m[3]
        )
        session.add(new_mark)
    session.commit()


if __name__ == "__main__":
    date_pool = get_date_pool(DATE_MIN, DATE_MAX)
    _students, _teachers, _subjects, _groups, _marks = generate_fake_data(
        randint(STUDENTS_MIN, STUDENTS_MAX),
        randint(TEACHERS_MIN, TEACHERS_MAX),
        randint(SUBJECTS_MIN, SUBJECTS_MAX),
        NUMBER_GROUPS,
        MARKS_MAX,
        date_pool
    )
    insert_data_to_db(_students, _teachers, _subjects, _groups, _marks)
