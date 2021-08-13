lista = [""]
ativador = 0
val = 1 # True
if lista == [""]:
    print("A lista atual está vazia")

while True:
    if len(lista) >= 2:
        ativador = 1 # 1 True
    if len(lista) <= 1:
        ativador = 0 #0 False
    if not ativador:
        print("Digite: \n \"a\"-Para Adicionar um item na lista \n \"b\"-Para Deletar o primeiro da lista:\"", lista[0],
              "\"\n \"d\"-Para Deletar a lista \n \"e\"-Para Deletar o ultimo da lista:\"", lista[-1], " \" ")

        x = input()
        if "" in lista:
            while "" in lista:
                del lista[0]

        if x in lista:
            val = True
            t = 0
            print("Apagou da lista:", x)
            while x in lista:
                z =len(lista) - 1 - t
                if x in lista[z]:
                    del lista[z]
                if lista == []:
                    lista = [""]
                if x not in lista[z]:
                    t = t + 1


        if x == "b":
            print("O item ", lista[0], "foi eliminado da lista")
            del lista[0]
            if not lista:
                lista = [""]
        if x == "a":
            y = input("Digite o item a adicionar na lista:")
            if y in lista:
                print("Este item ja existe na lista, \"s\" para inserir mesmo assim ou qualquer outra tecla para NAO")
                x0 = input()
                if x0 == "s":
                    lista.append(y)
                if x0 != "s":
                    print("Acao cancelada")
            if y not in lista:
                lista.append(y)
        if x == "d":
            del lista
            print("A lista foi deletada")
            lista = [""]
        if x == "e":
            if len(lista) == 1:
                x = "d"
            if len(lista) >= 1:
                del lista[-1]
            if lista == []:
                lista = [""]
        if x != "a" and x !="b" and x !="d" and x !="e" and val != 1:
            print("Error, Opcao nao existente!  Voltando para o Menu...")
        if lista != [""]:
            print("A lista atual é:", lista)
        else:
            print("A lista atual está vazia")

    if ativador:
        print("Digite: \n \"a\"-Para Adicionar um item na lista \n \"b\"-Para Deletar o primeiro da lista:\"", lista[0],
              "\"\n \"c\"-Para Deletar o segundo item da lista:\"", lista[1],
              "\"\n \"d\"-Para Deletar a lista \n \"e\"-Para Deletar o ultimo da lista:\" ", lista[-1], " \" ")
        print("  Voce pode digitar o item da lista para apaga-lo")
        x = input()
        if "" in lista:
            while "" in lista:
                del lista[0]
        if x in lista:
            t = 0
            print("Apagou da lista:",x)
            while x in lista:
                val = 0
                z =len(lista) - 1 - t
                if x not in lista[z]:
                    t = t + 1
                if x in lista[z]:
                    del lista[z]
                if lista == []:
                    lista = [""]


        if x == "b":
            print("O item ", lista[0], "foi eliminado da lista")
            del lista[0]
            if lista == []:
                lista = [""]

        if x == "a":
            y = input("Digite o item a adicionar na lista:")
            if y in lista:
                print("Este item ja existe na lista, \"s\" para inserir mesmo assim, e qualquer outra tecla para NAO")
                x0 = input()
                if x0 == "s":
                    lista.append(y)
                if x0 != "s":
                    print("Acao cancelada")
            if y not in lista:
                lista.append(y)

        if x == "c":
            print("Foi deletado o item:\"", lista[1], "\" da lista")
            del lista[1]

        if x == "d":
            del lista
            print("A lista foi deletada")
            lista = [""]
        if x == "e":
            del lista[-1]
            if not lista:
                lista = [""]
        if not lista:
            lista = [""]

        if x != "a" and x !="b" and x != "c"and x !="d" and x !="e" and val == True:
            print("Error, Opcao nao existente!  Voltando para o Menu...")
        if lista != [""]:
            print("A lista atual é",lista)
        else:
            print("A lista atual está vazia")
