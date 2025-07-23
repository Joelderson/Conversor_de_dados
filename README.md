# Conversor de Dados MATLAB para CSV

## 📋 Descrição

Este projeto converte arquivos de dados MATLAB (.mat) para formato CSV, especificamente otimizado para dados de vibração de rolamentos de motores elétricos. O conversor é especialmente projetado para trabalhar com datasets de análise de falhas em rolamentos, organizando os dados de forma estruturada e facilitando análises posteriores.

## 🎯 Funcionalidades

- **Conversão Automática**: Converte arquivos .mat para .csv mantendo a estrutura de pastas
- **Seleção Inteligente de Canais**: Prioriza automaticamente canais DE_time (Drive End) e FE_time (Fan End)
- **Organização Estruturada**: Mantém a hierarquia de pastas original
- **Metadados**: Gera arquivo de metadados com informações sobre a conversão
- **Logging Detalhado**: Registra todo o processo de conversão
- **Tratamento de Erros**: Identifica e reporta problemas durante a conversão

## 📁 Estrutura do Projeto

```
conversor_de_dados/
├── converter_matlab_para_csv.py    # Script principal de conversão
├── analisar_dados_convertidos.py   # Script de análise dos dados convertidos
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── .gitignore                      # Arquivos ignorados pelo Git
├── dados_matlab/                   # Dados originais em formato MATLAB
│   ├── Normal/
│   ├── 12k_Drive_End_Bearing_Fault_Data/
│   ├── 12k_Fan_End_Bearing_Fault_Data/
│   └── 48k_Drive_End_Bearing_Fault_Data/
└── dados_convertidos/              # Dados convertidos para CSV
    ├── Normal/
    ├── 12k_Drive_End_Bearing_Fault_Data/
    ├── 12k_Fan_End_Bearing_Fault_Data/
    ├── 48k_Drive_End_Bearing_Fault_Data/
    ├── metadados_conversao.json
    └── relatorio_analise_dados.json
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Dependências Principais

- `scipy`: Para carregar arquivos MATLAB
- `pandas`: Para manipulação de dados
- `numpy`: Para operações numéricas
- `pathlib`: Para manipulação de caminhos

## 📖 Como Usar

### Conversão Básica

```bash
python converter_matlab_para_csv.py
```

O script irá:
1. Ler todos os arquivos .mat da pasta `dados_matlab/`
2. Converter cada arquivo para CSV
3. Manter a estrutura de pastas original
4. Salvar os arquivos convertidos em `dados_convertidos/`
5. Gerar metadados da conversão

### Análise dos Dados Convertidos

```bash
python analisar_dados_convertidos.py
```

Este script analisa os dados convertidos e gera relatórios estatísticos.

## 📊 Estrutura dos Dados

### Organização das Pastas

- **Normal**: Dados de operação normal (sem falhas)
- **12k_Drive_End_Bearing_Fault_Data**: Falhas a 12.000 RPM, sensor no lado do acionamento
- **12k_Fan_End_Bearing_Fault_Data**: Falhas a 12.000 RPM, sensor no lado da ventoinha
- **48k_Drive_End_Bearing_Fault_Data**: Falhas a 48.000 RPM, sensor no lado do acionamento

### Tipos de Falha

- **B**: Ball Fault (falha na esfera)
- **IR**: Inner Race Fault (falha na pista interna)
- **OR**: Outer Race Fault (falha na pista externa)

### Cargas Aplicadas

- **007**: 7 milipolegadas (carga leve)
- **014**: 14 milipolegadas (carga média)
- **021**: 21 milipolegadas (carga pesada)
- **028**: 28 milipolegadas (carga muito pesada)

### Nomenclatura dos Arquivos

Cada subpasta contém 4 arquivos CSV com a nomenclatura:
- `[ID]_0.csv`: Primeira amostra temporal
- `[ID]_1.csv`: Segunda amostra temporal
- `[ID]_2.csv`: Terceira amostra temporal
- `[ID]_3.csv`: Quarta amostra temporal

## 🔧 Configuração

### Personalizando a Conversão

Você pode modificar o script `converter_matlab_para_csv.py` para:

1. **Alterar pastas de entrada/saída**:
   ```python
   pasta_entrada = "sua_pasta_matlab"
   pasta_saida = "sua_pasta_csv"
   ```

2. **Modificar a prioridade de canais**:
   ```python
   for prioridade in ['DE_time', 'FE_time']:  # Altere a ordem conforme necessário
   ```

3. **Adicionar filtros de arquivos**:
   ```python
   # Adicione condições no loop de processamento
   if "especifico" in str(arquivo_mat):
       continue
   ```

## 📈 Aplicações

Este conversor é ideal para:

- **Machine Learning**: Preparação de dados para treinamento de modelos
- **Análise de Sinais**: Processamento de dados de vibração
- **Manutenção Preditiva**: Desenvolvimento de sistemas de monitoramento
- **Pesquisa**: Estudos de falhas em rolamentos
- **Validação**: Testes de algoritmos de detecção de falhas

## 🐛 Solução de Problemas

### Arquivo CSV Vazio

Se um arquivo CSV for gerado apenas com cabeçalho, verifique:
1. Se o arquivo .mat original contém dados válidos
2. Se há múltiplas chaves no arquivo .mat
3. Se a chave correta está sendo selecionada

### Erro de Memória

Para arquivos muito grandes:
1. Aumente a memória disponível
2. Processe arquivos em lotes menores
3. Use compressão de dados

### Dependências Ausentes

```bash
pip install --upgrade scipy pandas numpy
```

## 📝 Logs e Relatórios

O sistema gera vários arquivos de informação:

- **metadados_conversao.json**: Informações sobre a conversão
- **relatorio_analise_dados.json**: Estatísticas dos dados convertidos
- **Logs no console**: Informações detalhadas do processo

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

**Joelderson**
- GitHub: [@Joelderson](https://github.com/Joelderson)
- Repositório: [Conversor_de_dados](https://github.com/Joelderson/Conversor_de_dados.git)

## 🙏 Agradecimentos

- Dataset de falhas em rolamentos da Case Western Reserve University
- Comunidade Python para as bibliotecas utilizadas
- Contribuidores e testadores do projeto

---

**Versão**: 1.0.0  
**Última Atualização**: Janeiro 2025  
**Status**: ✅ Funcional 