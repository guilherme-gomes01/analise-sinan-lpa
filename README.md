# Repositório analise-sinan-lpa
# Análise e Visualização de Dados de Saúde Pública (SINAN)
## 🎯 Visão Geral do Projeto
Este projeto consiste em uma aplicação web interativa desenvolvida em Python para a análise e visualização de dados de saúde pública do Sistema de Informação de Agravos de Notificação (SINAN) da FVS-RCP. A aplicação permite aos usuários fazer o upload de arquivos CSV contendo dados de notificação de agravos (como Tuberculose, Dengue, etc.), processar esses dados e gerar gráficos dinâmicos para análise epidemiológica.

A aplicação foi desenvolvida como projeto final da disciplina de Linguagem de Programação Avançada (LPA) no curso de Análise e Desenvolvimento de Sistemas do IFAM.

## 🚀 Funcionalidades
* Upload e Processamento de CSVs: Capacidade de carregar arquivos CSV atualizados, incluindo tratamento de dados, limpeza de nomes de colunas e conversão de tipos (ex: idade e data).

* Filtragem por Agravo: Seleção dinâmica do agravo de interesse para análise.

* Visualização de Dados: Geração de gráficos para diversas análises, incluindo:
    - Distribuição de casos por sexo.

    - Distribuição de casos por faixa etária.

    - Ranking dos 10 municípios com maior número de casos.

    - Evolução do número de casos por ano.

* Gráficos Aprimorados: Gráficos com labels numéricas (para barras e pontos) para facilitar a leitura dos dados.

* Indicador de Carregamento (Spinner): Feedback visual durante o processamento de arquivos grandes e a geração de gráficos.

## 💻 Tecnologias Utilizadas
Python (3.x)

Flask: Framework web para o backend e roteamento.

Pandas: Essencial para a leitura, manipulação, limpeza e agregação de dados.

Matplotlib: Utilizada para a geração dos gráficos de visualização, convertidos para Base64 para exibição no frontend.

HTML, CSS e JavaScript: Para a interface do usuário e o controle do spinner de carregamento.

## 🔧 Configuração e Instalação
Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

1. Pré-requisitos
Certifique-se de ter o Python 3.x e o pip instalados.

2. Clonar o Repositório

3. Navegar para o diretório e instalar as dependências:

```bash
pip install Flask pandas matplotlib numpy
```

## ✔️ Executando a Aplicação
Inicie o servidor Flask a partir da raiz do projeto:
```bash
python app.py
```

Abra seu navegador web e acesse: http://127.0.0.1:5000/

## 👌 Instruções de Uso

Vá ao site: https://office365prodam-my.sharepoint.com/:f:/g/personal/sass_fvs_am_gov_br/Ev52wq74EutIkt47OJAFa9IBGe9S9LcP8LA4WGFjd8yGjw e baixe o arquivo csv.

Upload do Arquivo CSV: Na página inicial, localize a seção de upload e selecione o arquivo CSV de dados do SINAN (com a estrutura de colunas esperada).

Clique em "Upload e Processar". O sistema irá carregar, limpar os dados e extrair a lista de agravos disponíveis.

Analisar o Agravo: Selecione o agravo desejado na lista suspensa (ex: "Tuberculose") e clique em "Analisar Agravo".

Os gráficos de análise serão exibidos dinamicamente na página.

## 📦 Estrutura do Projeto
```bash
analise-sinan-lpa/
├── app.py          # Código principal da aplicação Flask, lógica de dados e geração de gráficos
└── templates/
    └── index.html  # Interface de usuário (HTML, CSS, JS para o spinner)
```
## ✨ Contribuição
Contribuições são bem-vindas. Por favor, sinta-se à vontade para abrir issues ou pull requests.