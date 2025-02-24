import os
import glob
from datetime import datetime

# Caminho da pasta onde as imagens são salvas
pasta_downloads = r"C:\Users\Prefeitura\Downloads"

# Busca arquivos de imagem na pasta
formatos = ["*.jpeg"]
imagens = []

for formato in formatos:
    imagens.extend(glob.glob(os.path.join(pasta_downloads, formato)))

# Ordena as imagens por data de modificação (mais recente primeiro)
imagens.sort(key=os.path.getmtime, reverse=True)

# Pega apenas as 6 imagens mais recentes
imagens = imagens[:6]

# Verifica se há imagens na lista
if not imagens:
    print("Nenhuma imagem encontrada.")
else:
    # Pergunta o nome base para os arquivos
    nome_base = input("Digite o nome base para as imagens (sem numeração e extensão): ")

    print("Renomeando as 6 imagens mais recentes:")

    for i, img in enumerate(imagens, 1):
        # Obtém a extensão original do arquivo
        extensao = os.path.splitext(img)[1]

        # Define o novo nome com numeração sequencial
        novo_nome = f"{nome_base}_{i}{extensao}"

        # Garante que a extensão e o caminho original permaneçam
        novo_caminho = os.path.join(os.path.dirname(img), novo_nome)

        # Renomeia o arquivo
        os.rename(img, novo_caminho)
        print(f"{os.path.basename(img)} → {novo_nome}")
