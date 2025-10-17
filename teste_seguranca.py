import unittest
import hashlib
import requests
import sys
HIBP_API_URL = "https://api.pwnedpasswords.com/range/" #API que contém senhas que ja foram vazadas

#               INFORMAÇÕES PARA EXECUÇÃO
#
#  Intalações Necessárias: pip install requests
#  Execução: python teste_segurnaca.py
# --------------------------------------------------------
import hashlib

def hash_senha(senha):
    hash_sha1 = hashlib.sha1(senha.encode('utf-8')).hexdigest().upper()
    
    # 2. Separar prefixo (5 caracteres)
    prefixo = hash_sha1[:5]
    
    # 3. Separar sufixo (o restante)
    sufixo = hash_sha1[5:]
    
    return prefixo, sufixo

def verificar_senha_vazada(senha):
    
    prefixo, sufixo = hash_senha(senha)

    url_completa = HIBP_API_URL + prefixo
    
    headers = {
        'User-Agent': 'Meu Projeto de Verificação de Vazamentos'
    }
    
    try:
        response = requests.get(url_completa, headers=headers)
        response.raise_for_status() # Levanta um erro para códigos 4xx/5xx

        #Linhas para busca
        linhas = response.text.splitlines()
        
        # For que realiza a procura pelo sufixo completo
        for linha in linhas:
            hash_sufixo_retornado, contagem = linha.split(':')
            
            # Compara o sufixo da senha procurada e compara com os sufixos encontrados na API
            if hash_sufixo_retornado == sufixo:
                # Se encontrar, retorna a contagem de vazamentos
                return int(contagem)
                
        #Se o Loop for encerrado e nada for encontrado, a senha não foi vazada
        return 0

    #Indica erro ao utilizar a API
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do HIBP: {e}", file=sys.stderr)
        return -1
        
if __name__ == '__main__':
    senha = input('Escreva a senha que deseja verificar:')

    contagem_vazada = verificar_senha_vazada(senha)
    
    print("-" * 50)
    
    if contagem_vazada > 0:
        print(f"Senha '{senha}' VAZOU! Encontrada {contagem_vazada} vezes.")
    else:
        print(f"Senha '{senha}' está SEGURA (0 vazamentos encontrados).")

    print("-" * 50)
