from pydoc import plaintext

file = open('arquivo.txt','w')
file.write('olá como vc esta?\n')
file.write('bem e vc?')
file.close()
open('arquivo.txt', 'r', encoding='utf-8')
    conteudo = file.read()
    print(conteudo)