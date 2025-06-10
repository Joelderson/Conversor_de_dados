import os
import pandas as pd
import numpy as np
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analisar_estrutura_dados(pasta_dados):
    """
    Analisa a estrutura completa dos dados convertidos
    """
    print("🔍 ANALISANDO ESTRUTURA DOS DADOS CONVERTIDOS")
    print("=" * 60)
    
    pasta = Path(pasta_dados)
    estrutura = {}
    
    # Contar arquivos por categoria
    categorias = {}
    total_arquivos = 0
    
    for arquivo_csv in pasta.rglob("*.csv"):
        if arquivo_csv.name == "metadados_conversao.json":
            continue
            
        caminho_relativo = arquivo_csv.relative_to(pasta)
        partes = caminho_relativo.parts
        
        # Identificar categoria principal
        if len(partes) >= 1:
            categoria_principal = partes[0]
            if categoria_principal not in categorias:
                categorias[categoria_principal] = {
                    'total_arquivos': 0,
                    'subcategorias': {},
                    'tamanho_total': 0
                }
            
            categorias[categoria_principal]['total_arquivos'] += 1
            categorias[categoria_principal]['tamanho_total'] += arquivo_csv.stat().st_size
            
            # Analisar subcategorias
            if len(partes) >= 2:
                subcategoria = partes[1]
                if subcategoria not in categorias[categoria_principal]['subcategorias']:
                    categorias[categoria_principal]['subcategorias'][subcategoria] = 0
                categorias[categoria_principal]['subcategorias'][subcategoria] += 1
            
            total_arquivos += 1
    
    return categorias, total_arquivos

def analisar_conteudo_arquivo(caminho_arquivo):
    """
    Analisa o conteúdo de um arquivo CSV específico
    """
    try:
        df = pd.read_csv(caminho_arquivo)
        
        # Estatísticas básicas
        estatisticas = {
            'linhas': len(df),
            'colunas': len(df.columns),
            'colunas_nomes': list(df.columns),
            'memoria_uso': df.memory_usage(deep=True).sum(),
            'tipos_dados': df.dtypes.to_dict()
        }
        
        # Se há dados numéricos, calcular estatísticas
        if len(df.select_dtypes(include=[np.number]).columns) > 0:
            df_numerico = df.select_dtypes(include=[np.number])
            estatisticas.update({
                'min': df_numerico.min().to_dict(),
                'max': df_numerico.max().to_dict(),
                'media': df_numerico.mean().to_dict(),
                'desvio_padrao': df_numerico.std().to_dict(),
                'primeiros_valores': df_numerico.iloc[:5].to_dict('records')
            })
        
        return estatisticas
    except Exception as e:
        return {'erro': str(e)}

def gerar_relatorio_completo(pasta_dados):
    """
    Gera um relatório completo dos dados convertidos
    """
    print("📊 GERANDO RELATÓRIO COMPLETO DOS DADOS")
    print("=" * 60)
    
    # Analisar estrutura
    categorias, total_arquivos = analisar_estrutura_dados(pasta_dados)
    
    # Relatório principal
    relatorio = {
        'data_analise': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_arquivos_csv': total_arquivos,
        'categorias_principais': {},
        'amostras_por_categoria': {},
        'estatisticas_gerais': {}
    }
    
    print(f"📁 Total de arquivos CSV: {total_arquivos}")
    print(f"📂 Categorias principais: {len(categorias)}")
    print()
    
    # Analisar cada categoria
    for categoria, info in categorias.items():
        print(f"🔧 CATEGORIA: {categoria}")
        print(f"   📄 Arquivos: {info['total_arquivos']}")
        print(f"   💾 Tamanho: {info['tamanho_total'] / 1024 / 1024:.1f} MB")
        
        if info['subcategorias']:
            print(f"   📂 Subcategorias:")
            for subcat, count in info['subcategorias'].items():
                print(f"      - {subcat}: {count} arquivos")
        
        # Analisar amostra de arquivos desta categoria
        arquivos_categoria = list(Path(pasta_dados).rglob(f"{categoria}/*.csv"))
        if arquivos_categoria:
            amostra_arquivo = arquivos_categoria[0]
            print(f"   🔍 Analisando amostra: {amostra_arquivo.name}")
            
            estatisticas = analisar_conteudo_arquivo(amostra_arquivo)
            relatorio['amostras_por_categoria'][categoria] = {
                'arquivo_amostra': amostra_arquivo.name,
                'estatisticas': estatisticas
            }
            
            if 'erro' not in estatisticas:
                print(f"      📊 Linhas: {estatisticas['linhas']:,}")
                print(f"      📋 Colunas: {estatisticas['colunas']}")
                print(f"      💾 Memória: {estatisticas['memoria_uso'] / 1024 / 1024:.1f} MB")
                if 'primeiros_valores' in estatisticas:
                    print(f"      📈 Primeiros valores: {estatisticas['primeiros_valores'][0]}")
        
        relatorio['categorias_principais'][categoria] = info
        print()
    
    # Salvar relatório
    caminho_relatorio = Path(pasta_dados) / 'relatorio_analise_dados.json'
    with open(caminho_relatorio, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Relatório salvo em: {caminho_relatorio}")
    return relatorio

def explicar_significado_dados():
    """
    Explica o significado de cada elemento dos dados
    """
    print("\n📚 EXPLICAÇÃO DETALHADA DOS DADOS")
    print("=" * 60)
    
    explicacao = {
        "estrutura_geral": {
            "descricao": "Dataset de Análise de Falhas em Rolamentos de Motores Elétricos",
            "fonte": "Case Western Reserve University Bearing Data Center",
            "aplicacao": "Machine Learning para Detecção e Diagnóstico de Falhas"
        },
        
        "categorias_principais": {
            "Normal": {
                "significado": "Dados de operação normal do rolamento (sem falhas)",
                "condicoes": "Rolamento em perfeitas condições de funcionamento",
                "uso": "Linha de base para comparação com dados de falha"
            },
            
            "12k_Drive_End_Bearing_Fault_Data": {
                "significado": "Dados de falhas em rolamentos do lado do acionamento a 12.000 RPM",
                "localizacao": "Lado do motor onde a carga é aplicada",
                "velocidade": "12.000 rotações por minuto"
            },
            
            "12k_Fan_End_Bearing_Fault_Data": {
                "significado": "Dados de falhas em rolamentos do lado da ventoinha a 12.000 RPM",
                "localizacao": "Lado oposto ao acionamento (ventoinha)",
                "velocidade": "12.000 rotações por minuto"
            },
            
            "48k_Drive_End_Bearing_Fault_Data": {
                "significado": "Dados de falhas em rolamentos do lado do acionamento a 48.000 RPM",
                "localizacao": "Lado do motor onde a carga é aplicada",
                "velocidade": "48.000 rotações por minuto"
            }
        },
        
        "tipos_falhas": {
            "OR": {
                "nome": "Outer Race Fault",
                "significado": "Falha na pista externa do rolamento",
                "caracteristicas": "Vibração característica na frequência de passagem dos elementos rolantes"
            },
            
            "IR": {
                "nome": "Inner Race Fault", 
                "significado": "Falha na pista interna do rolamento",
                "caracteristicas": "Vibração com modulação de amplitude"
            },
            
            "B": {
                "nome": "Ball Fault",
                "significado": "Falha nos elementos rolantes (esferas)",
                "caracteristicas": "Vibração periódica na frequência de rotação das esferas"
            }
        },
        
        "cargas": {
            "007": "7 milipolegadas (carga leve)",
            "014": "14 milipolegadas (carga média)", 
            "021": "21 milipolegadas (carga pesada)",
            "028": "28 milipolegadas (carga muito pesada)"
        },
        
        "condicoes_operacao": {
            "@3": "Condição de operação 3 (baixa carga)",
            "@6": "Condição de operação 6 (carga média)",
            "@12": "Condição de operação 12 (alta carga)"
        },
        
        "dados_vibracao": {
            "tipo": "Sinais de vibração acelerométricos",
            "frequencia_amostragem": "12.000 Hz (12k) ou 48.000 Hz (48k)",
            "duracao": "Varia de 1 a 10 segundos por arquivo",
            "unidade": "g (aceleração gravitacional)",
            "formato": "Série temporal unidimensional"
        }
    }
    
    # Imprimir explicação
    for secao, conteudo in explicacao.items():
        print(f"\n📖 {secao.upper().replace('_', ' ')}:")
        if isinstance(conteudo, dict):
            for item, desc in conteudo.items():
                if isinstance(desc, dict):
                    print(f"   🔹 {item}:")
                    for subitem, subdesc in desc.items():
                        print(f"      • {subitem}: {subdesc}")
                else:
                    print(f"   🔹 {item}: {desc}")
        else:
            print(f"   {conteudo}")
    
    return explicacao

def main():
    """
    Função principal para executar análise completa
    """
    pasta_dados = "dados_convertidos"
    
    print("🚀 INICIANDO ANÁLISE COMPLETA DOS DADOS CONVERTIDOS")
    print("=" * 60)
    
    # Verificar se a pasta existe
    if not os.path.exists(pasta_dados):
        print(f"❌ Pasta {pasta_dados} não encontrada!")
        return
    
    # Gerar relatório técnico
    relatorio = gerar_relatorio_completo(pasta_dados)
    
    # Explicar significado dos dados
    explicacao = explicar_significado_dados()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("🎯 RESUMO FINAL DA ANÁLISE")
    print("=" * 60)
    print(f"✅ Total de arquivos analisados: {relatorio['total_arquivos_csv']}")
    print(f"📂 Categorias principais: {len(relatorio['categorias_principais'])}")
    print(f"🔧 Tipos de falhas: OR, IR, B")
    print(f"⚡ Velocidades: 12k RPM, 48k RPM")
    print(f"📊 Dados de vibração: Série temporal acelerométrica")
    print(f"🎯 Aplicação: Machine Learning para detecção de falhas")
    print("=" * 60)
    print("✅ Análise completa finalizada!")

if __name__ == "__main__":
    main() 