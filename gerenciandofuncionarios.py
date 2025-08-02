# Gerenciando Funcionarioa com Banco de dados SQLite

import sqlite3

# Conectar ao banco
conexao = sqlite3.connect("sistema.db")
cursor = conexao.cursor()



# Cria a tabela se ainda não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    cargo TEXT,
    senha TEXT NOT NULL
)
""")
conexao.commit()

def cadastrar_funcionario():
    nome = input("Nome: ")
    cpf = input("CPF (Somente números): ")
    cargo = input("Cargo: ")
    senha = input("Senha: ")

    try:
        cursor.execute("""
        INSERT INTO funcionarios (nome, cpf, cargo, senha)
        VALUES (?, ?, ?, ?)
        """, (nome, cpf, cargo, senha))
        conexao.commit()
        print("Funcionario cadastrado com sucesso!")
    except sqlite3.IntegrityError:
      print("CPF já cadastrado.\n")

def listar_funcionarios():
    cursor.execute("SELECT id, nome, cpf, cargo FROM funcionarios")
    funcionarios = cursor.fetchall()

    if funcionarios:
        for f in funcionarios:
            print(f"ID: {f[0]}, Nome: {f[1]}, CPF: {f[2]}, Cargo: {f[3]}")
    else:
        print("Nenhum funcionario cadastrado.\n")

def editar_funcionario():
    cpf = input("Digite o cpf do funcionario a ser editado:")

    cursor.execute("SELECT nome, cargo FROM funcionarios WHERE cpf = ?", (cpf,))
    funcionario = cursor.fetchone()

    if funcionario:
        print(f"Funcionario encontrado: {funcionario[0]} - Cargo atual: {funcionario[1]}")
        print("1 - Altera Cargo")
        print("2 - Altera senha")
        opcao = input("Escolha oque deseja altera: ")

        if opcao == "1":
                novo_cargo = input("Novo cargo: ")
                cursor.execute("UPDATE funcionarios SET cargo = ? WHERE cpf = ?",(novo_cargo, cpf))
                conexao.commit()
                print("Cargo atualizado comsucesso")

        elif opcao == "2":
            nova_senha = input("Nova senha: ")
            cursor.execute("UPDATE funcionarios SET senha = ? WHERE cpf = ?", (nova_senha, cpf))
            conexao.commit()
            print("Senha alterada com sucesso!\n")
        else:
            print("Opção invalida. Tente novamente.")
    else:
        print("Funcionario não encontrado.\n")


def remover_funcionario():
    cpf = input("Digite o CPF do funcionário a ser removido: ")

    cursor.execute("SELECT nome FROM funcionarios WHERE cpf = ?", (cpf,))
    funcionario = cursor.fetchone()

    if funcionario:
        comfirmação = input(f"Tem certeza que deseja remover {funcionario[0]}? (s/n): ")
        if comfirmação == "s": 
            cursor.execute("DELETE FROM funcionarios WHERE cpf = ?", (cpf,))
            conexao.commit()
            print("Funcionário removido com sucesso!\n")
        else:
            print("Remoção cancelada.\n")
    else:
        print("Funcionario não encontrado.\n")

def menu():
    while True:
     print("-" * 30)
     print("\n=== Menu de funcioanrios ===")
     print("1 - Cadastro de funcionários")
     print("2 - Lista de funcionários")
     print("3 - Editar funcionário")
     print("4 - Remover um funcionario")
     print("5 - sair")
     print("-" * 30)

     opcao = input("Opção: ")
  
     if opcao == "1":
         cadastrar_funcionario()
     elif opcao == "2":
         listar_funcionarios()
     elif opcao == "3":
         editar_funcionario()
     elif opcao == "4":
         remover_funcionario()
     elif opcao == "5":
         print("Sistema incerrado.")
         break
     else:
         print("Opção invalida. Tente Novamente.")

menu()
conexao.close()
