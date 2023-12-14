import json
import getpass
from urllib.parse import urlparse


class Usuario:
    def __init__(self, nome,senha,video=None, quizzes=None,tarefas=None):
        self.nome = nome
        self.senha = senha
        self.video = video
        self.quizzes = quizzes
        self.tarefas = tarefas

class Modulo:
    def __init__(self, titulo, conteudo):
        self.titulo = titulo
        self.conteudo = conteudo
        self.videos = []
        self.quizzes = []
        self.tarefas = []

    def adicionar_video(self,video):
        self.videos.append(video)
        print(f"Vídeo adicionado com sucesso ao módulo.")

class Curso:
    def __init__(self, titulo, descricao, instrutor):
        self.titulo = titulo
        self.descricao = descricao
        self.instrutor = instrutor
        self.modulos = []
        self.videos = []
        self.quizzes = []
        self.tarefas = []
        self.estudantes_matriculados = []
        self.cursos_inscritos = []

    def atualizar_informacoes(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao

    def adicionar_modulo(self, titulo, conteudo):
        modulo = Modulo(titulo, conteudo)
        self.modulos.append(modulo)

    def mostrar_estudantes_matriculados(self):
        print(f"Estudantes matriculados no curso '{self.titulo}':")
        for estudante in self.estudantes_matriculados:
            print(estudante.nome)

    def mostrar_conteudo_estudante(self, estudante):
        print("Módulos disponíveis:")
        for i, modulo in enumerate(self.modulos, start=1):
            print(f"{i}. {modulo.titulo}")

        try:
            modulo_numero = int(input("Escolha o número do módulo que deseja ver o conteúdo: "))
            modulo = self.modulos[modulo_numero - 1]

            print(f"Conteúdo do curso '{self.titulo}'")

            # Exibir informações do módulo
            print(f"\nConteúdo do módulo '{modulo.titulo}'")

            if modulo.videos:
                print("\nVídeos do módulo:")
                for i, video in enumerate(modulo.videos, start=1):
                    print(video)

            if modulo.quizzes:
                print("\nQuizzes do módulo:")
                for i, quiz in enumerate(modulo.quizzes, start=1):
                    print(f"{i}. Pergunta: {quiz['pergunta']}")

            if modulo.tarefas:
                print("\nTarefas do módulo:")
                for i, tarefa in enumerate(modulo.tarefas, start=1):
                    print(f"{i}. Descrição: {tarefa['descricao']}, Prazo: {tarefa['prazo']}")

            while True:
                print("\nEscolha uma opção:")
                print("1. Visualizar vídeo")
                print("2. Responder quiz")
                print("0. Sair")

                escolha_opcao = input("\nDigite o número da opção desejada (ou 0 para voltar para Menu): ")

                if escolha_opcao == '0':
                    break
                elif escolha_opcao == '1' and modulo.videos:
                    
                    print("\nVídeos disponíveis:")
                    for i, video in enumerate(modulo.videos, start=1):
                        print(f"{i}. {video.nome}")
                    
                    
                    escolha_video = int(input("\nDigite o número do vídeo para visualizar: "))
                    video = modulo.videos[escolha_video - 1]

                    print("O que você deseja fazer?")
                    print("1. Marcar como assistido")
                    print("2. Voltar")

                    escolha_assistido = input("\nDigite o número da opção desejada: ")

                    if escolha_assistido == '1':
                        if not video.assistido:
                            self.assistir_video(video, estudante)

                    elif escolha_assistido == '2':
                        print("Voltando ao menu anterior.")
                    else:
                        print("Opção inválida. Voltando ao menu anterior.")
                elif escolha_opcao == '2' and modulo.quizzes:
                    
                    print("\nQuizzes disponíveis:")
                    for i, quiz in enumerate(modulo.quizzes, start=1):
                        print(f"{i}. {quiz['pergunta']}")
    
                    escolha_quiz = int(input("\nDigite o número do quiz para responder: "))
                    quiz = modulo.quizzes[escolha_quiz - 1]
                    
                    print(f"Quiz escolhido: {quiz['pergunta']}")
                    resposta = input("Digite a sua resposta: ").lower().strip()
                    
                    if resposta == quiz['resposta_correta']:
                        print("Resposta correta! Avançando no progresso.")
                        estudante.avancar_progresso()
                    else:
                        print("Resposta incorreta. Tente novamente.")
                    
                else:
                    print("Opção inválida. Tente novamente.")

        except (ValueError, IndexError):
            print("Opção inválida ou curso não encontrado.")


    def assistir_video(self, video, estudante):
        print(f"Assistindo ao vídeo: {video.nome}")
        if video not in estudante.videos_assistidos:
            estudante.videos_assistidos.append(video)
            print("\nVídeo marcado como assistido.")
            estudante.avancar_progresso()
        else:
            print("\nEste vídeo já foi assistido.")


    def mostrar_progresso_estudante(self, estudante):
        total_modulos = len(self.modulos)
        modulos_concluidos = 0

        for i, modulo in enumerate(self.modulos, start=1):
            if estudante.concluiu_modulo(modulo):
                modulos_concluidos += 1

        # if total_modulos > 0:
        #     progresso = (modulos_concluidos / total_modulos) * 100
        #     print(f"\nProgresso no curso '{self.titulo}': {progresso:.2f}%")
        # else:
        #     print(f"\nEste curso '{self.titulo}' não possui módulos.")

class Video:
    def __init__(self, nome, url):
        self.nome = nome
        self.url = url
        self.assistido = False  # vai iniciar como não assistido

    def marcar_como_assistido(self):
        self.assistido = True

    def __str__(self):
        return f"{self.nome} - {self.url}"

class Instrutor(Usuario):
    def __init__(self, nome, senha, quizzes=None, tarefas=None):
        super().__init__(nome, senha,quizzes=quizzes, tarefas=tarefas)
        self.cursos_criados = []

    def criar_curso(self):
        if not isinstance(self, Instrutor):
            print("Apenas instrutores podem criar cursos.")
            return

        titulo = input("Digite o título do curso: ")
        descricao = input("Digite a descrição do curso: ")

        curso = Curso(titulo, descricao, self)
        self.cursos_criados.append(curso)

        plataforma.cursos_criados.append(curso) 
        print(f"Curso '{titulo}' criado com sucesso por {self.nome}.")

         

    def atualizar_informacoes_curso(self):
        if not self.cursos_criados:
            print("Você ainda não criou nenhum curso.")
            return

        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")

        try:
            curso_numero = int(input("Escolha o número do curso que deseja atualizar: "))
            curso_escolhido = self.cursos_criados[curso_numero - 1]

            novo_titulo = input("Digite o novo título do curso: ")
            nova_descricao = input("Digite a nova descrição do curso: ")
            
            curso_escolhido.atualizar_informacoes(novo_titulo, nova_descricao)
            print(f"Informações do curso '{curso_escolhido.titulo}' atualizadas com sucesso.")
        except (ValueError, IndexError):
            print("Opção inválida ou curso não encontrado.")
    
    def adicionar_modulo_curso(self):
        if not self.cursos_criados:
            print("Você ainda não criou nenhum curso.")
            return

        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")

        curso_numero = int(input("Escolha o número do curso para adicionar módulo: "))
        curso = self.cursos_criados[curso_numero - 1]
        titulo_modulo = input("Digite o título do módulo: ")
        conteudo_modulo = input("Digite o conteúdo do módulo: ")
        curso.adicionar_modulo(titulo_modulo, conteudo_modulo)
        print(f"Módulo '{titulo_modulo}' adicionado ao curso '{curso.titulo}'.")


        

    def remover_modulo_curso(self):
        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")
        curso_numero = int(input("Escolha o número do curso para remover módulo: "))
        curso = self.cursos_criados[curso_numero - 1]
        if not curso.modulos:
            print("O curso não possui módulos para remover.")
            return

        print("Módulos disponíveis:")
        for i, modulo in enumerate(curso.modulos, start=1):
            print(f"{i}. {modulo.titulo}")

        escolha = input("Escolha o número do módulo a ser removido: ")
        try:
            escolha = int(escolha)
            modulo_removido = curso.modulos.pop(escolha - 1)
            print(f"Módulo '{modulo_removido.titulo}' removido do curso '{curso.titulo}'.")
        except (ValueError, IndexError):
            print("Opção inválida.")

    def atualizar_conteudo_modulo(self):
        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")
        curso_numero = int(input("Escolha o número do curso para atualizar módulo: "))
        curso = self.cursos_criados[curso_numero - 1]
        if not curso.modulos:
            print("O curso não possui módulos para atualizar.")
            return

        print("Módulos disponíveis:")
        for i, modulo in enumerate(curso.modulos, start=1):
            print(f"{i}. {modulo.titulo}")

        escolha = input("Escolha o número do módulo a ter o conteúdo atualizado: ")
        try:
            escolha = int(escolha)
            modulo_escolhido = curso.modulos[escolha - 1]
            novo_conteudo = input("Digite o novo conteúdo do módulo: ")
            modulo_escolhido.conteudo = novo_conteudo
            print(f"Conteúdo do módulo '{modulo_escolhido.titulo}' atualizado.")
        except (ValueError, IndexError):
            print("Opção inválida.")

    def mostrar_detalhes_curso(self, curso):
        print("\n+++ Detalhes do Curso +++")
        print(f"Título: {curso.titulo}")
        print(f"Descrição: {curso.descricao}")
        print("Módulos:")
        for module in curso.modulos:
            print(f"  - {module.titulo}: {module.conteudo}")

    def mostrar_cursos_modulos_criados(self):
        print("\nCursos e Módulos Criados:")
        for curso in self.cursos_criados:
            print("\n+++ Detalhes do Curso +++")
            print(f"Título: {curso.titulo}")
            print(f"Descrição: {curso.descricao}")
            print("Módulos:")
            for modulo in curso.modulos:
                print(f"  - {modulo.titulo}: {modulo.conteudo}")

    def ver_estudantes_matriculados(self):
        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")

        try:
            curso_numero = int(input("Escolha o número do curso para ver os estudantes matriculados: "))
            curso_escolhido = self.cursos_criados[curso_numero - 1]
            curso_escolhido.mostrar_estudantes_matriculados()
        except (ValueError, IndexError):
            print("Opção inválida ou curso não encontrado.")

    def inserir_conteudo_modulo(self):
        if not self.cursos_criados:
            print("Você ainda não criou nenhum curso.")
            return

        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")

        curso_numero = int(input("Escolha o número do curso para inserir conteúdo: "))
        curso = self.cursos_criados[curso_numero - 1]

        if not curso.modulos:
            print("O curso não possui módulos para inserir conteúdo.")
            return

        print("Módulos disponíveis:")
        for i, modulo in enumerate(curso.modulos, start=1):
            print(f"{i}. {modulo.titulo}")

        modulo_numero = int(input("Escolha o número do módulo para inserir conteúdo: "))
        modulo = curso.modulos[modulo_numero - 1]

        tipo = input("Escolha o tipo de conteúdo (quiz, tarefa, video): ")

        if tipo.lower() == "video":
            
            caminho_video = input("Digite o caminho do arquivo de vídeo ou o link: ")
            conteudo = input("Digite o conteúdo do vídeo: ")

            if self.adicionar_conteudo_modulo(modulo, "video", caminho_video, conteudo):
                print(f"Vídeo adicionado ao módulo '{modulo.titulo}'.")

        elif tipo.lower() == "quiz":
            pergunta = input("Digite a pergunta do quiz: ")
            opcoes = input("Digite as opções do quiz separadas por vírgula: ").split(',')
            resposta_correta = input("Digite a resposta correta do quiz: ")

            quiz = {"pergunta": pergunta, "opcoes": opcoes, "resposta_correta": resposta_correta}
            modulo.quizzes.append(quiz)
            print(f"Quiz adicionado ao módulo '{modulo.titulo}'.")
        elif tipo.lower() == "tarefa":
            descricao_tarefa = input("Digite a descrição da tarefa: ")
            prazo_tarefa = input("Digite o prazo da tarefa: ")

            tarefa = {"descricao": descricao_tarefa, "prazo": prazo_tarefa}
            modulo.tarefas.append(tarefa)
            print(f"Tarefa adicionada ao módulo '{modulo.titulo}'.")
        else:
            print("Tipo de conteúdo não suportado.")

        print(f"Conteúdo inserido no módulo '{modulo.titulo}' do curso '{curso.titulo}'.")

        
    def adicionar_conteudo_modulo(self, modulo, tipo,caminho_video, conteudo=None):
        tipo = tipo.lower()   

        if tipo.lower() == "video":
            nome_video = input("Digite o nome do vídeo: ")
            video = Video(nome=nome_video, url=caminho_video)
            modulo.adicionar_video(video)
            return True

        elif tipo == "quiz":
            quiz = {"pergunta": conteudo, "respostas": []}
            for i in range(1, 5):
                resposta = input(f"Informe a opção {i} para a pergunta: ")
                quiz["respostas"].append(resposta)
            modulo.quizzes.append(quiz)
            return True
        elif tipo == "tarefa":
            tarefa = input("Digite a descrição da tarefa: ")
            modulo.tarefas.append(tarefa)
            return True
        else:
            return False

    def visualizar_conteudo_modulo(self, plataforma):
        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")

        try:
            curso_numero = int(input("Escolha o número do curso para visualizar conteúdo do módulo: "))
            curso = self.cursos_criados[curso_numero - 1]

            print("Módulos disponíveis:")
            for i, modulo in enumerate(curso.modulos, start=1):
                print(f"{i}. {modulo.titulo}")

            modulo_numero = int(input("Escolha o número do módulo para visualizar conteúdo: "))
            modulo = curso.modulos[modulo_numero - 1]

            # Exibir informações do módulo
            print(f"\nConteúdo do módulo '{modulo.titulo}': {modulo.conteudo}")

            if modulo.videos:
                print("\nVídeos do módulo:")
                for i, video in enumerate(modulo.videos, start=1):
                    print(f"{i}. {video}")

            if modulo.quizzes:
                print("\nQuizzes do módulo:")
                for i, quiz in enumerate(modulo.quizzes, start=1):
                    print(f"{i}. Pergunta: {quiz['pergunta']}")

            if modulo.tarefas:
                print("\nTarefas do módulo:")
                for i, tarefa in enumerate(modulo.tarefas, start=1):
                    print(f"{i}. Descrição: {tarefa['descricao']}, Prazo: {tarefa['prazo']}")

        except (ValueError, IndexError):
            print("Opção inválida ou curso não encontrado.")

class Estudante(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha)
        self.cursos_inscritos = []
        self.videos_assistidos = []
        self.progresso = 0

    def matricular_se_curso(self, plataforma):
        if not plataforma.usuarios:
            print("Não há instrutores cadastrados para criar cursos.")
            return

        cursos_disponiveis = []
        for usuario in plataforma.usuarios:
            if isinstance(usuario, Instrutor) and usuario.cursos_criados:
                cursos_disponiveis.extend(usuario.cursos_criados)

        if not cursos_disponiveis:
            print("Não há cursos disponíveis para matrícula.")
            return

        while True:
            print("\nCursos Disponíveis:")
            for i, curso in enumerate(cursos_disponiveis, start=1):
                print(f"{i}. {curso.titulo}")

            escolha = input("Escolha o número do curso para se matricular (ou 0 para voltar para Menu): ")

            if escolha == "0":
                break

            try:
                curso_escolhido = cursos_disponiveis[int(escolha) - 1]

                if curso_escolhido not in self.cursos_inscritos:
                    self.cursos_inscritos.append(curso_escolhido)
                    curso_escolhido.estudantes_matriculados.append(self)
                    print(f"Matrícula no curso '{curso_escolhido.titulo}' realizada com sucesso.")
                else:
                    print("Você já está matriculado neste curso.")
            except (ValueError, IndexError):
                print("Opção inválida.")

    def avancar_progresso(self):
        self.progresso += 1

    def mostrar_cursos_inscritos(self):
        if not self.cursos_inscritos:
            print("Você ainda não está matriculado em nenhum curso.")
            return

        print("Cursos Inscritos:")
        for i, curso in enumerate(self.cursos_inscritos, start=1):
            print(f"{i}. {curso.titulo}")

    def visualizar_conteudo_curso(self):
        if not self.cursos_inscritos:
            print("Você ainda não está matriculado em nenhum curso.")
            return

        print("Cursos Inscritos:")
        for i, curso in enumerate(self.cursos_inscritos, start=1):
            print(f"{i}. {curso.titulo}")

        escolha_curso = input("Escolha o número do curso para acessar o conteúdo (ou 0 para voltar para Menu): ")

        if escolha_curso == "0":
            return

        try:
            curso_escolhido = self.cursos_inscritos[int(escolha_curso) - 1]
            curso_escolhido.mostrar_conteudo_estudante(self)
        except (ValueError, IndexError):
            print("Opção inválida ou curso não encontrado.")

    def mostrar_progresso_cursos(self):
        if not self.cursos_inscritos:
            print("Você ainda não está matriculado em nenhum curso.")
            return

        print("Cursos Inscritos:")
        for i, curso in enumerate(self.cursos_inscritos, start=1):
            print(f"{i}. {curso.titulo}")

        escolha_curso = input("Escolha o número do curso para ver o progresso (): ")

        if escolha_curso == "0":
            return

        try:
            curso_escolhido = self.cursos_inscritos[int(escolha_curso) - 1]
            curso_escolhido.mostrar_progresso_estudante(self)
        except (ValueError, IndexError):
            print("Opção inválida ou curso não encontrado.")

    def assistir_video(self, video):
        print(f"Assistindo ao vídeo: {video}")
        if video not in self.videos_assistidos:
            self.videos_assistidos.append(video)
        else:
            print("\nEste vídeo já foi assistido.")

    def concluiu_quiz(self, quiz):
        print(f"Quiz: {quiz['pergunta']}")
        print("Opções:")
        
        for i, opcao in enumerate(quiz['opcoes'], start=1):
            print(f"{i}. {opcao}")

        resposta_usuario = input("Escolha a opção correta: ").strip().lower()

        return resposta_usuario == quiz['resposta_correta'][0].lower().strip()
        

    def concluiu_tarefa(self, modulo, tarefa):
        
        print("Tarefas do Módulo:")
        for i, tarefa in enumerate(modulo.tarefas, start=1):
            print(f"{i}. {tarefa['descricao']} - Prazo: {tarefa['prazo']}")

        entregou_todas = input("Você entregou todas as tarefas? (s/n): ").lower()
        return entregou_todas == 's'
        
class PlataformaElearning:
    def __init__(self):
        self.usuarios = []
        self.usuario_autenticado = None
        self.cursos_criados = []

    def carregar_usuarios(self):
        try:
            with open('usuarios.json', 'r') as file:
                data = json.load(file)
                for usuario_data in data['usuarios']:
                    if usuario_data['tipo'].lower() == 'instrutor':
                        usuario = Instrutor(usuario_data['nome'], usuario_data['senha'])
                    elif usuario_data['tipo'].lower() == 'estudante':
                        usuario = Estudante(usuario_data['nome'], usuario_data['senha'])
                        usuario.cursos_inscritos = usuario_data.get('cursos_inscritos', [])
                    else:
                        raise ValueError("Tipo de usuário inválido.")
                    self.usuarios.append(usuario)
        except FileNotFoundError:
        
            pass

    def salvar_usuarios(self):
        with open('usuarios.json', 'w') as file:
            data = {'usuarios': []}
            for usuario in self.usuarios:
                usuario_data = {'nome': usuario.nome, 'senha': usuario.senha, 'tipo': type(usuario).__name__}
                if isinstance(usuario, Estudante):
                    usuario_data['cursos_inscritos'] = usuario.cursos_inscritos
                data['usuarios'].append(usuario_data)
            json.dump(data, file)


    def mostrar_detalhes_curso(self, curso):
        print("\n+++ Detalhes do Curso +++")
        print(f"Título: {curso.titulo}")
        print(f"Descrição: {curso.descricao}")
        print("Módulos:")
        for module in curso.modulos:
            print(f"  - {module.titulo}: {module.conteudo}")
    

    def cadastrar_usuario(self, nome, senha, tipo):
        if any(usuario.nome == nome for usuario in self.usuarios):
            print("Usuário já cadastrado. Escolha outro nome.")
            return False

        if tipo.lower() == 'instrutor':
            usuario = Instrutor(nome, senha)
        elif tipo.lower() == 'estudante':
            usuario = Estudante(nome, senha)
        else:
            print("Tipo de usuário inválido.")
            return False

        self.usuarios.append(usuario)
        self.salvar_usuarios()
        print(f"Usuário {nome} cadastrado com sucesso.")
        return True

    def autenticar_usuario(self, nome, senha):
        for usuario in self.usuarios:
            if usuario.nome == nome and usuario.senha == senha:
                self.usuario_autenticado = usuario
                return True
        return False

    def mostrar_cursos_modulos_criados(self):
        if not self.cursos_criados:
            print("Você ainda não criou nenhum curso.")
            return

        print("Cursos criados:")
        for i, curso in enumerate(self.cursos_criados, start=1):
            print(f"{i}. {curso.titulo}")

    def menu_instrutor(self):
        print("\nMenu do Instrutor:")
        print("1. Criar Curso")
        print("2. Atualizar Informações do Curso")
        print("3. Adicionar Módulo")
        print("4. Remover Módulo")
        print("5. Atualizar Conteúdo do Módulo")
        print("6. Mostrar Cursos e Módulos Criados")
        print("7. Ver Estudantes Matriculados em um Curso")
        print("8. Inserir conteúdo em um módulo")
        print("9. Visualizar conteúdo do módulo")
        print("0. Sair")

    def menu_estudante(self):
        print("\nMenu do Estudante:")
        print("1. Matricular-se em um Curso")
        print("2. Mostrar Cursos Inscritos")
        print("3. Acessar Conteúdo de um Curso")
        print("0. Sair")


    def realizar_acoes(self,plataforma):
        while True:
            if isinstance(self.usuario_autenticado, Instrutor):
                self.menu_instrutor()
                escolha = input("Escolha uma opção (ou 0 para voltar para Menu): ")
                if escolha == "0":
                    break
                elif escolha == "1":
                    self.usuario_autenticado.criar_curso()
                elif escolha == "2":
                    self.usuario_autenticado.atualizar_informacoes_curso()
                elif escolha == "3":
                    self.usuario_autenticado.adicionar_modulo_curso()
                elif escolha == "4":
                    self.usuario_autenticado.remover_modulo_curso()
                elif escolha == "5":
                    self.usuario_autenticado.atualizar_conteudo_modulo()
                elif escolha == "6":
                    self.usuario_autenticado.mostrar_cursos_modulos_criados()
                elif escolha == "7":
                    self.usuario_autenticado.ver_estudantes_matriculados()
                elif escolha == "8":
                    self.usuario_autenticado.inserir_conteudo_modulo()
                elif escolha == "9":
                    self.usuario_autenticado.visualizar_conteudo_modulo(plataforma)
                else:
                    print("Opção inválida. Tente novamente.")

            elif isinstance(self.usuario_autenticado, Estudante):
                self.menu_estudante()
                escolha = input("Escolha uma opção (ou 0 para sair): ")
                if escolha == "0":
                    break
                elif escolha == "1":
                    self.usuario_autenticado.matricular_se_curso(plataforma)
                elif escolha == "2":
                    self.usuario_autenticado.mostrar_cursos_inscritos()
                elif escolha == "3":
                    self.usuario_autenticado.visualizar_conteudo_curso()
                else:
                    print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    plataforma = PlataformaElearning()
    plataforma.carregar_usuarios()
    

    while True:
        print("\nMenu Principal:")
        print("1. Cadastrar Usuário")
        print("2. Login")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break
        elif opcao == "1":
            nome = input("Digite o nome do usuário: ")
            senha = getpass.getpass("Digite a senha: ")
            tipo = input("Digite o tipo de usuário (Instrutor ou Estudante): ")

            plataforma.cadastrar_usuario(nome, senha, tipo)
        elif opcao == "2":
            nome = input("Digite o nome do usuário: ")
            senha = getpass.getpass("Digite a senha: ")

            if plataforma.autenticar_usuario(nome, senha):
                print(f"Bem-vindo, {plataforma.usuario_autenticado.nome}!")
                plataforma.realizar_acoes(plataforma)
            else:
                print("Falha na autenticação. Verifique seu nome de usuário e senha.")
        else:
            print("Opção inválida. Tente novamente.")
            
    plataforma.salvar_usuarios()
    
