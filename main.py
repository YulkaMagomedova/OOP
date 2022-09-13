class Person:

    def __init__(self, name, surname, gender=None, role=None):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.role = role

    def introduce(self):
        return f'Имя: {self.name} \nФамилия: {self.surname} ' \
               f'\nПол: {self.gender if self.gender is not None else "не указан"} ' \
               f'\nДолжность {self.role}'


class Student(Person):
    student_instances = []

    def __init__(self, name, surname, gender=None, role='Студент'):
        Person.__init__(self, name, surname, gender)
        self.__class__.student_instances.append(self)
        self.finished_courses = []
        self.courses_in_progress = []
        self.role = role
        self.grades = {}

    def __str__(self):
        return f'{self.introduce()} \nСредняя оценка за домашние задания: {str(self.get_middle_grade())} ' \
               f'\nКурсы в процессе изучения: {", ".join(self.get_courses_in_progress())} ' \
               f'\nЗавершенные курсы: {", ".join(self.get_finished_courses())} \n'

    def __eq__(self, other):
        if self.role != other.role:
            raise TypeError('Сравнение некорректно!')
        else:
            return self.get_middle_grade() == other.get_middle_grade()

    def __gt__(self, other):
        if self.role != other.role:
            raise TypeError('Сравнение некорректно!')
        else:
            return self.get_middle_grade() > other.get_middle_grade()

    def __ge__(self, other):
        if self.role != other.role:
            raise TypeError('Сравнение некорректно!')
        else:
            return self.get_middle_grade() >= other.get_middle_grade()

    def get_middle_grade(self):
        if len(self.grades) != 0:
            summ = sum([sum(self.grades[j]) for j in self.grades])
            count = sum([len(self.grades[j]) for j in self.grades])
            return round((summ / count), 1)
        else:
            return 0

    def get_courses_in_progress(self):  # list
        if len(self.courses_in_progress) != 0:
            return self.courses_in_progress
        else:
            return ['Нет текущих курсов']

    def get_finished_courses(self):     # list
        if len(self.finished_courses) != 0:
            return self.finished_courses
        else:
            return ['Нет завершенных курсов']

    def grade_mentor(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) \
                and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Курсы не совпадают!'


class Mentor(Person):
    mentor_instances = []

    def __init__(self, name, surname, gender=None, role='Ментор'):
        Person.__init__(self, name, surname, gender, role)
        self.__class__.mentor_instances.append(self)
        self.courses_attached = []


class Lecturer(Mentor):
    lecturer_instances = []

    def __init__(self, name, surname, gender=None, role='Лектор'):
        Mentor.__init__(self, name, surname, gender, role)
        self.__class__.lecturer_instances.append(self)
        self.grades = {}

    def __str__(self):
        return f'{self.introduce()} \nСредняя оценка за лекции: {str(self.get_middle_grade())}\n'

    def __eq__(self, other):
        if self.role != other.role:
            raise TypeError('Сравнение некорректно!')
        else:
            return self.get_middle_grade() == other.get_middle_grade()

    def __gt__(self, other):
        if self.role != other.role:
            raise TypeError('Сравнение некорректно!')
        else:
            return self.get_middle_grade() > other.get_middle_grade()

    def __ge__(self, other):
        if self.role != other.role:
            raise TypeError('Сравнение некорректно!')
        else:
            return self.get_middle_grade() >= other.get_middle_grade()

    def get_middle_grade(self):
        if len(self.grades) != 0:
            summ = sum([sum(self.grades[j]) for j in self.grades])
            count = sum([len(self.grades[j]) for j in self.grades])
            return round((summ / count), 1)
        else:
            return 0


class Reviewer(Mentor):
    reviewer_instances = []

    def __init__(self, name, surname, gender=None, role='Ревьюер'):
        Mentor.__init__(self, name, surname, gender, role)
        self.__class__.reviewer_instances.append(self)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Курсы не совпадают!'

    def __str__(self):
        return f'{self.introduce()} \n'


def get_student_middle_grade(cours):
    grade_list = [j.grades.get(cours) for j in Student.student_instances]
    middle_grade_sum = 0
    k = 0
    for f in grade_list:
        if f is not None:
            c = 0
            summ = 0
            for j in f:
                c += 1
                summ += j
            middle_grade_sum += summ / c
            k += 1
    return round(middle_grade_sum / k, 1) if k > 0 else 'Нет оценок'


def get_lecturer_middle_grade(cours):
    grade_list = [j.grades.get(cours) for j in Lecturer.lecturer_instances]
    middle_grade_sum = 0
    k = 0
    for f in grade_list:
        if f is not None:
            c = 0
            summ = 0
            for j in f:
                c += 1
                summ += j
            middle_grade_sum += summ / c
            k += 1
    return round(middle_grade_sum / k, 1) if k > 0 else 'Нет оценок'


stud1 = Student("Антонина", "Суходрищенко", "женский")
stud2 = Student("Ахмеджон", "Бюблюоглы", "мужской")
stud3 = Student("Петя", "Ленивый", "мужской")

rev1 = Reviewer("Саша", "Белый")
rev2 = Reviewer("Рубен", "Хачапурян")

lec1 = Lecturer("Диана", "Гордская", "женский")
lec2 = Lecturer("Гавриил", "Православович")

stud1.courses_in_progress = ["Python", "C++", "PHP", "Java", "Kotlin", "Ruby", "TurboPascal"]
stud1.finished_courses = ["Microsoft Office"]

stud2.courses_in_progress += ["Python"]

rev1.courses_attached = ["Python", "GO", "PHP"]
rev2.courses_attached += ["C++", "Java"]

lec1.courses_attached += ["Python", "Go", "Java", "C#", "Fortran", "JS", "C++", "PHP", "Scratch"]
lec2.courses_attached += ["C++", "Python"]

rev1.rate_hw(stud1, "Python", 8)
rev1.rate_hw(stud1, "Python", 6)
rev1.rate_hw(stud1, "Python", 4)
rev1.rate_hw(stud2, "Python", 10)
rev1.rate_hw(stud2, "GO", 10)

rev2.rate_hw(stud1, "C++", 5)
rev2.rate_hw(stud2, "Python", 10)
rev2.rate_hw(stud2, "Python", 10)

stud1.grade_mentor(lec1, "Python", 7)
stud1.grade_mentor(lec2, "C++", 5)
stud2.grade_mentor(lec1, "Python", 6)
stud1.grade_mentor(lec2, "Python", 7)

ppl_list = Reviewer.reviewer_instances + Lecturer.lecturer_instances + Student.student_instances
print("Список всех персонажей:\n")
for i in ppl_list:
    print(i)

courses = 'Python'
print('Средняя оценка студентов за задания по теме', courses, ':', get_student_middle_grade("Python"))
print('Средняя оценка лекторов за лекции по теме', courses, ':', get_lecturer_middle_grade("Python"))
