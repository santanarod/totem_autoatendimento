from random import choice
from time import sleep

# REQUISITOS
# Objetivo: Programa de frente de caixa/totem de autoatendimento de um restaurante fast food.
# O cliente poderá escolher dentre os produtos disponíveis no cardápio.
# A forma de pagamento poderá ser cartão ou dinheiro. O cartão poderá ser recusado de forma aleatória.
# Na forma de pagamento em dinheiro, a quantidade de cada cédula fornecida deverá ser informada, gerando troco ou a insuficiência de pagamento, conforme o caso.
# O sistema é capaz de registrar os valores venda a venda e apresentar, ao final, o valor total do faturamento (cartão +  dinheiro) em reais.
# O estoque inicial é baixado a cada venda realizada. Os itens são descontados apenas após a confirmação de pagamento.
# O software poderá ser finalizado/desligado.
# O sistema apresenta o relatório de controle de estoque e caixa.

# OBS.: As linhas 192 e 91 foram comentadas para que o pytest rode os testes no terminal através do comando pytest Pedido.py
# Para executar o programa com a inserção dos inputs, descomentar as linhas citadas e utilizar o comando pytest Pedido.py -s

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
            "hambúrguer": 1,
            "cheddar": 30,
            "cebola": 10,
            "picles": 10,
            "ketchup": 10,
            "mostarda": 10,
            "pão com gergelim": 1,
        },
        "valor": 21.50,
    }
}

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
    "pão com gergelim": 0,
}

metodos_pagamento = ["credito", "debito", "dinheiro"]
cedulas_dinheiro = [2, 5, 10, 20]
valor_pedido = 0
faturamento = 0


print("====== 🍔 BEM VINDO AO FAST-FOOD DO BRASIL 🍔======")
def iniciar_programa():
    menu_escolha = input("Qual será o seu pedido? (big mac/quarterao/cheeseburger): ")
    efetuar_pedido(menu_escolha)


def efetuar_pedido(n):
    if n == "fechamento":
        exibir_relatorio()
        return "Relatório"
    elif n == "off":
        return "Programa encerrado"
    elif MENU.get(n) is None:
        print("Opção inválida. Por favor, escolha uma opção válida")
        # iniciar_programa()
        return "Produto não disponível no cardápio. Por favor, escolha um produto válido"
    else:
        pedido_andamento = MENU[n]
        if verificar_estoque(pedido_andamento["ingredientes"]):
            global valor_pedido
            valor_pedido = pedido_andamento['valor']

            metodo = input("Informe o método de pagamento (credito/debito/dinheiro): ")
            if validar_pagamento(metodo) == True:
                baixar_estoque(pedido_andamento["ingredientes"])
        return iniciar_programa()


def validar_pagamento(n):
    if n in metodos_pagamento:
        if n == "credito" or n == "debito":
            return processar_cartao(choice([True, False]))

        else:
            total = 0
            for valor in cedulas_dinheiro:
                valida_qntde = False
                while valida_qntde == False:
                    qntde = input(f"Quantas notas de R${valor}?: ")
                    valida_qntde = inserir_cedula(qntde)
                total += (int(qntde) * valor)
            return processar_dinheiro(total)

    else:
        print("Esta não é uma opção válida de pagamento.")
        return False


def inserir_cedula(qntde):
    try:
        entrada = int(qntde)
        if entrada < 0:
            return False
        return True
    except ValueError:
        return False


def processar_cartao(autorizacao):
    print("Processando pagamento...")
    sleep(1)
    if autorizacao:
        print("✅ Operacao realizada com sucesso!")
        global faturamento
        faturamento += valor_pedido
        return True
    else:
        print("‼️ Operação não autorizada pela Administradora do Cartão")
        return False


def processar_dinheiro(valor_recebido):
    global valor_pedido
    if valor_recebido >= valor_pedido:
        troco = round(valor_recebido - valor_pedido, 2)
        print(f"Aqui está o seu troco de R${troco}.")
        global faturamento
        faturamento += valor_pedido
        return True
    else:
        print("Desculpe, não há dinheiro suficiente. Dinheiro devolvido")
        return False


def verificar_estoque(ingredientes):
    for item in ingredientes:
        if ingredientes[item] >= recursos[item]:
            print(f"Desculpe, o item {item} está em falta no estoque.")
            return False
    return True


def baixar_estoque(ingredientes):
    for item in ingredientes:
        recursos[item] = recursos[item] - ingredientes[item]


def exibir_relatorio():
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
    print(f"Pão: {recursos['pão']}un")
    print(f"Pão: {recursos['pão com gergelim']}un\n")

    print("📈 FATURAMENTO")
    print(f"Dinheiro/Cartão R${faturamento}\n")


# iniciar_programa()


def test_deve_falhar_quando_cliente_escolher_produto_nao_identificado():
    assert efetuar_pedido("hkjhkjh") == "Produto não disponível no cardápio. Por favor, escolha um produto válido"

def test_deve_falhar_quando_forma_pagamento_invalida():
    assert validar_pagamento("nubank") == False

def test_deve_retornar_false_quando_cartao_nao_autorizado():
    assert processar_cartao(False) == False

def test_deve_retornar_true_quando_cartao_autorizado():
    assert processar_cartao(True) == True

def test_deve_falhar_quando_quantidade_cedula_menor_do_que_zero():
    assert inserir_cedula(-10) == False

def test_deve_retornar_programa_encerrado_quando_comando_off():
    assert efetuar_pedido("off") == "Programa encerrado"

def test_deve_retornar_relatorio_quando_comando_fechamento():
    assert efetuar_pedido("fechamento") == "Relatório"

def test_deve_falhar_quando_quantidade_cedula_igual_string():
    assert inserir_cedula("dez") == False

def test_deve_falhar_quando_pagamento_dinheiro_insuficiente():
    assert processar_dinheiro(-20) == False

def test_deve_falhar_quando_estoque_insuficiente():
    sanduiche = MENU["cheeseburger"]
    assert verificar_estoque(sanduiche["ingredientes"]) == False