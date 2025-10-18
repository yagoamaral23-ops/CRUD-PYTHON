import mysql.connector
import json
import os

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="102030",
        database="crud_cli"
    )
    cursor = conn.cursor()
    print("Conexão com o banco realizada com sucesso!")
except mysql.connector.Error as err:
    print(f"Erro ao conectar: {err}")
    exit()


def menuINTERATIVO():
    print("1-ADICIONAR DADOS \n2-LISTAR DADOS \n3-DELETAR DADOS \n4-ATUALIZAR\n0-SAIR")
    while True:
        try:
            menu=int(input(""))
            if menu>5 or menu<0:
                print("DIGITE APENAS NUMEROS DE 0 A 5")
            else:
                break
        except ValueError:
            print("DIGITE APENAS NUMEROS DE 0 A 5")
    return menu
def pedirINT(enunciado):
    while True:
        try:
            idade=int(input(enunciado))
            if idade >100 or idade<0:
                print("IDADE ENTRE 0 E 100 POR FAVOR")
            else:
                break
        except ValueError:
            print("digite apenas numeros")
    return idade
def pedirSTR(enunciado):
    textoSTR=input(enunciado)
    return textoSTR
def inserir(nome,idade,email):
    sql="INSERT INTO tabtreino (nome, idade, email) VALUES (%s, %s, %s)"
    cursor.execute(sql,(nome,idade,email))
    if cursor.rowcount>0:
        print(f"{cursor.rowcount} REGISTRO(S) FORAM ALTERADOS")
    conn.commit()
def listar():
    cursor.execute("SELECT id, nome, idade, email FROM tabtreino")
    listar=cursor.fetchall()
    if listar:
        print(f"{listar}\n")
    else:
        print("A LISTA ESTA VAZIA")
def deletar():
    while True:
        try:
            QUAL_DELETAR=int(input("ID A SER DELETADO"))
            if QUAL_DELETAR<0:
                print("O PROGRAMA NAO ACEITA NUMEROS NEGATIVOS")
            else:
                break
        except ValueError:
            print("APENAS NUMEROS, SÓ ACEITAMOS NUMEROS DE ID")

    sql1="SELECT * FROM tabtreino WHERE id =%s"
    cursor.execute(sql1,(QUAL_DELETAR,))
    EXISTENCIA_EXCLUSAO=cursor.fetchall()

    if not EXISTENCIA_EXCLUSAO :
        print("ESSE ID NAO EXISTE NO BANCO DE DADOS")
    else:
        while True:
            try:
                confirmacao=int(input(f"DESEJA REALMENTE DELETAR O ID {QUAL_DELETAR} (1-SIM/2-NAO)"))
                if confirmacao==1:
                    sql="DELETE FROM tabtreino WHERE id = %s"
                    cursor.execute(sql,(QUAL_DELETAR,))
                    if cursor.rowcount>0:
                        print(f"{cursor.rowcount} REGISTRO(S) FORAM ALTERADOS")
                    conn.commit()
                    break
                else:
                    print("ESTE ID NAO FOI DELETADO")
                    break
            except:
                print("APENAS 1 OU 2")
def atualizar():
    try:
        QUAL_ATUALIZAR=int(input("DIGITE O ID QUE VOCE DESEJA ATUALIZAR"))
    except ValueError:
        print("DIGITE APENAS NUMEROS")
        return
    sql1=("SELECT * FROM tabtreino WHERE id=%s")
    cursor.execute(sql1,(QUAL_ATUALIZAR,))
    listar=cursor.fetchall()
    if listar:
        nome=pedirSTR("nome")
        idade=pedirINT("idade")
        email=pedirSTR("email")
        sql=("UPDATE tabtreino SET nome=%s, idade=%s, email=%s where id=%s")
        cursor.execute(sql,(nome,idade,email,QUAL_ATUALIZAR))
        
        if cursor.rowcount>0:
            print(f"{cursor.rowcount} REGISTRO(S) FORAM ALTERADOS \n \n \n")

        conn.commit()
        cursor.execute(sql1,(QUAL_ATUALIZAR,))
        listar=cursor.fetchone()
        print(listar)
    else:
        print("ESSE ID NAO EXISTE NO BANCO DE DADOS")
def pesquisar():
    resultado=[]
    pesquisa=input("DIGITE ALGO REFERENTE A SUA PESQUISA").strip()
    pesquisa=(f"%{pesquisa}%")

    sql="""
    SELECT id, nome, idade, email 
    FROM tabtreino 
    WHERE CAST(id AS CHAR) LIKE %s
        OR nome LIKE %s 
        OR CAST(IDADE AS CHAR) LIKE %s 
        OR email LIKE %s
    """
    
    cursor.execute(sql,(pesquisa,pesquisa,pesquisa,pesquisa))
    resultado=cursor.fetchall()  
    print(resultado)
    
while True:
    iniciar=menuINTERATIVO()
    if iniciar==1:
        nome=pedirSTR("DIGITE O NOME DO USUARIO")
        idade=pedirINT("DIGITE A IDADE DO USUARIO")
        email=pedirSTR("DIGITE O E-MAIL DO USUARIO")
        inserir(nome,idade,email)
    elif iniciar==2:
        listar()
    elif iniciar==3:
        deletar()
    elif iniciar==4:
        atualizar()
    elif iniciar==5:
        pesquisar()
    elif iniciar==0:
        cursor.close()
        conn.close()
        break
    else:
        print("ALGO INESPERADO DEU ERRADO")

