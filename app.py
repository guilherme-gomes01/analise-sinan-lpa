import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_para_o_projeto_lpa' 

processed_df = None
agravos_disponiveis = []

UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'csv'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_column_names(df):
    cols = df.columns
    new_cols = []
    for col in cols:
        col = col.replace(' ', '_').replace('/', '_')
        col = col.replace('Ã§', 'c').replace('Ã£', 'a').replace('Ãª', 'e')
        col = col.replace('Ã¡', 'a').replace('Ã³', 'o').replace('Ãº', 'u')
        col = col.replace('Ã­', 'i')
        col = col.replace('Â', '').replace('(', '').replace(')', '')
        col = col.lower()
        new_cols.append(col)
    df.columns = new_cols
    return df

def process_dataframe(df):
    df_processed = df.copy()

    df_processed = df_processed.rename(columns={'ï»¿Doenca/Agravo': 'Doenca/Agravo'})
    df_processed = clean_column_names(df_processed)

    df_processed['idade_anos'] = pd.to_numeric(df_processed['idade_anos'], errors='coerce')
    df_processed['idade_anos'] = df_processed['idade_anos'].fillna(0).astype(int)

    df_processed['data'] = pd.to_datetime(df_processed['data'], errors='coerce', dayfirst=True)
    df_processed.dropna(subset=['data'], inplace=True)
    df_processed['ano'] = df_processed['data'].dt.year

    return df_processed

# Funcao para gerar e salvar um grafico como imagem base64
def generate_plot_base64(df_filtered, plot_type):
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(10, 6))

    current_agravo_name = df_filtered['doenca_agravo'].iloc[0] if not df_filtered.empty else "Agravo Desconhecido"

    if plot_type == 'sexo':
        dist_sexo = df_filtered['sexo'].value_counts()
        ax = dist_sexo.plot(kind='bar', color=['#6A05A1', '#FF6B6B', '#FFD166'])
        plt.title(f'Distribuição de Casos por Sexo ({current_agravo_name})', fontsize=16)
        plt.xlabel('Sexo', fontsize=12)
        plt.ylabel('Número de Casos', fontsize=12)
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7) 
        plt.tight_layout()
        # Adiciona labels
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10, color='black')

    elif plot_type == 'faixa_etaria':
        dist_faixa_etaria = df_filtered['faixa_etaria'].value_counts().sort_index()
        ax = dist_faixa_etaria.plot(kind='bar', color='#1ABC9C')
        plt.title(f'Distribuição de Casos por Faixa Etária ({current_agravo_name})', fontsize=16)
        plt.xlabel('Faixa Etária', fontsize=12)
        plt.ylabel('Número de Casos', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        # Adiciona labels
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10, color='black')

    elif plot_type == 'ranking_municipio':
        if 'municipio' in df_filtered.columns:
            top_municipios = df_filtered['municipio'].value_counts().head(10)
            ax = top_municipios.sort_values(ascending=True).plot(kind='barh', color='#3498DB')
            plt.title(f'Top 10 Municípios com Casos ({current_agravo_name})', fontsize=16)
            plt.xlabel('Número de Casos', fontsize=12)
            plt.ylabel('Município', fontsize=12)
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            # Adiciona labels
            for p in ax.patches:
                ax.annotate(f'{int(p.get_width())}', (p.get_width(), p.get_y() + p.get_height() / 2.),
                            ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=10, color='black')
        else:
            plt.text(0.5, 0.5, 'Coluna "municipio" não encontrada.', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
            plt.axis('off') 

    elif plot_type == 'evolucao_anual':
        evolucao_anual = df_filtered['ano'].value_counts().sort_index()
        ax = evolucao_anual.plot(kind='line', marker='o', color='#E74C3C', linewidth=2)
        plt.title(f'Evolução do Número de Casos por Ano ({current_agravo_name})', fontsize=16)
        plt.xlabel('Ano', fontsize=12)
        plt.ylabel('Número de Casos', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        # Adiciona labels nos pontos da linha
        for x, y in zip(evolucao_anual.index, evolucao_anual.values):
            ax.annotate(f'{int(y)}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10, color='black')

    else:
        plt.text(0.5, 0.5, 'Gráfico não especificado.', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.axis('off')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()
    return img_base64

@app.route('/')
def index():
    global processed_df, agravos_disponiveis
    if 'file_uploaded' not in session:
        processed_df = None
        agravos_disponiveis = []
    
    # Adiciona flag para indicar se há gráficos para exibir
    show_charts = False
    if request.args.get('show_charts') == 'true':
        show_charts = True

    return render_template('index.html', 
                           agravos=agravos_disponiveis, 
                           file_uploaded=(processed_df is not None),
                           show_charts=show_charts) # Passa a flag para o template

@app.route('/upload_file', methods=['POST'])
def upload_file():
    global processed_df, agravos_disponiveis
    
    if 'file' not in request.files:
        return render_template('index.html', agravos=[], error="Nenhum arquivo enviado.")
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', agravos=[], error="Nenhum arquivo selecionado.")
    
    if file and allowed_file(file.filename):
        try:
            file_stream = io.StringIO(file.stream.read().decode('latin1'))
            df_raw = pd.read_csv(file_stream, sep=';', low_memory=False)
            
            processed_df = process_dataframe(df_raw)
            agravos_disponiveis = sorted(processed_df['doenca_agravo'].unique().tolist())
            session['file_uploaded'] = True

            # Redireciona para a página principal com uma mensagem de sucesso
            return render_template('index.html', 
                                   agravos=agravos_disponiveis, 
                                   file_uploaded=True,
                                   success_message="Arquivo carregado e processado com sucesso! Selecione um agravo.")
        except Exception as e:
            # Captura a exceção e retorna uma mensagem de erro
            error_message = f"Erro ao processar o arquivo: {e}. Verifique a estrutura do CSV (separador, codificação, nomes de colunas)."
            return render_template('index.html', agravos=[], error=error_message)
    else:
        return render_template('index.html', agravos=[], error="Tipo de arquivo não permitido. Apenas CSVs são aceitos.")

@app.route('/analisar', methods=['POST'])
def analisar():
    global processed_df, agravos_disponiveis

    if processed_df is None or processed_df.empty:
        return render_template('index.html', agravos=agravos_disponiveis, error="Por favor, primeiro faça o upload e processe um arquivo CSV.")

    selected_agravo = request.form.get('agravo')

    if not selected_agravo:
        return render_template('index.html', agravos=agravos_disponiveis, error="Por favor, selecione um agravo.")

    df_agravo = processed_df[processed_df['doenca_agravo'] == selected_agravo].copy()

    if df_agravo.empty:
        return render_template('index.html', agravos=agravos_disponiveis, selected_agravo=selected_agravo, error=f"Nenhum dado encontrado para '{selected_agravo}'.")

    plot_sexo_base64 = generate_plot_base64(df_agravo, 'sexo')
    plot_faixa_etaria_base64 = generate_plot_base64(df_agravo, 'faixa_etaria')
    plot_ranking_municipio_base64 = generate_plot_base64(df_agravo, 'ranking_municipio')
    plot_evolucao_anual_base64 = generate_plot_base64(df_agravo, 'evolucao_anual')

    return render_template('index.html',
                           agravos=agravos_disponiveis,
                           selected_agravo=selected_agravo,
                           plot_sexo=plot_sexo_base64,
                           plot_faixa_etaria=plot_faixa_etaria_base64,
                           plot_ranking_municipio=plot_ranking_municipio_base64,
                           plot_evolucao_anual=plot_evolucao_anual_base64,
                           file_uploaded=True,
                           show_charts=True)

if __name__ == '__main__':
    app.run(debug=True)