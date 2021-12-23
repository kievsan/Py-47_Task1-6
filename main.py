# PD-47
# PY-47
# Task 1.6
# «Объекты и классы. Инкапсуляция, наследование и полиморфизм»


_person_roles = []  # для списка ролей всех типов участников образовательного процесса


def append_person_role(roles, new_role):
    """
    Собираем роли участников при создании неабстрактных классов
    :param roles:
    :param new_role:
    :return: new_role
    """
    new_role = str(new_role).strip().lower().title()
    if not new_role:
        new_role = 'Чёрти-кто'
    if not (new_role in roles):
        roles.append(new_role)
        print(f'Добавлена новая роль "{new_role}".')
    return new_role


def get_person_gender():
    return {'M': 'муж', 'W': 'жен'}


def get_err_message():
    return 'error'


def display_list(any_list):
    if any_list:
        return ", ".join([str(i) for i in any_list])
    return "отсутствуют!"


def who_is_the_best_person(person_list):
    """
    Поиск лучших в списке в своём классе,
    класс берётся из первого в списке, если он способен оцениваться
    Иначе - возврат ошибки
    :param person_list: список участников
    :return: лучший или ошибка
    """
    if not person_list:
        return get_err_message()
    max_person = person_list[0]
    print(f'ПОИСК: лучший {max_person.get_purpose()} в группе:')
    if not (isinstance(max_person, Student) or
            isinstance(max_person, Lecturer)):
        return get_err_message()
    for person in person_list:
        print(f'{person.introduce_herself()}', end="")
        result = max_person.__lt__(person)
        if result == get_err_message():
            print(end=", ")
            continue
        print(f' - {person.get_average_grade()} бал.', end=", ")
        if result:
            max_person = person
    return max_person


def display_who_is_the_best(person_list):
    """
    Распечатка результата поиска лучшего в списке
    :param person_list: список участников
    :return:
    """
    result = who_is_the_best_person(person_list)
    if result == get_err_message():
        print('Ошибки сравнения - операция прервана!')
    else:
        print(f'\nЛучший {result.get_purpose().lower()}: '
              f'{result.name} {result.surname} - '
              f'{result.get_average_grade()} бал.\n')


def get_average_of_course_grades(person_list, course, person_class):
    """
    Рассчёт для всего списка средней оценки за курс,
    если участник принадлежит определенному классу
    :param person_list: список людей
    :param course: название курса (str)
    :param person_class: класс участников для расчёта ср.оценки
    :return: средняя оценка
    """
    if not person_list:
        return 0
        # return "оценки отсутствуют!"
    number_of_grades = 0
    sum_of_grades = 0
    for person in person_list:
        if person.__class__ != person_class:
            continue
        course_grades = person.get_course_grades(course)
        if course_grades:
            print(course_grades)
            number_of_grades += len(course_grades)
            sum_of_grades += sum(course_grades)
    if number_of_grades == 0:
        return 0
    return sum_of_grades / number_of_grades


def get_students_average_grade_of_course(person_list, course, display=False):
    average_grade = round(get_average_of_course_grades(person_list,
                                                       course,
                                                       some_student.__class__), 2)
    if display:
        print(f'Средняя оценка за домашние задания по всем студентам '
              f'в рамках курса "{course}" - {average_grade} бал.\n')
    return average_grade


def get_lecturers_average_grade_of_course(person_list, course, display=False):
    average_grade = round(get_average_of_course_grades(person_list,
                                                       course,
                                                       some_lecturer.__class__), 2)
    if display:
        print(f'Средняя оценка за лекции всех лекторов '
              f'в рамках курса "{course}" - {average_grade} бал.\n')
    return average_grade


class _Person:

    def __init__(self, name, surname,
                 gender=get_person_gender()['M'],
                 person_role='Студент'):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.person_role = person_role
        self.grades = {}

    def __str__(self):
        return (f'{self.get_purpose()} ({self.gender}):\n'
                f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n')

    def __lt__(self, other):
        if (isinstance(other, self.__class__) and
                (isinstance(self, Student) or isinstance(self, Lecturer))):
            return self.get_average_grade() < other.get_average_grade()
        # print("Ошибка сравнения!\n")
        return get_err_message()

    def get_purpose(self):
        return self.person_role

    def introduce_herself(self):
        return f'{self.name} {self.surname} ({self.get_purpose().lower()})'

    def get_average_grade(self):
        """
        Рассчитать среднюю оценку человека по всем курсам вместе
        :return: средняя оценка
        """
        grades = self.grades
        if not grades:
            return 0
            # return "оценки отсутствуют!"
        number_of_grades = 0
        sum_of_grades = 0
        for list_of_grades in grades.values():
            number_of_grades += len(list_of_grades)
            sum_of_grades += sum(list_of_grades)
        return sum_of_grades / number_of_grades

    def gives_grade(self, evaluated_person, course_name, grade):
        """
        Ставим оценку на курсе
        :param evaluated_person: оцениваемый
        :param course_name: название курса
        :param grade: оценка
        :return: True - успех операции
        """
        if course_name in evaluated_person.grades:
            evaluated_person.grades[course_name] += [grade]
        else:
            evaluated_person.grades[course_name] = [grade]
        print(f'{self.introduce_herself()} ставит оценку за курс "{course_name}": '
              f'{evaluated_person.introduce_herself()} - {grade} бал.\n')
        return True

    def get_course_grades(self, course_name):
        """
        Выбрать оценки за курс
        :param course_name: название курса
        :return: список оценок
        """
        course_grades = []
        if course_name in self.grades:
            course_grades += self.grades[course_name]
        return course_grades

    def display_error_message(self, message):
        print(f'{self.introduce_herself()} оОшибся {message}!\n')


class Student(_Person):
    _who_are_you = append_person_role(_person_roles, 'Студент')
    _activity = 'учится'

    def __init__(self, name, surname, gender=get_person_gender()['M']):
        super(Student, self).__init__(name, surname, gender, self._who_are_you)
        self.__finished_courses = []
        self.__courses_in_progress = []

    def __str__(self):
        return (f'{super(Student, self).__str__()}'
                f'Средняя оценка за домашние задания: {round(self.get_average_grade(), 1)}\n'
                f'Курсы в процессе изучения: {display_list(self.get_courses_in_progress())}\n'
                f'Завершенные курсы: {display_list(self.get_finished_courses())}\n')

    def gives_grade(self, evaluated_person, course_name, grade):
        """
        Студенты ставят оценки за качество курса
        :param evaluated_person: оцениваемый
        :param course_name: название курса
        :param grade: оценка
        :return: True - успешная операция
        """
        if (isinstance(evaluated_person, Lecturer)
                and course_name in self.get_courses_in_progress()
                and course_name in evaluated_person.get_courses_attached()):
            super(Student, self).gives_grade(evaluated_person, course_name, grade)
            return True
        self.display_error_message('при выставлении оценки')

    def lets_start_course(self, course_name):
        """
        Запись на курс
        :param course_name:  название курса
        :return: сообщение выполнении
        """
        report = 'уже'
        if not (course_name in self.__courses_in_progress):
            report = 'теперь'
            self.__courses_in_progress.append(course_name)
        print(f'{self.introduce_herself()} {report} {self._activity} на курсе "{course_name}"!\n')

    def lets_finish_course(self, course_name):
        """
        Завершение курса
        :param course_name: название курса
        :return: сообщение выполнении
        """
        report = 'не изучал'
        if course_name in self.__courses_in_progress:
            self.__courses_in_progress.remove(course_name)
            self.__finished_courses.append(course_name)
            report = 'завершил'
        print(f'{self.introduce_herself()} {report} курс {course_name}!\n')

    def get_finished_courses(self):
        return self.__finished_courses

    def get_courses_in_progress(self):
        return self.__courses_in_progress


class _Mentors(_Person):
    _who_are_you = 'Ментор'
    _activity = 'преподаёт'

    def __init__(self, name, surname, gender=get_person_gender()['M'], mentor_role=_who_are_you):
        super(_Mentors, self).__init__(name, surname, gender, self._who_are_you)
        self.person_role = mentor_role
        self.__courses_attached = []

    def get_purpose(self):
        return (f'{super(_Mentors, self).get_purpose()}'
                f'-{self._who_are_you}')

    def gives_grade(self, evaluated_person, course_name, grade):
        if (isinstance(self, Reviewer) and isinstance(evaluated_person, Student)
                and course_name in self.get_courses_attached()
                and course_name in evaluated_person.get_courses_in_progress()):
            super(_Mentors, self).gives_grade(evaluated_person, course_name, grade)
            return True
        self.display_error_message('при выставлении оценки')

    def add_course(self, course_name):
        report = 'уже'
        if not (course_name in self.__courses_attached):
            report = 'теперь'
            self.__courses_attached.append(course_name)
        print(f'{self.introduce_herself()} {report} {self._activity} на курсе "{course_name}"!\n')

    def get_courses_attached(self):
        return self.__courses_attached


class Lecturer(_Mentors):
    _who_are_you = append_person_role(_person_roles, 'Лектор')
    _activity = 'читает лекции'

    def __str__(self):
        return (f'{super(Lecturer, self).__str__()}'
                f'Средняя оценка за лекции: {round(self.get_average_grade(), 1)}\n')


class Reviewer(_Mentors):
    _who_are_you = append_person_role(_person_roles, 'Ревьювер')
    _activity = 'проверяет работы'


if __name__ == '__main__':
    print(f'Всего ролей: {display_list(_person_roles)}\n')

    best_student = Student('Samanta', 'Eman', get_person_gender()['W'])
    some_student = Student('Taddy', 'Gray')
    print(best_student)
    print(some_student)

    cool_reviewer = Reviewer('Mary', 'Buddy', get_person_gender()['W'])
    some_reviewer = Reviewer('David', 'Fox')
    print(cool_reviewer)
    print(some_reviewer)

    cool_lecturer = Lecturer('Anna', 'Red', get_person_gender()['W'])
    some_lecturer = Lecturer('Alex', 'Writer')
    print(cool_lecturer)
    print(some_lecturer)

    best_student.lets_finish_course("Python")

    cool_reviewer.add_course('Python')
    best_student.lets_start_course('Python')

    cool_reviewer.gives_grade(best_student, 'Python', 10)
    cool_reviewer.gives_grade(best_student, 'Python', 9)
    cool_reviewer.gives_grade(best_student, 'Python', 8)

    cool_lecturer.add_course('Python')

    best_student.gives_grade(cool_reviewer, 'Python', 6)
    best_student.gives_grade(cool_lecturer, 'Python', 8)
    best_student.gives_grade(cool_lecturer, 'Python', 9)
    best_student.gives_grade(cool_lecturer, 'Python', 10)

    some_reviewer.add_course('Git')
    best_student.lets_start_course('Git')

    some_lecturer.add_course('Git')
    best_student.gives_grade(some_lecturer, 'Git', 4)
    best_student.gives_grade(some_lecturer, 'Python', 6)
    some_lecturer.add_course('Python')
    best_student.gives_grade(some_lecturer, 'Python', 6)
    best_student.gives_grade(some_lecturer, 'Git', 5)

    print(best_student)
    best_student.lets_finish_course("Python")
    print(best_student)

    print(some_student.grades)
    print(some_student)

    print(cool_lecturer.grades)
    print(cool_lecturer)
    print(some_lecturer.grades)
    print(some_lecturer)

    print(cool_reviewer)
    print(some_reviewer)

    print(some_lecturer.__lt__(cool_lecturer))
    print(best_student.__lt__(some_student))
    print(some_lecturer.__lt__(some_student))
    print()

    display_who_is_the_best((cool_lecturer, some_student, best_student, some_lecturer))

    display_who_is_the_best((some_student, cool_lecturer, best_student, some_lecturer))

    display_who_is_the_best((some_reviewer, cool_lecturer, some_student, best_student, some_lecturer))
    print()

    get_students_average_grade_of_course((cool_lecturer, some_student,
                                          best_student, some_lecturer),
                                         'Python', True)

    get_lecturers_average_grade_of_course((some_reviewer, cool_lecturer,
                                           some_student, best_student,
                                           some_lecturer), 'Python', True)
