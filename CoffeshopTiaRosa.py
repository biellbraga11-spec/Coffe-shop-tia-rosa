from datetime import datetime
import json
import os
import re

ARQUIVO_CARDAPIO = "cardapio.json"
ARQUIVO_VENDAS = "vendas.json"
ARQUIVO_CLIENTES = "clientes.json"


################################################## CARDAPIO #######################################################

CARDAPIO_PADRAO = {
    1: {"nome": "pao de queijo", "preco": 1.50, "estoque": 100},
    2: {"nome": "tapioca", "preco": 3.00, "estoque": 100},
    3: {"nome": "cafe", "preco": 3.50, "estoque": 100},
    4: {"nome": "pingado", "preco": 4.00, "estoque": 100},
    5: {"nome": "coxinha", "preco": 5.00, "estoque": 50},
    6: {"nome": "suco de laranja", "preco": 6.50, "estoque": 45},
    7: {"nome": "refrigerante", "preco": 7.00, "estoque": 70},
    8: {"nome": "enroladinho", "preco": 5.50, "estoque": 38},
    9: {"nome": "torta de frango", "preco": 8.00, "estoque": 15},
}


########################################### GERENCIAMENTO CARDAPIO ###################################################


def carregar_cardapio():
    if os.path.exists(ARQUIVO_CARDAPIO) and os.path.getsize(ARQUIVO_CARDAPIO) > 0:
        try:
            with open(ARQUIVO_CARDAPIO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return {int(k): v for k, v in dados.items()}
        except json.JSONDecodeError:
            return CARDAPIO_PADRAO
    return CARDAPIO_PADRAO


def salvar_cardapio():
    with open(ARQUIVO_CARDAPIO, "w", encoding="utf-8") as f:
        json.dump(cardapio, f, indent=4, ensure_ascii=False)


cardapio = carregar_cardapio()


######################################### FIDELIDADE E DESCONTO ####################################################
def carregar_clientes():
    if os.path.exists(ARQUIVO_CLIENTES) and os.path.getsize(ARQUIVO_CLIENTES) > 0:
        try:
            with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def salvar_clientes(clientes):
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)


def limpar_telefone(texto):
    return re.sub(r"\D", "", texto)


def consultar_fidelidade():
    clientes = carregar_clientes()
    print("\n" + "=" * 40)
    print("      PROGRAMA DE FIDELIDADE TIA ROSA")
    print("=" * 40)

    telefone_raw = input("Digite o telefone do cliente (apenas números): ")
    telefone = limpar_telefone(telefone_raw)

    if telefone in clientes:
        cliente = clientes[telefone]
        print(f"\nCliente: {cliente['nome']}")
        print(f"Saldo atual: {cliente['pontos']} pontos")

        if cliente['pontos'] >= 50:
            opcao = input(
                "\nDeseja resgatar 50 pontos por R$ 5,00 de desconto na próxima comanda? (S/N): ").strip().upper()
            if opcao == "S":
                cliente['pontos'] -= 50
                salvar_clientes(clientes)
                print("-> Resgate efetuado com sucesso! Aplique R$ 5,00 de desconto no caixa.")
        else:
            faltam = 50 - cliente['pontos']
            print(f"Faltam {faltam} pontos para alcançar o próximo desconto de R$ 5,00.")
    else:
        print("Cliente não encontrado no cadastro de fidelidade.")


############################################# RALATORIO DE VENDAS ################################################


def carregar_vendas():
    if os.path.exists(ARQUIVO_VENDAS) and os.path.getsize(ARQUIVO_VENDAS) > 0:
        try:
            with open(ARQUIVO_VENDAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def registrar_venda(comanda_finalizada):
    vendas = carregar_vendas()

    comanda_finalizada["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    comanda_finalizada["data"] = datetime.now().strftime("%d/%m/%Y")

    vendas.append(comanda_finalizada)

    with open(ARQUIVO_VENDAS, "w", encoding="utf-8") as f:
        json.dump(vendas, f, indent=4, ensure_ascii=False)


def relatorio_vendas():
    vendas = carregar_vendas()

    if not vendas:
        print("\nNenhuma venda registrada ainda.")
        return

    hoje = datetime.now().strftime("%d/%m/%Y")

    print("\n" + "=" * 50)
    print(f"       RELATÓRIO DE VENDAS DIÁRIAS ({hoje})")
    print("=" * 50)

    total_dia = 0.0
    vendas_hoje = 0
    totais_pagamento = {
        "Pix": 0.0,
        "Cartão (Crédito)": 0.0,
        "Cartão (Débito)": 0.0,
        "Dinheiro": 0.0
    }

    for v in vendas:
        if v.get("data") == hoje:
            vendas_hoje += 1
            valor = v["preco"]
            pagto = v["pagamento"]

            total_dia += valor
            if pagto in totais_pagamento:
                totais_pagamento[pagto] += valor

            print(f"[{v['data_hora']}] Cliente: {v['cliente']:<12} | Pagto: {pagto:<17} | Total: R$ {valor:.2f}")

    print("-" * 50)
    print(f"Total de comandas hoje: {vendas_hoje}")
    print("-" * 50)
    print("RESUMO POR FORMA DE PAGAMENTO:")
    for forma, total_forma in totais_pagamento.items():
        print(f"- {forma:<18}: R$ {total_forma:.2f}")
    print("-" * 50)
    print(f"FATURAMENTO TOTAL DO DIA: R$ {total_dia:.2f}")
    print("=" * 50)


#################################### FUNÇÕES DO SISTEMA  ###########################################################
def cadastrar_produto():
    print("\n--- Cadastrar item ---")
    proximo_codigo = max(cardapio.keys()) + 1 if cardapio else 1
    nome = input("Digite o nome do produto: ").strip()
    preco = float(input("Digite o preço do produto: R$ "))
    estoque_inicial = int(input("Digite a quantidade em estoque: "))

    cardapio[proximo_codigo] = {
        "nome": nome,
        "preco": preco,
        "estoque": estoque_inicial
    }
    salvar_cardapio()
    print(f"Produto '{nome}' cadastrado no código {proximo_codigo}!")


def exibir_cardapio():
    print("\n" + "=" * 50)
    print("          COFFEE SHOP TIA ROSA ")
    print("=" * 50)
    print(f"{'Cod':<4} | {'Item':<18} | {'Preço':<8} | {'Estoque':<7}")
    print("-" * 50)

    for codigo, produto in cardapio.items():
        nome = produto["nome"].title()
        preco = produto["preco"]
        qtd = produto["estoque"]
        print(f"{codigo:<4} | {nome:<18} | R$ {preco:<5.2f} | {qtd:<7}")


def comanda():
    print("\n" + "=" * 40)
    cliente = input("Digite o nome do cliente ou da mesa: ")

    dados_comanda = {
        'cliente': cliente,
        'itens': [],
        'preco': 0.0,
        'pagamento': None
    }

    print(f"Comanda aberta para: {cliente}")
    exibir_cardapio()

    while True:
        codigo = input("\nDigite o codigo do produto ou 0 para sair: ").strip()

        if codigo == "0":
            break

        if codigo.isdigit():
            codigo_num = int(codigo)

            if codigo_num in cardapio:
                item_escolhido = cardapio[codigo_num]

                if item_escolhido['estoque'] > 0:
                    item_escolhido['estoque'] -= 1
                    salvar_cardapio()

                    dados_comanda['itens'].append(item_escolhido['nome'])
                    dados_comanda['preco'] += item_escolhido['preco']
                    print(f"-> {item_escolhido['nome'].title()} adicionado! (Restam: {item_escolhido['estoque']})")
                else:
                    print(f"PRODUTO ESGOTADO! Não há '{item_escolhido['nome']}' em estoque.")
            else:
                print("Código não encontrado! Tente novamente.")
        else:
            print("Por favor, digite apenas números válidos.")

    if not dados_comanda['itens']:
        print("Comanda cancelada ou vazia.")
        return

    print("\n" + "=" * 40)
    print(f"Resumo da comanda - {dados_comanda['cliente'].upper()}")
    print("=" * 40)
    print(f"Itens do pedido: {', '.join(dados_comanda['itens'])}")
    print(f"Total a pagar: R$ {dados_comanda['preco']:.2f}")

    if dados_comanda['preco'] > 0:
        print("\n" + "-" * 40)
        print("FORMA DE PAGAMENTO")
        print("1 - Pix")
        print("2 - Cartão (Crédito / Débito)")
        print("3 - Dinheiro (com troco)")
        print("-" * 40)

        while True:
            opcao_pag = input("Escolha a forma de pagamento (1, 2 ou 3): ").strip()

            if opcao_pag == "1":
                dados_comanda['pagamento'] = "Pix"
                print("\n[PIX] Chave Pix: 12.345.678/0001-99 (Tia Rosa)")
                input("Pressione ENTER após confirmar o recebimento...")
                print("-> Pagamento Pix confirmado!")
                break

            elif opcao_pag == "2":
                tipo = input("1 para Crédito | 2 para Débito: ").strip()
                modalidade = "Crédito" if tipo == "1" else "Débito"
                dados_comanda['pagamento'] = f"Cartão ({modalidade})"
                print(f"-> Pagamento APROVADO no cartão de {modalidade}!")
                break

            elif opcao_pag == "3":
                dados_comanda['pagamento'] = "Dinheiro"
                total = dados_comanda['preco']

                while True:
                    try:
                        valor_entregue = float(input(f"Total: R$ {total:.2f} | Valor recebido do cliente: R$ "))
                        if valor_entregue >= total:
                            troco = valor_entregue - total
                            print(f"-> Pagamento efetuado! Troco: R$ {troco:.2f}")
                            break
                        else:
                            faltam = total - valor_entregue
                            print(f"Valor insuficiente! Faltam R$ {faltam:.2f}")
                    except ValueError:
                        print("Por favor, digite um valor numérico válido.")
                break

            else:
                print("Opção inválida! Escolha 1, 2 ou 3.")

        # REGISTRA A VENDA NO ARQUIVO JSON
        registrar_venda(dados_comanda)

        # INTEGRAÇÃO FIDELIDADE
        clientes = carregar_clientes()
        telefone_raw = input("\nInforme o telefone do cliente para pontos de fidelidade (ou ENTER para ignorar): ")
        telefone = limpar_telefone(telefone_raw)

        if telefone:
            if telefone not in clientes:
                nome_fidelidade = input("Novo cliente no programa! Digite o nome: ").strip()
                clientes[telefone] = {"nome": nome_fidelidade, "pontos": 0}

            pontos_ganhos = int(dados_comanda['preco'])
            clientes[telefone]['pontos'] += pontos_ganhos
            salvar_clientes(clientes)
            print(
                f"-> {pontos_ganhos} pontos acumulados! Saldo atual de {clientes[telefone]['nome']}: {clientes[telefone]['pontos']} pts.")

        print("\n" + "=" * 40)
        print("COMPROVANTE FINAL")
        print(f"Cliente: {dados_comanda['cliente'].title()}")
        print(f"Pagamento: {dados_comanda['pagamento']}")
        print(f"Total Pago: R$ {dados_comanda['preco']:.2f}")
        print("Obrigado e volte sempre!")


#################################################  MENU DO SISTEMA  ##################################################
def menu_principal():
    while True:
        print("\n" + "=" * 40)
        print("Sistema COFFEE SHOP TIA ROSA ")
        print("=" * 40)
        print("1 para ver cardapio")
        print("2 para cadastrar produto")
        print("3 para iniciar uma comanda")
        print("4 para ver relatório de vendas do dia")
        print("5 para consultar/resgatar pontos de fidelidade")
        print("0 para sair")
        print("=" * 40)
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                exibir_cardapio()
            case "2":
                cadastrar_produto()
            case "3":
                comanda()
            case "4":
                relatorio_vendas()
            case "5":
                consultar_fidelidade()
            case "0":
                print("Saindo do sistema...")
                break
            case _:
                print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()

#######################################################################################################################