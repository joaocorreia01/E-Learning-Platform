class Curso:
    def __init__(self, titulo, descricao, instrutor, modulos=[]):
        self.titulo = titulo
        self.descricao = descricao
        self.instrutor = instrutor
        self.modulos = modulos

    def adicionar_modulo(self, modulo):
        self.modulos.append(modulo)

    def atualizar_descricao(self, nova_descricao):
        self.descricao = nova_descricao


titulo_curso = input("Digite o título do curso: ")
descricao_curso = input("Digite a descrição do curso: ")
instrutor_curso = input("Digite o nome do instrutor do curso: ")

curso_usuario = Curso(titulo=titulo_curso, descricao=descricao_curso, instrutor=instrutor_curso)

num_modulos = int(input("Quantos módulos você deseja adicionar? "))
for i in range(num_modulos):
    modulo = input(f"Digite o nome do módulo {i + 1}: ")
    curso_usuario.adicionar_modulo(modulo)

print(f"\nInformações do Curso:")
print(f"Título: {curso_usuario.titulo}")
print(f"Descrição: {curso_usuario.descricao}")
print(f"Instrutor: {curso_usuario.instrutor}")
print("Módulos:")
for modulo in curso_usuario.modulos:
    print(f" - {modulo}")
