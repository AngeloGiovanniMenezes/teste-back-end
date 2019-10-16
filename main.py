import sys
from collections import namedtuple
from operator import attrgetter

class Usuario():

    def __init__(self, email, permissoes):
        
        self.email = email
        self.permissoes = permissoes

    def getEmail(self):

        return str(self.email)

    def getPermissoes(self):
        
        return self.permissoes

def main():

    def abreArquivo():

         #le o arquivo e armazena o conteudo separado por linhas na lista "linhas_arquivo"
        with open("code-test Back-End.txt") as arquivo:
            linhas = arquivo.readlines()
        
        return linhas

    def leArquivo(linhas_arquivo, dicionario_permissoes, lista_usuarios):

        #percorre a lista que contem as linhas do arquivo
        for i in range(0, len(linhas_arquivo)):
            #quebra a linha atual nos ; e salva o conteudo na lista auxiliar "temp"
            temp = linhas_arquivo[i].split(";")

            '''
                temp[0] = usuario ou grupo
                temp[1] = para usuario corresponde ao email, para grupo corresponde a funcao
                temp[2] = para usuario, lista de pares (tipo_grupo, id_condominio), para grupo corresponde ao id_condominio
                temp[3] = somente para grupo, corresponde as permissoes
            '''

            #testa se a linha atual corresponde a um usuario ou grupo
            if (temp[0] == "Grupo"):
                #no caso de grupo, cria o dicionario, sendo a funcao e o id do condominio a chave, e a permissao entra como valor
                dicionario_permissoes[temp[1] + temp[2]] = temp[3]
            else:
                lista_permissoes_usuario = formataPermissoes(temp)
                usuario = Usuario(temp[1], lista_permissoes_usuario)
                lista_usuarios.append(usuario)

    def formataPermissoes(temp):

        #formatacao das funcoes lidas do arquivo, para serem usadas como chave no dicionario de permissoes
        permissoes_usuario = temp[2].replace("[", "").rstrip()
        permissoes_usuario = permissoes_usuario.replace("]", "")
        permissoes_usuario = permissoes_usuario.replace("(", "")
        permissoes_usuario = permissoes_usuario.replace(",", "")
        permissoes_usuario = permissoes_usuario[:-1]

        lista_permissoes_usuario = permissoes_usuario.split(")")

        return lista_permissoes_usuario

    def pesquisaUsuario(usuario, lista_usuarios):

        for i in range(0, len(lista_usuarios)):
            if(lista_usuarios[i].getEmail() == usuario):
                return lista_usuarios[i]
    
    def geraStringSaida(permissoes):

        string_saida = str(permissoes[-1:]) + "; " + str(dicionario_permissoes.get(permissoes))
        print(string_saida)

    #variaveis
    lista_usuarios = []
    linhas_arquivo = []
    dicionario_permissoes = {}

    nivel_permissoes = {'Morador2': 6, 'Morador1': 5, 'Sindico1': 4, 'Porteiro2': 3, 'Porteiro1': 2, 'Sindico2': 1}

    linhas_arquivo = abreArquivo()
    leArquivo(linhas_arquivo, dicionario_permissoes, lista_usuarios)
    
    if (len(sys.argv) < 2):
        print("Por favor informe um email a ser pesquisado na execucao do script.")
        sys.exit(0)
    
    usuario = pesquisaUsuario(str(sys.argv[1]), lista_usuarios)
    if usuario is None:
        print("Usuario Invalido")
        sys.exit(0)
    
    permissoes = usuario.getPermissoes()
    if (len(permissoes) == 1):
        geraStringSaida(permissoes[0])
    else:
        permissoes = sorted(permissoes, key=lambda x: nivel_permissoes[x])
        for i in range(0, len(permissoes)):
            geraStringSaida(permissoes[i])
   
main()
