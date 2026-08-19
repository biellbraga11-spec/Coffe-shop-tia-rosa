import json
import os

ARQUIVO_CARDAPIO = "cardapio.json"

# Cardápio
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


# Carregar arquivo JSON ao iniciar
cardapio = carregar_cardapio()


# Cadastro
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

    # Salva  JSON
    salvar_cardapio()
    print(f"Produto '{nome}' cadastrado no código {proximo_codigo} com {estoque_inicial} unidades!")


########################################################################################################
# EXIBIÇÃO CARDAPIO
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


###################################################################################################
# COMANDA
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

                # Verificação e baixa no estoque
                if item_escolhido['estoque'] > 0:
                    item_escolhido['estoque'] -= 1  # Subtrai 1 unidade do estoque
                    salvar_cardapio()  # Atualiza a alteração no arquivo JSON

                    dados_comanda['itens'].append(item_escolhido['nome'])
                    dados_comanda['preco'] += item_escolhido['preco']
                    print(f"-> {item_escolhido['nome'].title()} adicionado! (Restam: {item_escolhido['estoque']})")
                else:
                    print(f"PRODUTO ESGOTADO! Não há '{item_escolhido['nome']}' em estoque.")
            else:
                print("Código não encontrado! Tente novamente.")
        else:
            print("Por favor, digite apenas números válidos.")

    # RESUMO DA COMANDA
    print("\n" + "=" * 40)
    print(f"Resumo da comanda - {dados_comanda['cliente'].upper()}")
    print("=" * 40)
    print(f"Itens do pedido: {', '.join(dados_comanda['itens'])}")
    print(f"Total a pagar: R$ {dados_comanda['preco']:.2f}")

    # SISTEMA DE PAGAMENTO
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

        print("\n" + "=" * 40)
        print("COMPROVANTE FINAL")
        print(f"Cliente: {dados_comanda['cliente'].title()}")
        print(f"Pagamento: {dados_comanda['pagamento']}")
        print(f"Total Pago: R$ {dados_comanda['preco']:.2f}")
        print("Obrigado e volte sempre!")

    return dados_comanda


###################################################################################################
# MENU DO SISTEMA
def menu_principal():
    while True:
        print("\n" + "=" * 40)
        print("Sistema COFFEE SHOP TIA ROSA ")
        print("=" * 40)
        print("1 para ver cardapio")
        print("2 para cadastrar produto")
        print("3 para iniciar uma comanda")
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
            case "0":
                print("Saindo do sistema...")
                break
            case _:
                print("Opção inválida! Tente novamente.")


menu_principal()