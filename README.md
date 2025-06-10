# Conversor de Dados MATLAB para CSV - Dataset CWRU Bearing

## 📋 Descrição do Projeto

Este projeto converte dados de vibração de rolamentos do formato MATLAB (.mat) para CSV, facilitando a análise e processamento para machine learning. Os dados são do Case Western Reserve University (CWRU) Bearing Data Center.

## 🎯 Objetivo

Converter dados de vibração de rolamentos de motores elétricos para formato CSV, mantendo a estrutura organizacional e permitindo fácil análise para detecção de falhas.

## 📁 Estrutura do Projeto

```
Conversor/
├── dados_matlab/                    # Dados originais em MATLAB
│   ├── Normal/                      # Dados de operação normal
│   ├── 12k_Drive_End_Bearing_Fault_Data/  # Falhas a 12k RPM (Drive End)
│   ├── 12k_Fan_End_Bearing_Fault_Data/    # Falhas a 12k RPM (Fan End)
│   └── 48k_Drive_End_Bearing_Fault_Data/  # Falhas a 48k RPM (Drive End)
├── dados_convertidos/               # Dados convertidos para CSV
│   ├── Normal/                      # Dados normais convertidos
│   ├── 12k_Drive_End_Bearing_Fault_Data/  # Falhas convertidas
│   ├── 12k_Fan_End_Bearing_Fault_Data/    # Falhas convertidas
│   ├── 48k_Drive_End_Bearing_Fault_Data/  # Falhas convertidas
│   ├── metadados_conversao.json     # Metadados da conversão
│   ├── relatorio_analise_dados.json # Relatório de análise
│   └── relatorio_explicativo.txt    # Explicação detalhada
├── converter_matlab_para_csv.py     # Script principal de conversão
├── analisar_dados_convertidos.py    # Script de análise dos dados
├── requirements.txt                 # Dependências Python
└── README.md                       # Este arquivo
```

## 🔧 Scripts Incluídos

### 1. `converter_matlab_para_csv.py`
- **Função:** Converte todos os arquivos MATLAB para CSV
- **Recursos:**
  - Processamento recursivo de pastas
  - Manutenção da estrutura organizacional
  - Geração de metadados
  - Logging detalhado
  - Tratamento de erros

### 2. `analisar_dados_convertidos.py`
- **Função:** Analisa os dados convertidos
- **Recursos:**
  - Análise estatística dos dados
  - Geração de relatórios
  - Explicação detalhada da estrutura
  - Contagem de arquivos por categoria

## 📊 Estrutura dos Dados

### Categorias Principais
- **Normal:** Dados de operação normal (sem falhas)
- **12k_Drive_End:** Falhas a 12.000 RPM (lado do acionamento)
- **12k_Fan_End:** Falhas a 12.000 RPM (lado da ventoinha)
- **48k_Drive_End:** Falhas a 48.000 RPM (lado do acionamento)

### Tipos de Falhas
- **OR:** Outer Race Fault (falha na pista externa)
- **IR:** Inner Race Fault (falha na pista interna)
- **B:** Ball Fault (falha na esfera)

### Cargas Aplicadas
- **007:** 7 milipolegadas (carga leve)
- **014:** 14 milipolegadas (carga média)
- **021:** 21 milipolegadas (carga pesada)
- **028:** 28 milipolegadas (carga muito pesada)

### Condições de Operação
- **@3:** Baixa carga
- **@6:** Carga média
- **@12:** Alta carga

## 📈 Estatísticas dos Dados

- **Total de arquivos convertidos:** 161
- **Tamanho total:** ~656 MB
- **Frequência de amostragem:** 12kHz e 48kHz
- **Formato dos dados:** Série temporal de aceleração (g)

## 🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Converter Dados MATLAB para CSV
```bash
python converter_matlab_para_csv.py
```

### 3. Analisar Dados Convertidos
```bash
python analisar_dados_convertidos.py
```

## 📋 Dependências

- `scipy>=1.9.0`
- `pandas>=1.5.0`
- `numpy>=1.21.0`
- `matplotlib>=3.5.0`
- `seaborn>=0.11.0`

## 📄 Arquivos de Relatório

### `metadados_conversao.json`
Contém informações sobre a conversão, incluindo:
- Data e hora da conversão
- Estrutura completa das pastas
- Tamanho dos arquivos originais

### `relatorio_analise_dados.json`
Relatório técnico com:
- Estatísticas dos dados convertidos
- Análise por categoria
- Informações sobre amostras

### `relatorio_explicativo.txt`
Explicação detalhada de:
- Significado de cada pasta e subpasta
- Numerações e condições
- Estrutura dos arquivos CSV

## 🎯 Aplicações

Este dataset é ideal para:
- **Machine Learning:** Detecção e diagnóstico de falhas
- **Análise de Sinais:** Processamento de vibração
- **Manutenção Preditiva:** Desenvolvimento de modelos
- **Pesquisa:** Estudos em engenharia mecânica

## 📚 Referências

- **Fonte dos dados:** Case Western Reserve University Bearing Data Center
- **Aplicação:** Análise de falhas em rolamentos de motores elétricos
- **Formato original:** MATLAB (.mat)
- **Formato convertido:** CSV

## 👨‍💻 Autor

Desenvolvido para conversão e análise de dados de vibração de rolamentos.

---

**Nota:** Este projeto converte dados MATLAB para CSV mantendo toda a estrutura organizacional original, facilitando análises posteriores e aplicações de machine learning. 