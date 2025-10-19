import mysql.connector
import json
import os
from datetime import datetime

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

ARQUIVO = "lista_auditoria.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        lista_auditoria = json.load(f)
else:
    lista_auditoria = []
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista_auditoria, f, indent=2, ensure_ascii=False)

def menuINTERATIVO():
    print("1-ADICIONAR DADOS \n2-LISTAR DADOS \n3-DELETAR DADOS \n4-ATUALIZAR\n5-PESQUISAR\n6-AUDITORIA\n7-LIXEIRA\n0-SAIR")
    while True:
        try:
            menu=int(input(""))
            if menu>7 or menu<0:
                print("DIGITE APENAS NUMEROS DE 0 A 7")
            else:
                break
        except ValueError:
            print("DIGITE APENAS NUMEROS DE 0 A 7")
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
    global id_auditoria, comando_auditoria, funcao_auditoria, horario_auditoria
    sql="INSERT INTO tabtreino (nome, idade, email) VALUES (%s, %s, %s)"
    cursor.execute(sql,(nome,idade,email))
    if cursor.rowcount>0:
        print(f"{cursor.rowcount} REGISTRO(S) FORAM ALTERADOS")
    conn.commit()

    id_auditoria=contadorID()
    comando_auditoria =(f"NOME:{nome:<20}IDADE:{idade:<5}EMAIL:{email}")
    funcao_auditoria = "DADOS ADICIONADOS"
    horario_auditoria = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    auditoria(id_auditoria,comando_auditoria,funcao_auditoria,horario_auditoria,nome,idade,email)
def listar():
    cursor.execute("SELECT id, nome, idade, email FROM tabtreino")
    listar=cursor.fetchall()
    if listar:
        for id,nome,idade,email in listar:
            print(f"ID:{id:<4}NOME:{nome:<20}IDADE:{idade:<5}EMAIL:{email}")
            print("____________________________________________________________________________________________________________") 
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
        for id,x,y,z in EXISTENCIA_EXCLUSAO:
            nome=x
            idade=y
            email=z
        while True:
            try:
                confirmacao=int(input(f"DESEJA REALMENTE DELETAR O ID {QUAL_DELETAR} (1-SIM/2-NAO)"))
                if confirmacao==1:
                    sql="DELETE FROM tabtreino WHERE id = %s"
                    cursor.execute(sql,(QUAL_DELETAR,))
                    conn.commit()

                    id_auditoria=contadorID()
                    comando_auditoria =(f"NOME:{nome:<20}IDADE:{idade:<5}EMAIL:{email}")
                    funcao_auditoria = "DADOS DELETADOS"
                    horario_auditoria = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    auditoria(id_auditoria,comando_auditoria,funcao_auditoria,horario_auditoria,nome,idade,email)

                    if cursor.rowcount>0:
                        print(f"{cursor.rowcount} REGISTRO(S) FORAM ALTERADOS")
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
        id_auditoria=contadorID()
        comando_auditoria =(f"NOME:{nome:<20}IDADE:{idade:<5}EMAIL:{email}")
        funcao_auditoria = "DADOS ATUALIZADOS"
        horario_auditoria = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        auditoria(id_auditoria,comando_auditoria,funcao_auditoria,horario_auditoria)

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
def auditoria(id_auditoria,comando_auditoria,funcao_auditoria,horario_auditoria,nome_auditoria,idade_auditoria,email_auditoria):
    lista_dicionario={
        "ID":id_auditoria,
        "COMANDO":comando_auditoria,
        "FUNCAO":funcao_auditoria,
        "HORARIO":horario_auditoria,
        "NOME":nome_auditoria,
        "IDADE":idade_auditoria,
        "EMAIL":email_auditoria
    }
    lista_auditoria.append(lista_dicionario)

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista_auditoria, f, indent=2, ensure_ascii=False)
def listar_auditoria():
    for a in lista_auditoria:
        print(f"{a["ID"]}")
        print(f"{a["COMANDO"]}")
        print(f"{a["FUNCAO"]}")
        print(f"{a["HORARIO"]}")
        print("____________________________________________________________________________________________________________")                       
def contadorID():
    contador_id=1
    for a in lista_auditoria:
        contador_id=int(a["ID"])
        contador_id+=1
    return contador_id
def lixeira():
    for x in lista_auditoria:
    
        if (f"{x["FUNCAO"]}") == "DADOS DELETADOS" :
            print(f"{x["ID"]}")
            print(f"{x["COMANDO"]}")
            print(f"{x["FUNCAO"]}")
            print(f"{x["HORARIO"]}")
            print("____________________________________________________________________________________________________________")
    while True:
        try: 
            confirmacao_restaurar=int(input("DESEJA RESTAURAR ALGUM DADO EXCLUIDO ? 1-SIM/2-NAO"))
            if confirmacao_restaurar == 1 or confirmacao_restaurar ==2:
                break
            else:
                print("DIGITE APENAS 1 PARA SIM E 2 PARA NAO")
        except ValueError:
            print("DIGITE APENAS 1 PARA SIM E 2 PARA NAO")
    while True:
        try:
            id_restaurar=int(input("RESTAURE POR ID, DIGITE APENAS NUMEROS"))
            for x in lista_auditoria:
                if id_restaurar==int(f"{x['ID']}"):
                    while True:
                        try:
                            confirmacao_final=int(input(f"DESEJA RESTAURAR ? 1-SIM/2-NAO \n{x['COMANDO']}"))
                            if confirmacao_final==1:
                                sql=("INSERT INTO tabtreino (nome,idade,email) VALUES (%s,%s,%s)")
                                cursor.execute(sql,(x["NOME"],x["IDADE"],x["EMAIL"]))
                                conn.commit()
                                break
                            if confirmacao_final==2:
                                print("NADA FOI ALTERADO")
                                break
                            else:
                                break
                        except ValueError:
                            print("APENAS 1 OU 2 PARA INTERAGIR")

                else:
                    print("")
            break
        except ValueError:
            print("DIGITE APENAS NUMEROS")


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
    elif iniciar==6:
        listar_auditoria()
    elif iniciar==7:
        lixeira()
    elif iniciar==0:
        cursor.close()
        conn.close()
        break
    else:
        print("ALGO INESPERADO DEU ERRADO")

