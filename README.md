# 📊 Dashboard de Insights do ENEM

> **Decodificando o ENEM: Dos Dados Brutos às Estratégias Pedagógicas**

Uma plataforma interativa desenvolvida como Projeto Integrador em Computação IV que democratiza o acesso aos microdados do ENEM, permitindo a extração de insights valiosos sobre o desempenho e perfil dos estudantes brasileiros.

## 🎯 Objetivo

Este projeto visa resolver o problema de que professores e gestores educacionais não possuem ferramentas acessíveis para explorar a imensa base de dados do ENEM, dificultando a extração de informações para embasar estratégias pedagógicas eficazes.

## 📈 Dados Analisados

- **3.300.000+ candidatos** analisados
- **Microdados do ENEM** com informações demográficas, socioeconômicas e de desempenho
- **Dados de 27 estados** brasileiros
- **Análise temporal** e comparativa entre regiões

## 🚀 Funcionalidades

### Dashboard Interativo (Streamlit)
- **Filtros dinâmicos** por estado, renda, gênero e outras variáveis
- **Visualizações interativas** com Plotly
- **Análise de desigualdades** socioeconômicas e digitais
- **Exploração personalizada** dos dados
- **Métricas em tempo real** baseadas nos filtros aplicados

### Análises Principais
1. **Perfil Demográfico**: Distribuição por gênero, cor/raça e localização
2. **Desigualdade Socioeconômica**: Correlação entre renda familiar e desempenho
3. **Desigualdade Digital**: Impacto do acesso a computadores e internet
4. **Desempenho Acadêmico**: Análise por disciplinas e áreas de conhecimento
5. **Frequência e Evasão**: Análise de faltantes por área

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit** - Interface web interativa
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas
- **Matplotlib & Seaborn** - Visualizações estáticas
- **Jupyter Notebook** - Análise exploratória de dados

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Execução

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd pi
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o Dashboard Streamlit
```bash
streamlit run dashboard_enem.py
```
O dashboard será aberto automaticamente no seu navegador em `http://localhost:8501`

### 4. Execute a Análise Exploratória (Opcional)
```bash
jupyter notebook dados.ipynb
```

## 📊 Dados Necessários

Certifique-se de que os seguintes arquivos estão presentes no diretório do projeto:
- `dados_sample.csv` - Dataset de amostra do ENEM (já incluído)

## 📊 Estrutura do Projeto

```
pi/
├── dashboard_enem.py          # Dashboard interativo principal
├── dados.ipynb               # Notebook de análise exploratória
├── dados_sample.csv          # Dataset do ENEM (amostra)
├── tests.py                  # Script para gerar amostra dos dados
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

## 📁 Dados

Os dados utilizados são uma amostra dos microdados oficiais do ENEM, disponibilizados pelo INEP. Para acessar o dataset completo:

[📥 Download dos Dados](https://drive.google.com/file/d/1euqNTyrhhbuLd6ZUkWxwPD0IyP5iaRCN/view?usp=drive_link)

## 🔍 Principais Insights Descobertos

### Desigualdade Socioeconômica
- **Correlação forte** entre renda familiar e desempenho acadêmico
- **Diferença significativa** nas notas entre faixas de renda
- **Impacto do acesso digital** no desempenho dos estudantes

### Desigualdade Digital
- **Acesso limitado** a computadores e internet em famílias de baixa renda
- **Diferença de desempenho** entre estudantes com e sem acesso digital
- **Necessidade de políticas** de inclusão digital na educação

### Desempenho por Disciplinas
- **Variações significativas** entre áreas de conhecimento
- **Diferenças de gênero** em disciplinas específicas
- **Padrões regionais** de desempenho

## 📈 Métricas Principais

- **3.300.000+** candidatos analisados
- **27 estados** brasileiros cobertos
- **5 disciplinas** principais analisadas
- **18 faixas** de renda familiar categorizadas
- **Análise de presença/ausência** por área de conhecimento

## 🎓 Aplicações Práticas

### Para Educadores
- Identificar grupos de estudantes em situação de vulnerabilidade
- Desenvolver estratégias pedagógicas direcionadas
- Acompanhar o impacto de políticas educacionais

### Para Gestores
- Planejamento de recursos educacionais
- Identificação de necessidades regionais
- Avaliação de programas de inclusão digital

### Para Pesquisadores
- Base de dados estruturada para análises acadêmicas
- Ferramentas de visualização para apresentações
- Metodologia replicável para outros estudos

## 🔧 Desenvolvimento

Este projeto foi desenvolvido como parte do Projeto Integrador em Computação IV, focando em:

- **Análise exploratória de dados** (EDA)
- **Visualização de dados** interativa
- **Desenvolvimento de dashboard** web
- **Aplicação de conceitos** de ciência de dados na educação
