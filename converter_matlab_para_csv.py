import os
import scipy.io
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_arquivo_matlab(caminho_arquivo):
    """
    Carrega um arquivo MATLAB e retorna os dados como dicionário
    """
    try:
        dados = scipy.io.loadmat(caminho_arquivo)
        return dados
    except Exception as e:
        logger.error(f"Erro ao carregar {caminho_arquivo}: {e}")
        return None

def converter_dados_para_dataframe(dados_matlab):
    """
    Converte os dados MATLAB para um DataFrame pandas
    """
    if dados_matlab is None:
        return None
    
    # Remover chaves especiais do MATLAB
    chaves_para_remover = ['__header__', '__version__', '__globals__']
    dados_limpos = {k: v for k, v in dados_matlab.items() if k not in chaves_para_remover}
    
    # Se há apenas uma chave de dados, usar ela diretamente
    if len(dados_limpos) == 1:
        chave_dados = list(dados_limpos.keys())[0]
        dados_array = dados_limpos[chave_dados]
    else:
        # Se há múltiplas chaves, tentar encontrar a que contém os dados principais
        for chave, valor in dados_limpos.items():
            if isinstance(valor, np.ndarray) and valor.size > 0:
                dados_array = valor
                break
        else:
            logger.warning("Não foi possível identificar os dados principais")
            return None
    
    # Converter para DataFrame
    if dados_array.ndim == 1:
        df = pd.DataFrame(dados_array, columns=['valor'])
    elif dados_array.ndim == 2:
        if dados_array.shape[1] == 1:
            df = pd.DataFrame(dados_array, columns=['valor'])
        else:
            df = pd.DataFrame(dados_array)
    else:
        # Para arrays 3D ou maiores, achatamos para 2D
        dados_reshaped = dados_array.reshape(dados_array.shape[0], -1)
        df = pd.DataFrame(dados_reshaped)
    
    return df

def converter_arquivo_matlab_para_csv(caminho_entrada, caminho_saida):
    """
    Converte um arquivo MATLAB específico para CSV
    """
    try:
        # Carregar dados MATLAB
        dados_matlab = carregar_arquivo_matlab(caminho_entrada)
        if dados_matlab is None:
            return False
        
        # Converter para DataFrame
        df = converter_dados_para_dataframe(dados_matlab)
        if df is None:
            return False
        
        # Criar diretório de saída se não existir
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        
        # Salvar como CSV
        df.to_csv(caminho_saida, index=False)
        logger.info(f"Convertido: {caminho_entrada} -> {caminho_saida}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao converter {caminho_entrada}: {e}")
        return False

def processar_pasta_recursivamente(pasta_entrada, pasta_saida):
    """
    Processa recursivamente todas as pastas e arquivos MATLAB
    """
    pasta_entrada = Path(pasta_entrada)
    pasta_saida = Path(pasta_saida)
    
    # Criar pasta de saída se não existir
    pasta_saida.mkdir(parents=True, exist_ok=True)
    
    arquivos_processados = 0
    arquivos_erro = 0
    
    # Percorrer todos os arquivos .mat recursivamente
    for arquivo_mat in pasta_entrada.rglob("*.mat"):
        try:
            # Calcular caminho relativo para manter estrutura
            caminho_relativo = arquivo_mat.relative_to(pasta_entrada)
            
            # Criar caminho de saída com extensão .csv
            caminho_saida = pasta_saida / caminho_relativo.with_suffix('.csv')
            
            # Converter arquivo
            if converter_arquivo_matlab_para_csv(str(arquivo_mat), str(caminho_saida)):
                arquivos_processados += 1
            else:
                arquivos_erro += 1
                
        except Exception as e:
            logger.error(f"Erro ao processar {arquivo_mat}: {e}")
            arquivos_erro += 1
    
    return arquivos_processados, arquivos_erro

def criar_arquivo_metadados(pasta_entrada, pasta_saida):
    """
    Cria um arquivo de metadados com informações sobre a conversão
    """
    metadados = {
        'pasta_origem': str(pasta_entrada),
        'pasta_destino': str(pasta_saida),
        'data_conversao': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'estrutura_pastas': {}
    }
    
    # Mapear estrutura de pastas
    pasta_entrada = Path(pasta_entrada)
    for item in pasta_entrada.rglob("*"):
        if item.is_dir():
            rel_path = str(item.relative_to(pasta_entrada))
            metadados['estrutura_pastas'][rel_path] = 'diretório'
        elif item.suffix == '.mat':
            rel_path = str(item.relative_to(pasta_entrada))
            metadados['estrutura_pastas'][rel_path] = f'arquivo_matlab ({item.stat().st_size / 1024 / 1024:.1f} MB)'
    
    # Salvar metadados
    caminho_metadados = Path(pasta_saida) / 'metadados_conversao.json'
    import json
    with open(caminho_metadados, 'w', encoding='utf-8') as f:
        json.dump(metadados, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Metadados salvos em: {caminho_metadados}")

def main():
    """
    Função principal para executar a conversão
    """
    pasta_entrada = "dados_matlab"
    pasta_saida = "dados_convertidos"
    
    logger.info("Iniciando conversão de arquivos MATLAB para CSV...")
    logger.info(f"Pasta de entrada: {pasta_entrada}")
    logger.info(f"Pasta de saída: {pasta_saida}")
    
    # Verificar se a pasta de entrada existe
    if not os.path.exists(pasta_entrada):
        logger.error(f"Pasta de entrada não encontrada: {pasta_entrada}")
        return
    
    # Processar todos os arquivos
    arquivos_processados, arquivos_erro = processar_pasta_recursivamente(pasta_entrada, pasta_saida)
    
    # Criar arquivo de metadados
    criar_arquivo_metadados(pasta_entrada, pasta_saida)
    
    # Relatório final
    logger.info("=" * 50)
    logger.info("RELATÓRIO DE CONVERSÃO")
    logger.info("=" * 50)
    logger.info(f"Arquivos processados com sucesso: {arquivos_processados}")
    logger.info(f"Arquivos com erro: {arquivos_erro}")
    logger.info(f"Total de arquivos: {arquivos_processados + arquivos_erro}")
    logger.info("=" * 50)
    
    if arquivos_erro == 0:
        logger.info("✅ Conversão concluída com sucesso!")
    else:
        logger.warning(f"⚠️ Conversão concluída com {arquivos_erro} erros.")

if __name__ == "__main__":
    main() 