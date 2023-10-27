#!/usr/bin/env python3 
##
"""
Script criado para cortar bordas de imagens que tenham um círculo central com a foto do funcionário, o círculo pode não ser totalmente redondo e a imagem pode ser de vários tamanhos.
Será criada uma nova imagem quadrada mantendo o círculo no centro.
As primeiras imagens usadas para criação da assinatura em HTML já haviam sido editadas.


- criar, e entrar no embiente virtual Python
    python3 -m venv venv_cortarImagens
    source venv_cortarImagens/bin/activate

- instalar dependências
    pip3 install opencv-python-headless numpy

"""



import os
import cv2
import numpy as np

# Diretório onde as imagens originais estão localizadas # os.getcwd() => diretório atual do script
diretorio_imagens = os.path.join(os.getcwd(), 'fotos_originais')
print("=> Diretório das imagens originais:", diretorio_imagens)

# Diretório onde as imagens editadas serão salvas
diretorio_saida = os.path.join(os.getcwd(), 'fotos')
print("=> Diretório de saída:", diretorio_saida)


if not os.path.exists(diretorio_imagens): # Parar scriptse pasta com arquivos originais não existir
    print(f"Impossível continuar, diretório com as imagens originais não foi encontrado:	{diretorio_imagens} \n")
    exit(1)

if not os.path.exists(diretorio_saida): # Se diretório de saída não existe, crie-o
    os.makedirs(diretorio_saida)

# Lista de arquivos no diretório de imagens
arquivos = os.listdir(diretorio_imagens)
print("\nArquivos encontrados: \n\n", arquivos)

print("\n=> executando")
for arquivo in arquivos:

    posicao_ponto = arquivo.rfind('.')  # Encontrar a posição do último ponto no nome do arquivo
    if posicao_ponto != -1: # Verificar se um ponto foi encontrado e, se sim, extrair a extensão
        extensao = arquivo[posicao_ponto:]

        # Carregar a imagem
        caminho_imagem = os.path.join(diretorio_imagens, arquivo)
        print("   Carregando imagem:", caminho_imagem)
        imagem = cv2.imread(caminho_imagem, cv2.IMREAD_UNCHANGED)

        # Encontrar os contornos na imagem
        contornos, _ = cv2.findContours(imagem[:, :, 3], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contornos) > 0:
            # Encontrar o contorno com a maior área (presumindo que seja o círculo central)
            maior_contorno = max(contornos, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(maior_contorno)

            # Calcular o centro do círculo
            centro_x = x + w // 2
            centro_y = y + h // 2

            # Calcular o tamanho do quadrado
            tamanho_quadrado = max(w, h)

            # Criar uma imagem quadrada com fundo transparente
            imagem_quadrada = np.zeros((tamanho_quadrado, tamanho_quadrado, 4), dtype=np.uint8)

            # Calcular as coordenadas para colar o círculo no centro da imagem quadrada
            x1 = (tamanho_quadrado - w) // 2
            x2 = x1 + w
            y1 = (tamanho_quadrado - h) // 2
            y2 = y1 + h

            # Colar o círculo no centro da imagem quadrada
            imagem_quadrada[y1:y2, x1:x2] = imagem[y:y + h, x:x + w]

            # Salvar a imagem cortada em formato PNG com fundo transparente
            nome_saida = os.path.splitext(arquivo)[0] + extensao # _cortada.png
            caminho_saida = os.path.join(diretorio_saida, nome_saida)
            cv2.imwrite(caminho_saida, imagem_quadrada)
            print("   - Imagem cortada salva em:", caminho_saida)
        else:
            print("   - ATENÇÃO: imagem ignorada")
            print("Nenhum contorno encontrado na imagem", arquivo)
    else:
        print("Encerrando! Este arquivo não possui uma extensão, verifique:", arquivo)
        exit(1)
print("\n\n=> Processo Concluído \nVefifique as novas imagens no diretório de saída:", diretorio_saida, "\n")