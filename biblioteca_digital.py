import os
from datetime import datetime
import json
import shutil # Módulo para manipulação de arquivos de alto nível

# Define o nome do diretório principal da biblioteca
DIRETORIO_BIBLIOTECA = 'documentos_digitais'

# Se o diretório não existir, ele será criado
if not os.path.exists(DIRETORIO_BIBLIOTECA):
    os.makedirs(DIRETORIO_BIBLIOTECA)
    print(f"Diretório '{DIRETORIO_BIBLIOTECA}' criado.")

def listar_e_organizar_documentos():
    """Lista e organiza documentos por tipo de arquivo e ano de modificação."""
    estrutura_organizacional = {}

    for nome_arquivo in os.listdir(DIRETORIO_BIBLIOTECA):
        caminho_completo = os.path.join(DIRETORIO_BIBLIOTECA, nome_arquivo)
        
        # Ignora subdiretórios
        if os.path.isdir(caminho_completo):
            continue

        # Extrai Tipo (Extensão)
        _, extensao = os.path.splitext(nome_arquivo)
        tipo_arquivo = extensao.lower() if extensao else '(sem_extensao)'
        
        # Extrai o Ano de Modificação (proxy para o ano de publicação)
        try:
            timestamp_modificacao = os.path.getmtime(caminho_completo)
            ano_publicacao = datetime.fromtimestamp(timestamp_modificacao).strftime('%Y')
        except Exception:
            ano_publicacao = '(data_indisponível)'


        # Organiza na estrutura aninhada: {tipo: {ano: [arquivos]}}
        if tipo_arquivo not in estrutura_organizacional:
            estrutura_organizacional[tipo_arquivo] = {}
        
        if ano_publicacao not in estrutura_organizacional[tipo_arquivo]:
            estrutura_organizacional[tipo_arquivo][ano_publicacao] = []
        
        estrutura_organizacional[tipo_arquivo][ano_publicacao].append(nome_arquivo)
            
    return estrutura_organizacional

# --- Funções de Manipulação de Arquivos (CRUD) ---

def adicionar_documento(nome_novo):
    """Simula adicionar um documento novo à biblioteca (cria um arquivo vazio)."""
    caminho_destino = os.path.join(DIRETORIO_BIBLIOTECA, nome_novo)
    
    if os.path.exists(caminho_destino):
         return f"ERRO: Documento '{nome_novo}' já existe na biblioteca."

    try:
        # Cria um arquivo vazio (simulação de cópia)
        with open(caminho_destino, 'w') as f:
            f.write(f"Conteúdo simulado: {nome_novo}")
        
        # Simula uma data de criação diferente para teste de organização (opcional)
        # Por exemplo, se o nome tiver o ano, você pode simular a data.
        
        return f"SUCESSO: Documento '{nome_novo}' adicionado à biblioteca."
    except Exception as e:
        return f"ERRO ao adicionar: {e}"

def renomear_documento(nome_antigo, nome_novo):
    """Renomeia um documento dentro do diretório da biblioteca."""
    caminho_antigo = os.path.join(DIRETORIO_BIBLIOTECA, nome_antigo)
    caminho_novo = os.path.join(DIRETORIO_BIBLIOTECA, nome_novo)
    
    if os.path.exists(caminho_antigo):
        try:
            os.rename(caminho_antigo, caminho_novo)
            return f"SUCESSO: '{nome_antigo}' renomeado para '{nome_novo}'."
        except Exception as e:
            return f"ERRO ao renomear: {e}"
    else:
        return f"ERRO: Documento '{nome_antigo}' não encontrado."

def remover_documento(nome_arquivo):
    """Remove (deleta) um documento da biblioteca."""
    caminho_completo = os.path.join(DIRETORIO_BIBLIOTECA, nome_arquivo)
    
    if os.path.exists(caminho_completo):
        try:
            os.remove(caminho_completo)
            return f"SUCESSO: Documento '{nome_arquivo}' removido."
        except Exception as e:
            return f"ERRO ao remover: {e}"
    else:
        return f"ERRO: Documento '{nome_arquivo}' não encontrado."


# --- Interface de Linha de Comando (CLI) ---

def cli_interface():
    """Interface principal para interação com os bibliotecários."""
    print("\n--- Sistema de Gestão de Biblioteca Digital ---")
    
    # Adiciona alguns arquivos de teste na primeira execução
    if not os.listdir(DIRETORIO_BIBLIOTECA):
        adicionar_documento("tese_doutorado_2025.pdf")
        adicionar_documento("artigo_IA_2024.epub")
        adicionar_documento("manual_de_uso_2023.doc")

    while True:
        print("\nOpções:")
        print("1. Listar e Organizar Documentos")
        print("2. Adicionar Novo Documento (Simulado)")
        print("3. Renomear Documento")
        print("4. Remover Documento")
        print("5. Sair")
        
        escolha = input("Escolha uma opção (1-5): ")
        
        if escolha == '1':
            organizacao = listar_e_organizar_documentos()
            print("\n--- Organização Atual ---")
            # O json.dumps exibe o dicionário de forma formatada e legível
            print(json.dumps(organizacao, indent=4, ensure_ascii=False)) 
            print("-------------------------\n")
            
        elif escolha == '2':
            nome_novo = input("Digite o nome do novo documento (ex: Livro_Quimica.pdf): ")
            print(adicionar_documento(nome_novo))
            
        elif escolha == '3':
            antigo = input("Digite o nome do arquivo a ser renomeado: ")
            novo = input("Digite o novo nome do arquivo: ")
            print(renomear_documento(antigo, novo))
            
        elif escolha == '4':
            nome = input("Digite o nome do arquivo a ser removido: ")
            print(remover_documento(nome))
            
        elif escolha == '5':
            print("Saindo do sistema. Até logo!")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

# Garante que a interface CLI inicia quando o script é executado
if __name__ == "__main__":
    cli_interface()