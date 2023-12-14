import json

class Database:
    def __init__(self, db_file="database.json"):
        self.db_file = db_file
        self.load_database()

    def load_database(self):
        try:
            with open(self.db_file, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = {'instructors': {}, 'students': {}}
            self.save_database()

    def save_database(self):
        with open(self.db_file, 'w') as file:
            json.dump(self.users, file, indent=2)

    def add_user(self, user_type, username, password):
        self.users[user_type][username] = {'password': password}
        self.save_database()

    def authenticate_user(self, user_type, username, password):
        user_data = self.users.get(user_type, {}).get(username)
        return user_data and user_data['password'] == password
    
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Instructor(User):
    def __init__(self, username, password, expertise):
        super().__init__(username, password)
        self.expertise = expertise
        self.courses = []

    def create_course(self, title, description):
        new_course = Course(title, description, instructor=self)
        self.courses.append(new_course)
        return new_course

    def update_course(self, course, new_title=None, new_description=None):
        if course in self.courses:
            course.update(new_title, new_description)

    def add_course(self, course):
        self.courses.append(course)

    def remove_course(self, course):
        self.courses.remove(course)

    def manage_course(self, course):
        # falta implentar essa funcionalidade
        pass

class student(User):
    def __init__(self, username, email, student_id):
        self.username = username
        self.email = email
        self.student_id = student_id
        self.enrolled_courses = []

    def enroll_in_course(self, course):
        if course not in self.enrolled_courses and self in ui.students:
            self.enrolled_courses.append(course)
            course.enroll_student(self)
            print(f"Inscrição de '{self.username}' no curso '{course.title}' realizada com sucesso.")
        else:
            print(f"{self.username} já está inscrito no curso '{course.title}'.")

    def view_course_content(self, course):
        # Lógica para visualizar o conteúdo do curso
        pass

    def submit_assignment(self, assignment, submission_text):
        # Lógica para enviar uma tarefa
        pass

class Course:
    def __init__(self, title, description, instructor):
        self.title = title
        self.description = description
        self.instructor = instructor
        self.modules = []
        self.enrolled_students = []

    def update(self, new_title=None, new_description=None):
        if new_title:
            self.title = new_title
        if new_description:
            self.description = new_description

    def add_module(self, module):
        self.modules.append(module)

    def enroll_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(f"Estudante '{student.name}' inscrito no curso '{self.title}' com sucesso.")
        else:
            print(f"Estudante '{student.name}' já está inscrito no curso '{self.title}'.")
    def get_enrolled_students(self):
        if not self.enrolled_students:
            print(f"Não há estudantes inscritos no curso '{self.title}'.")
        else:
            print(f" Estudantes inscritos no curso '{self.title}':")
            for student in self.enrolled_students:
                print(f"  - {student.name}")

class Module:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.videos = []
        self.quizzes = []
        self.assignments = []

    def add_video(self, video_title, video_url, video_format):
        video = Video(video_title, video_url, video_format)
        self.videos.append(video)
    
    def add_quiz(self, quiz_title, quiz_questions):
        quiz = Quiz(quiz_title, quiz_questions)
        self.quizzes.append(quiz)

    def add_assignment(self, assignment_title, assignment_description):
        assignment = Assignment(assignment_title, assignment_description)
        self.assignments.append(assignment)

class Video:
    def __init__(self, title, url, format):
        self.title = title
        self.url = url
        self.format =  format

class Quiz:
    def __init__(self, title, questions):
        self.title = title
        self.questions = questions

class Assignment:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.submissions = []

    def submit(self, student, submission_text):
        submission = Submission(student, submission_text)
        self.submissions.append(submission)

class Submission:
    def __init__(self, student, text):
        self.student = student
        self.text = text

class UserInterface:
    def __init__(self, db):
        self.instructor = []
        self.students = []
        self.db = db
        self.logged_in_user = None

    def login(self):
        print("Bem-vindo à Plataforma de Cursos JV!\n")

        while True:
            username = input("Digite seu nome de usuário (ou pressione Enter para sair): ")
            if not username:
                break

            password = input("Digite sua senha: ")

            user_type = self.get_user_type(username)

            if user_type and self.db.authenticate_user(user_type, username, password):
                self.logged_in_user = username
                if user_type == 'instructors':
                    # Verifica se o instrutor já está na lista
                    instructor = next((inst for inst in self.instructor if inst.username == username), None)
                    if instructor is None:
                        instructor = Instructor(username, password, expertise="alguma_especialidade")
                        self.instructor.append(instructor)
                print(f"Bem-vindo, {username}!")
            else:
                print("Usuário ou senha inválidos. Tente novamente.")

    def get_user_type(self, username):
        if username in self.db.users['instructors']:
            return 'instructors'
        elif username in self.db.users['students']:
            return 'students'
        else:
            return None
    
    def start(self):
        if self.logged_in_user:
            print("Login realizado com sucesso. Acesse as funcionalidades apropriadas para o tipo de usuário.")
            user_type = self.get_user_type(self.logged_in_user)

            if user_type == 'instructors':
                self.display_instructor_menu()
            elif user_type == 'students':
                self.display_student_menu()
            else:
                print("Tipo de usuário inválido.")
        else:
            print("Nenhum usuário logado. Faça o login primeiro.")

    def display_instructor_menu(self):
        while True:
            print("\nOpções para Instrutores:")
            print("1.  Criar Curso")
            print("2.  Atualizar Informações do Curso")
            print("3.  Atualizar Conteúdo do Módulo")
            print("4.  Remover Conteúdo do Módulo")
            print("5.  Adicionar Módulo")
            print("6.  Remover Módulo")
            print("7.  Mostrar Cursos e Módulos Criados")
            print("0.  Sair")

            choice = input("Escolha uma opção (0-7): ")

            if choice == '1':
                self.create_course()
            elif choice == '2':
                self.update_course_information()
            elif choice == '3':
                self.update_module_content()
            elif choice == '4':
                self.remove_module_content()
            elif choice == '5':
                self.add_module()
            elif choice == '6':
                self.remove_module()
            elif choice == '7':
                self.display_created_courses_and_modules()
            elif choice == '0':
                break
            else:
                print("Opção inválida. Tente novamente.")

    def display_student_menu(self):
        while True:
            print("\nOpções para Estudantes:")
            print("1.  Matricular-se em um Curso")
            print("2.  Mostrar Cursos Inscritos")
            print("0.  Sair")

            choice = input("Escolha uma opção (0-2): ")

            if choice == '1':
                self.enroll_students_in_course()
            elif choice == '2':
                self.display_enrolled_courses()
            elif choice == '0':
                break
            else:
                print("Opção inválida. Tente novamente.")

    def create_course(self):
        if not self.instructors:
            print("Nenhum instrutor disponível para criar um curso.")
            return

        instructor = self.instructors[0]  # Assumindo que haja apenas um instrutor logado, ajuste conforme necessário
        course_title = input("Digite o título do curso: ")
        course_description = input("Digite a descrição do curso: ")
        new_course = instructor.create_course(title=course_title, description=course_description)
        
        # Adição de módulos
        while True:
            module_title = input("Digite o título do módulo (ou pressione Enter para encerrar): ")
            if not module_title:
                break
            module_content = input("Digite o conteúdo do módulo: ")
            module = Module(title=module_title, content=module_content)
            new_course.add_module(module)

        self.display_course_details(new_course)

    def register_student(self):
        student_name = input("Digite o nome do estudante: ")
        student_id = input("Digite o ID do estudante: ")
        student_email = input("Digite o email do estudante: ")
        new_student = student(name=student_name, email=student_email, student_id=student_id)
        print(f"Estudante '{new_student.name}' criado com sucesso.")
        self.students.append(new_student)

    def update_course_information(self):
        update_course_title = input("Digite o título do curso que deseja atualizar: ")

        # Verificando se o curso existe
        for course in self.instructor.courses:
            if update_course_title == course.title:

                new_course_title = input("Digite o novo título do curso (ou pressione Enter para manter o mesmo): ")

                new_course_description = input("Digite a nova descrição do curso (ou pressione Enter para manter a mesma): ")

                self.instructor.update_course(course, new_title=new_course_title, new_description=new_course_description)
                break
        else:
            print("Curso não encontrado. Não foi possível realizar a atualização.")

    def update_module_content(self):
        update_module_title = input("Digite o título do módulo que deseja atualizar: ")

        # Verificando se o módulo existe
        for course in self.instructor.courses:
            for module in course.modules:
                if update_module_title == module.title:
            
                    new_module_content = input("Digite o novo conteúdo do módulo (ou pressione Enter para manter o mesmo): ")

                    module.content = new_module_content
                    print(f"Conteúdo do módulo '{module.title}' atualizado com sucesso.")
                    break
            else:
                continue
            break
        else:
            print("Módulo não encontrado. Não foi possível realizar a atualização.")

    def remove_module_content(self):
        remove_module_title = input("Digite o título do módulo que deseja remover o conteúdo: ")

        # Verificando se o módulo existe
        for course in self.instructor.courses:
            for module in course.modules:
                if remove_module_title == module.title:
                    module.content = ""
                    print(f"Conteúdo do módulo '{module.title}' removido com sucesso.")
                    break
            else:
                continue
            break
        else:
            print("Módulo não encontrado. Não foi possível remover o conteúdo.")

    def add_module(self):
        
        if not self.instructor.courses:
            print("Não há cursos disponíveis para adicionar um módulo.")
            return

        print("Cursos disponíveis:")
        for i, course in enumerate(self.instructor.courses, 1):
            print(f"{i}. {course.title}")

        while True:
            try:
                course_index = int(input("Escolha o número do curso para adicionar o módulo: ")) - 1
                selected_course = self.instructor.courses[course_index]
                break
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")

        module_title = input("Digite o título do novo módulo: ")
        module_content = input("Digite o conteúdo do novo módulo: ")
        new_module = Module(title=module_title, content=module_content)

        #Adicionando videos aos módulos

        while True:
            video_title = input("Digite o título do vídeo (ou pressione Enter para encerrar): ")
            if not video_title:
                break
            video_url = input("Digite a URL do vídeo: ")
            video_format = input("Digite o formato do vídeo: ")
            new_module.add_video(video_title, video_url, video_format)
        
        #Adicionando questionários aos módulos

        while True:
            quiz_title = input("Digite o título do quiz (ou pressione Enter para encerrar): ")
            if not quiz_title:
                break
            quiz_questions = input("Digite as questões do quiz: ")
            new_module.add_quiz(quiz_title, quiz_questions)

        #Adicionando tarefas aos modulos

        while True:
            assignment_title = input("Digite o título da tarefa (ou pressione Enter para encerrar): ")
            if not assignment_title:
                break
            assignment_description = input("Digite a descrição da tarefa (ou pressione Enter para encerrar): ")
            new_module.add_assignment(assignment_title, assignment_description)

        selected_course.add_module(new_module)
        print(f"Novo módulo '{new_module.title}' adicionado ao curso '{selected_course.title}' com sucesso.")

    def remove_module(self):

        if not self.instructor.courses:
            print("Não há cursos disponíveis para remover um módulo.")
            return

        print("Cursos disponíveis:")
        for i, course in enumerate(self.instructor.courses, 1):
            print(f"{i}. {course.title}")

        while True:
            try:
                course_index = int(input("Escolha o número do curso para remover o módulo: ")) - 1
                selected_course = self.instructor.courses[course_index]
                break
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")


        print(f"Módulos disponíveis no curso '{selected_course.title}':")
        for i, module in enumerate(selected_course.modules, 1):
            print(f"{i}. {module.title}")


        while True:
            try:
                module_index = int(input("Escolha o número do módulo para remover: ")) - 1
                removed_module = selected_course.modules.pop(module_index)
                print(f"Módulo '{removed_module.title}' removido do curso '{selected_course.title}' com sucesso.")
                break
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")

    def display_course_details(self, course):
        print("\nDetalhes do Curso:")
        print(f"Título: {course.title}")
        print(f"Descrição: {course.description}")
        print("Módulos:")
        for module in course.modules:
            print(f"  - {module.title}: {module.content}")

    def display_created_courses_and_modules(self):
        print("\nCursos e Módulos Criados:")
        for course in self.instructor.courses:
            self.display_course_details(course)

    def display_instructor_details(self):
        print("\nDetalhes do Instrutor:")
        print(f"Nome: {self.instructor.username}")
        print(f"Especialidade: {self.instructor.expertise}")
        print("Cursos:")
        for course in self.instructor.courses:
            print(f"  - {course.title}")
    
    def enroll_students_in_course(self):
        if not self.instructors:
            print("Não há instrutores disponíveis para matricular estudantes.")
            return

        print("Instrutores disponíveis:")
        for i, instructor in enumerate(self.instructors, 1):
            print(f"{i}. {instructor.username}")

        while True:
            try:
                instructor_index = int(input("Escolha o número do instrutor para matricular estudantes: ")) - 1
                selected_instructor = self.instructors[instructor_index]
                break
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")

        if not selected_instructor.courses:
            print(f"O instrutor '{selected_instructor.username}' não possui cursos disponíveis para matricular estudantes.")
            return

        print("Cursos disponíveis:")
        for i, course in enumerate(selected_instructor.courses, 1):
            print(f"{i}. {course.title}")

        while True:
            try:
                course_index = int(input("Escolha o número do curso para matricular estudantes: ")) - 1
                selected_course = selected_instructor.courses[course_index]
                break
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")

        while True:
            student_username = input("Digite o nome de usuário do estudante a ser matriculado (ou pressione Enter para encerrar): ")
            if not student_username:
                break

            found_students = [student for student in self.students if student.username == student_username]
            if found_students:
                selected_student = found_students[0]
                selected_student.enroll_in_course(selected_course)
            else:
                print(f"Estudante '{student_username}' não encontrado. Crie o estudante primeiro.")

    def display_enrolled_students(self):
        if not self.instructor.courses:
            print("Não há cursos disponíveis para mostrar os estudantes inscritos.")
            return
        
        print(f"Cursos disponíveis:")
        for i, course in enumerate(self.instructor.courses, 1):
            print(f"{i}. {course.title}")

        while True:
            try:
                course_index = int(input("Escolha o número do curso para mostrar os estudantes inscritos: ")) - 1
                selected_course = self.instructor.courses[course_index]
                break
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")
        
        selected_course.get_enrolled_students()

db = Database()
db.add_user("instructors", "joao.victor", "jv123")
db.add_user("students", "estudante1", "senha456")

instructor_auth = db.authenticate_user("instructors", "joao.victor", "jv123")
student_auth = db.authenticate_user("students", "estudante1", "senha456")

ui = UserInterface(db)
ui.login()
ui.start()