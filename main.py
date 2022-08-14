from random import choice, random
from time import sleep

MENU = {
    "big mac": {
        "ingredientes": {
            "hambúrguer": 2,
            "alface": 1,
            "cheddar": 20,
            "maionese": 30,
            "cebola": 10,
            "picles": 10,
            "pão": 1,

        },
        "valor": 22.90,
    },
    "quarterao": {
        "ingredientes": {
            "hambúrguer": 1,
            "cheddar": 30,
            "picles": 10,
            "cebola": 10,
            "ketchup": 10,
            "mostarda": 10,
            "pão": 1,

        },
        "valor": 31.44,
    },
    "cheeseburger": {
        "ingredientes": {
            "hamburguer": 1,
            "cheddar": 30,
            "cebola": 10,
            "picles": 10,
            "ketchup": 10,
            "mostarda": 10,
            "pão": 1,
        },
        "valor": 21.50,
    }
}

faturamento = 0

recursos = {
    # Considera-se o volume dos itens em gramas, exceto hamburger e pão
    "hambúrguer": 10,
    "alface": 100,
    "cheddar": 200,
    "maionese": 300,
    "cebola": 200,
    "picles": 100,
    "ketchup": 100,
    "mostarda": 100,
    "pão": 120,
}


def checar_estoque(pedido_ingredientes):
    # Retorna True quando a ordem pode ser feita, False se os ingredientes são insuficientes
    for item in pedido_ingredientes:
        if pedido_ingredientes[item] >= recursos[item]:
            print(f"Desculpe, o item {item} está em falta no estoque.")
            return False
    return True


def baixar_estoque(pedido_ingredientes):
    # Baixa os ingredientes no estoque conforme pedido efetivado
    for item in pedido_ingredientes:
        recursos[item] = recursos[item] - pedido_ingredientes[item]


def informar_pagamento():
    # Retorna o método de pagamento selecionado pelo cliente, podendo ser: crédito, débito ou dinheiro
    metodo_pagamento = ""
    while metodo_pagamento != "credito" and metodo_pagamento != "debito" and metodo_pagamento != "dinheiro":
        metodo_pagamento = input("Informe o método de pagamento (credito/debito/dinheiro): ")
    return metodo_pagamento


def processar_cartao(valor):
    # Retorna True se a operação for bem sucessida e False se a compra não foi autorizada (aleatório)
    escolha = input("Por favor, insira o cartão de crédito (confirmar/cancelar): ")
    autorizacao_cartao = False

    if escolha == "confirmar":
        print("Processando pagamento...")
        sleep(1)
        autorizacao_cartao = choice([False, True])

        if autorizacao_cartao == False:
            print("‼️ Operação não autorizada pela Administradora do Cartão")
        else:
            print("✅ Operacao realizada com sucesso!")
            global faturamento
            faturamento += valor

    return autorizacao_cartao


def processar_dinheiro():
    """Retorna o valor total calculado com base nas cédulas fornecidas"""
    print("Por favor, insira as cédulas")
    total = int(input("Quantas notas de R$2?: ")) * 2
    total += int(input("Quantas notas de R$5? ")) * 5
    total += int(input("Quantas notas de R$10? ")) * 10
    total += int(input("Quantas notas de R$20? ")) * 20
    return total


def checar_transacao(dinheiro_recebido, valor):
    """Retorna True quando o pagamento é aceito ou False se o dinheiro for insuficiente"""
    if dinheiro_recebido >= valor:
        troco = round(dinheiro_recebido - valor, 2)
        print(f"Aqui está o seu troco de R${troco}.")
        global faturamento
        faturamento += valor
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")
        return False


is_on = True

print("====== 🍔 BEM VINDO AO FAST-FOOD DO BRASIL 🍔======")
while is_on:
    escolha = input("Qual será o seu pedido? (big mac/quarterao/cheeseburger): ")
    if escolha == "off":
        is_on = False
    elif escolha == "fechamento":
        print("======Fechamento Caixa======")
        print("📦 ESTOQUE")
        print(f"Hambúrguer: {recursos['hambúrguer']}un")
        print(f"Alface: {recursos['alface']}gr")
        print(f"Cheddar: {recursos['cheddar']}gr")
        print(f"Maionese: {recursos['maionese']}gr")
        print(f"Cebola: {recursos['cebola']}gr")
        print(f"Picles: {recursos['picles']}gr")
        print(f"Ketchup: {recursos['ketchup']}gr")
        print(f"Mostarda: {recursos['mostarda']}gr")
        print(f"Pão: {recursos['pão']}un\n")

        print("📈 FATURAMENTO")
        print(f"Dinheiro/Cartão R${faturamento}\n")
    else:
        sanduiche = MENU[escolha]

        if checar_estoque(sanduiche["ingredientes"]):
            transacao_financeira = False

            while transacao_financeira == False:
                metodo = informar_pagamento()
                if metodo == "credito" or metodo == "debito":
                    transacao_financeira = processar_cartao(sanduiche["valor"])
                else:
                    pagamento = processar_dinheiro()
                    transacao_financeira = checar_transacao(pagamento, sanduiche["valor"])

            baixar_estoque(sanduiche["ingredientes"])

