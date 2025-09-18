import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- Config & Theming --------------------
st.set_page_config(layout="wide", page_title="Dashboard de Insights do ENEM", page_icon="📊")

# Global Plotly style
PLOTLY_TEMPLATE = "plotly_white"
COLOR_SEQUENCE = px.colors.sequential.Blues + px.colors.sequential.Greens

# Subtle CSS polish
st.markdown(
    """
    <style>
      .main > div { padding-top: 1rem; }
      h1, h2, h3 { font-weight: 700; letter-spacing: .2px; }
      .big-subtitle { color: #4b5563; font-size: 1.05rem; line-height: 1.6; }
      .section-divider { height: 1px; background: linear-gradient(90deg, #e5e7eb, #cbd5e1, #e5e7eb); margin: 1.25rem 0 0.75rem; }
      .metric-row .stMetric { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px; }
      .stSelectbox label { font-weight: 600; color: #374151; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Data --------------------
df = pd.read_csv('dados_sample.csv', sep=';', encoding='ISO-8859-1')

# Criar coluna de nota média a partir das notas das provas
component_scores = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
# Garantir que as colunas existem antes de calcular
existing_scores = [col for col in component_scores if col in df.columns]
if existing_scores:
    for col in existing_scores:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['NOTA_MEDIA'] = df[existing_scores].mean(axis=1, skipna=True)

# Mapear sexo para rótulos legíveis
mapa_sexo = {'M': 'Masculino', 'F': 'Feminino'}
if 'TP_SEXO' in df.columns:
    df['SEXO'] = df['TP_SEXO'].map(mapa_sexo).fillna(df['TP_SEXO'])

# -------------------- Cabeçalho --------------------
st.title("Decodificando o ENEM: Dos Dados Brutos às Estratégias Pedagógicas")
st.markdown(
    """
    <div class="big-subtitle">Esta plataforma interativa, resultado do Projeto Integrador em Computação IV,
    permite a exploração dos microdados do ENEM para extrair insights valiosos sobre o desempenho e o perfil dos estudantes.</div>
    """,
    unsafe_allow_html=True,
)

# Métricas principais
col1, col2 = st.columns(2, gap="large")
with col1:
    st.metric("Candidatos Analisados", "3.300.000+", help="Total aproximado de participantes considerados")
with col2:
    st.metric("Objetivo do Projeto", "Democratizar o acesso aos dados")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------- Filtros (Sidebar) --------------------
st.sidebar.header("Filtros Globais")
uf_selecionada = st.sidebar.selectbox(
    "Estado (UF)", options=['Todos'] + sorted(df['SG_UF_PROVA'].dropna().unique().tolist())
)

# Mapeamento dos códigos de cor/raça para nomes legíveis (usado mais abaixo)
mapa_cor_raca = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena',
    6: 'Não dispõe'
}

if uf_selecionada != 'Todos':
    df_filtrado = df[df['SG_UF_PROVA'] == uf_selecionada].copy()
else:
    df_filtrado = df.copy()

# -------------------- 1. O Problema --------------------
st.header("O Tesouro Escondido nos Dados do ENEM")
st.markdown(
    "> <b>Problema:</b> Professores e gestores não possuem ferramentas acessíveis para explorar a imensa base de dados do ENEM, dificultando a extração de informações para embasar estratégias pedagógicas.",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------- 2. Quem são os Candidatos? --------------------
st.header("Um Retrato do Futuro do Brasil")

col1, col2 = st.columns(2, gap="large")

# Gráfico de Gênero - Barras
st.info("📊 **Distribuição por Gênero**: Este gráfico mostra a distribuição dos candidatos por gênero. Permite identificar se há equilíbrio entre candidatos masculinos e femininos na região selecionada.")
df_sexo = df_filtrado['SEXO'].value_counts(dropna=False).reset_index()
df_sexo.columns = ['SEXO', 'Quantidade']
fig_sexo = px.bar(
    df_sexo,
    x='SEXO',
    y='Quantidade',
    text='Quantidade',
    title=f'Distribuição por Gênero em {uf_selecionada}',
    color='SEXO',
    template=PLOTLY_TEMPLATE,
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_sexo.update_traces(textposition='outside')
fig_sexo.update_layout(showlegend=False, xaxis_title='', yaxis_title='Quantidade')
col1.plotly_chart(fig_sexo, use_container_width=True)

# Gráfico de Raça/Cor - Barras
if 'TP_COR_RACA' in df_filtrado.columns:
    st.info("🌍 **Distribuição por Cor/Raça**: Este gráfico mostra a distribuição dos candidatos por cor/raça. É importante para identificar a diversidade étnica dos participantes e possíveis desigualdades de acesso ao ensino superior.")
    df_filtrado['COR/RACA'] = df_filtrado['TP_COR_RACA'].map(mapa_cor_raca)
    df_raca = df_filtrado['COR/RACA'].value_counts(dropna=False).reset_index()
    df_raca.columns = ['COR/RACA', 'Quantidade']
    fig_raca = px.bar(
        df_raca,
        x='COR/RACA',
        y='Quantidade',
        text='Quantidade',
        title=f'Distribuição por Cor/Raça em {uf_selecionada}',
        color='COR/RACA',
        color_discrete_sequence=px.colors.qualitative.Set3,
        template=PLOTLY_TEMPLATE,
    )
    fig_raca.update_traces(textposition='outside')
    fig_raca.update_layout(showlegend=False, xaxis_title='', yaxis_title='Quantidade')
    col2.plotly_chart(fig_raca, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------- 3. A Desigualdade nos Números --------------------
st.header("Onde o Desempenho Encontra a Desigualdade")

ordem_renda = [
    'Nenhuma Renda', 'Até R$ 1.100,00', 'De R$ 1.100,01 até R$ 1.650,00',
    'De R$ 1.650,01 até R$ 2.200,00', 'De R$ 2.200,01 até R$ 2.750,00',
    'De R$ 2.750,01 até R$ 3.300,00', 'De R$ 3.300,01 até R$ 3.850,00',
    'De R$ 3.850,01 até R$ 4.400,00', 'De R$ 4.400,01 até R$ 5.500,00',
    'De R$ 5.500,01 até R$ 6.600,00', 'De R$ 6.600,01 até R$ 7.700,00',
    'De R$ 7.700,01 até R$ 8.800,00', 'De R$ 8.800,01 até R$ 9.900,00',
    'De R$ 9.900,01 até R$ 11.000,00', 'De R$ 11.000,01 até R$ 13.200,00',
    'De R$ 13.200,01 até R$ 16.500,00', 'De R$ 16.500,01 até R$ 22.000,00',
    'Acima de R$ 22.000,00'
]

# Ordenar as categorias de renda para o gráfico
map_renda = {
    'A': 'Nenhuma Renda',
    'B': 'Até R$ 1.100,00',
    'C': 'De R$ 1.100,01 até R$ 1.650,00',
    'D': 'De R$ 1.650,01 até R$ 2.200,00',
    'E': 'De R$ 2.200,01 até R$ 2.750,00',
    'F': 'De R$ 2.750,01 até R$ 3.300,00',
    'G': 'De R$ 3.300,01 até R$ 3.850,00',
    'H': 'De R$ 3.850,01 até R$ 4.400,00',
    'I': 'De R$ 4.400,01 até R$ 5.500,00',
    'J': 'De R$ 5.500,01 até R$ 6.600,00',
    'K': 'De R$ 6.600,01 até R$ 7.700,00',
    'L': 'De R$ 7.700,01 até R$ 8.800,00',
    'M': 'De R$ 8.800,01 até R$ 9.900,00',
    'N': 'De R$ 9.900,01 até R$ 11.000,00',
    'O': 'De R$ 11.000,01 até R$ 13.200,00',
    'P': 'De R$ 13.200,01 até R$ 16.500,00',
    'Q': 'De R$ 16.500,01 até R$ 22.000,00',
    'R': 'Acima de R$ 22.000,00'
}


if 'Q006' in df.columns:
    # Criar coluna global de renda categorizada sem sobrescrever Q006
    df['RENDA'] = df['Q006'].map(map_renda).fillna(df['Q006'])
    df['RENDA'] = pd.Categorical(df['RENDA'], categories=ordem_renda, ordered=True)

    # Aplicar o mesmo recorte por UF
    df_filtrado['RENDA'] = df_filtrado['Q006'].map(map_renda).fillna(df_filtrado['Q006'])
    df_filtrado['RENDA'] = pd.Categorical(df_filtrado['RENDA'], categories=ordem_renda, ordered=True)

    # Gráfico de linha da mediana da nota média por faixa de renda
    medianas_renda = df_filtrado.groupby('RENDA', observed=True)['NOTA_MEDIA'].median()
    df_line = medianas_renda.reset_index()
    df_line.columns = ['RENDA', 'MEDIANA_NOTA_MEDIA']
    if df_line.empty:
        st.warning('Sem dados suficientes para calcular a mediana por faixa de renda neste filtro.')
    else:
        st.info("📈 **Mediana da Nota Média por Renda Familiar**: Este gráfico de linha mostra a relação entre renda familiar e desempenho acadêmico. A tendência crescente indica desigualdade educacional, onde estudantes de famílias com maior renda tendem a ter melhor desempenho no ENEM.")
        fig_renda = px.line(
            df_line.sort_values('RENDA'),
            x='RENDA',
            y='MEDIANA_NOTA_MEDIA',
            markers=True,
            title='Mediana da Nota Média por Renda Familiar',
            labels={'RENDA': 'Faixa de Renda Familiar', 'MEDIANA_NOTA_MEDIA': 'Mediana da Nota Média'},
            category_orders={'RENDA': ordem_renda},
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=["#2563eb"],
        )
        fig_renda.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_renda, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------- 3.1. Desigualdade Digital --------------------
st.header("A Desigualdade Digital: O Abismo Tecnológico na Educação")

# Mapeamento das respostas para Q024 (computador) e Q025 (internet)
mapa_computador = {
    'A': 'Não',
    'B': 'Sim, um',
    'C': 'Sim, dois', 
    'D': 'Sim, três',
    'E': 'Sim, quatro ou mais'
}

mapa_internet = {
    'A': 'Não',
    'B': 'Sim'
}

# Verificar se as colunas existem
if 'Q024' in df_filtrado.columns and 'Q025' in df_filtrado.columns:
    # Criar colunas legíveis
    df_filtrado['ACESSO_COMPUTADOR'] = df_filtrado['Q024'].map(mapa_computador).fillna(df_filtrado['Q024'])
    df_filtrado['ACESSO_INTERNET'] = df_filtrado['Q025'].map(mapa_internet).fillna(df_filtrado['Q025'])
    
    col1, col2 = st.columns(2, gap="large")
    
    # Gráfico de acesso a computadores
    with col1:
        st.info("💻 **Acesso a Computadores**: Este gráfico mostra quantos candidatos têm acesso a computadores em casa. O acesso à tecnologia é fundamental para o aprendizado e pode impactar significativamente o desempenho acadêmico.")
        df_computador = df_filtrado['ACESSO_COMPUTADOR'].value_counts(dropna=False).reset_index()
        df_computador.columns = ['ACESSO_COMPUTADOR', 'Quantidade']
        
        # Ordenar por quantidade de computadores
        ordem_computador = ['Não', 'Sim, um', 'Sim, dois', 'Sim, três', 'Sim, quatro ou mais']
        df_computador['ACESSO_COMPUTADOR'] = pd.Categorical(df_computador['ACESSO_COMPUTADOR'], 
                                                           categories=ordem_computador, ordered=True)
        df_computador = df_computador.sort_values('ACESSO_COMPUTADOR')
        
        fig_computador = px.bar(
            df_computador,
            x='ACESSO_COMPUTADOR',
            y='Quantidade',
            text='Quantidade',
            title=f'Acesso a Computadores em {uf_selecionada}',
            color='ACESSO_COMPUTADOR',
            color_discrete_sequence=px.colors.qualitative.Set3,
            template=PLOTLY_TEMPLATE,
        )
        fig_computador.update_traces(textposition='outside')
        fig_computador.update_layout(showlegend=False, xaxis_title='', yaxis_title='Quantidade')
        fig_computador.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_computador, use_container_width=True)
    
    # Gráfico de acesso à internet
    with col2:
        st.info("🌐 **Acesso à Internet**: Este gráfico de pizza mostra a proporção de candidatos que têm acesso à internet em casa. A conectividade é essencial para pesquisa, estudos online e acesso a recursos educacionais digitais.")
        df_internet = df_filtrado['ACESSO_INTERNET'].value_counts(dropna=False).reset_index()
        df_internet.columns = ['ACESSO_INTERNET', 'Quantidade']
        
        fig_internet = px.pie(
            df_internet,
            values='Quantidade',
            names='ACESSO_INTERNET',
            title=f'Acesso à Internet em {uf_selecionada}',
            color_discrete_sequence=px.colors.qualitative.Set2,
            template=PLOTLY_TEMPLATE,
        )
        fig_internet.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_internet, use_container_width=True)
    
    # Análise da relação entre acesso digital e renda
    st.subheader("Acesso Digital vs. Renda Familiar")
    
    if 'RENDA' in df_filtrado.columns:
        # Criar tabela de contingência para computadores
        tabela_computador_renda = pd.crosstab(
            df_filtrado['RENDA'], 
            df_filtrado['ACESSO_COMPUTADOR'], 
            normalize='index'
        ) * 100
        
        # Filtrar apenas "Não" e "Sim, um" para simplificar a visualização
        colunas_simples = ['Não', 'Sim, um']
        colunas_disponiveis = [col for col in colunas_simples if col in tabela_computador_renda.columns]
        
        if colunas_disponiveis:
            st.info("🔥 **Mapa de Calor - Acesso a Computadores por Renda**: Este mapa de calor mostra a relação entre renda familiar e acesso a computadores. Cores mais escuras indicam maior percentual de acesso, revelando como a desigualdade econômica se reflete no acesso à tecnologia.")
            tabela_simples = tabela_computador_renda[colunas_disponiveis]
            
            fig_heatmap = px.imshow(
                tabela_simples.T,
                title='Percentual de Acesso a Computadores por Faixa de Renda',
                labels=dict(x="Faixa de Renda", y="Acesso a Computadores", color="Percentual (%)"),
                color_continuous_scale='Blues',
                template=PLOTLY_TEMPLATE,
                aspect="auto"
            )
            fig_heatmap.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Análise do impacto do acesso digital no desempenho
    st.subheader("Impacto do Acesso Digital no Desempenho Acadêmico")
    
    # Box plot: Nota média por acesso à internet
    if 'NOTA_MEDIA' in df_filtrado.columns:
        st.info("📊 **Desempenho Acadêmico por Acesso à Internet**: Este gráfico de caixa (box plot) compara o desempenho acadêmico entre estudantes com e sem acesso à internet. Mostra a distribuição das notas, incluindo mediana, quartis e valores extremos, evidenciando o impacto da conectividade no aprendizado.")
        fig_digital_performance = px.box(
            df_filtrado,
            x='ACESSO_INTERNET',
            y='NOTA_MEDIA',
            title='Desempenho Acadêmico por Acesso à Internet',
            labels={'ACESSO_INTERNET': 'Acesso à Internet', 'NOTA_MEDIA': 'Nota Média'},
            color='ACESSO_INTERNET',
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig_digital_performance, use_container_width=True)
    
    # Estatísticas resumidas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sem_internet = (df_filtrado['ACESSO_INTERNET'] == 'Não').sum()
        total = len(df_filtrado)
        perc_sem_internet = (sem_internet / total * 100) if total > 0 else 0
        st.metric("Sem Acesso à Internet", f"{perc_sem_internet:.1f}%")
    
    with col2:
        sem_computador = (df_filtrado['ACESSO_COMPUTADOR'] == 'Não').sum()
        perc_sem_computador = (sem_computador / total * 100) if total > 0 else 0
        st.metric("Sem Computador", f"{perc_sem_computador:.1f}%")
    
    with col3:
        if 'NOTA_MEDIA' in df_filtrado.columns:
            nota_com_internet = df_filtrado[df_filtrado['ACESSO_INTERNET'] == 'Sim']['NOTA_MEDIA'].mean()
            nota_sem_internet = df_filtrado[df_filtrado['ACESSO_INTERNET'] == 'Não']['NOTA_MEDIA'].mean()
            diferenca = nota_com_internet - nota_sem_internet
            st.metric("Diferença de Nota (Com vs Sem Internet)", f"{diferenca:.1f}")

else:
    st.warning("Dados de acesso digital (Q024 e Q025) não disponíveis no dataset atual.")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------- 4. Desempenho Acadêmico --------------------
st.header("Análise das Disciplínas: Forças e Fraquezas")
if 'NU_NOTA_MT' in df_filtrado.columns and 'SEXO' in df_filtrado.columns:
    st.info("📚 **Desempenho em Matemática por Gênero**: Este gráfico de caixa compara o desempenho em Matemática entre gêneros. Mostra a distribuição das notas, mediana e quartis, permitindo identificar se há diferenças significativas no desempenho entre candidatos masculinos e femininos nesta disciplina.")
    fig_mt_sexo = px.box(
        df_filtrado,
        x='SEXO', y='NU_NOTA_MT',
        title='Desempenho em Matemática por Gênero',
        labels={'SEXO': 'Gênero', 'NU_NOTA_MT': 'Nota de Matemática'},
        color='SEXO',
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig_mt_sexo, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------- 5. A Solução (Exploração) --------------------
st.header("Frequência: Faltantes por Área")

# Mapeia colunas de presença do ENEM para nomes legíveis das áreas
presence_cols = {
    'TP_PRESENCA_CN': 'Ciências da Natureza',
    'TP_PRESENCA_CH': 'Ciências Humanas',
    'TP_PRESENCA_LC': 'Linguagens e Códigos',
    'TP_PRESENCA_MT': 'Matemática',
}

available_presence = [(col, label) for col, label in presence_cols.items() if col in df_filtrado.columns]

if not available_presence:
    st.info("Colunas de presença por área não foram encontradas no conjunto atual.")
else:
    stats_faltas = []
    for col, label in available_presence:
        serie = pd.to_numeric(df_filtrado[col], errors='coerce')
        total_validos = serie.notna().sum()
        num_faltantes = (serie == 0).sum()
        perc_faltantes = (num_faltantes / total_validos * 100) if total_validos > 0 else 0
        stats_faltas.append({
            'Área': label,
            'Faltantes': int(num_faltantes),
            'Percentual': perc_faltantes,
        })

    df_faltas = pd.DataFrame(stats_faltas).sort_values('Faltantes', ascending=False)

    c1, c2 = st.columns([2, 1], gap="large")
    with c1:
        st.info("📉 **Alunos Faltantes por Área**: Este gráfico mostra quantos candidatos faltaram em cada área de conhecimento do ENEM. A análise de faltas é importante para identificar padrões de abandono e áreas onde os estudantes podem ter mais dificuldades ou desinteresse.")
        fig_faltas = px.bar(
            df_faltas,
            x='Área',
            y='Faltantes',
            text='Faltantes',
            title=f'Alunos faltantes por área em {uf_selecionada}',
            template=PLOTLY_TEMPLATE,
            color='Área',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_faltas.update_traces(textposition='outside')
        fig_faltas.update_layout(showlegend=False, yaxis_title='Quantidade', xaxis_title='')
        st.plotly_chart(fig_faltas, use_container_width=True)

    with c2:
        df_display = df_faltas.copy()
        df_display['Percentual'] = df_display['Percentual'].map(lambda v: f"{v:.1f}%")
        st.dataframe(df_display, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------- 5. A Solução (Exploração) --------------------
st.header("Faça sua Própria Análise")
st.markdown("Use os filtros abaixo para explorar os dados e encontrar seus próprios insights. Selecione 'Todos' para incluir todas as opções de uma categoria.")

col1, col2, col3 = st.columns(3, gap="large")

# Preparar opções para os filtros
opcoes_uf = ['Todos'] + sorted(df['SG_UF_PROVA'].dropna().unique().tolist())
opcoes_renda = ['Todos'] + ordem_renda
opcoes_sexo = ['Todos'] + sorted(df['SEXO'].dropna().unique().tolist())

with col1:
    uf_exp = st.selectbox(
        "Estado", 
        options=opcoes_uf, 
        index=0,
        key="uf_exp",
        help="Selecione 'Todos' para incluir todos os estados ou escolha um estado específico"
    )
with col2:
    renda_exp = st.selectbox(
        "Renda", 
        options=opcoes_renda, 
        index=0,
        key="renda_exp",
        help="Selecione 'Todos' para incluir todas as faixas de renda ou escolha uma faixa específica"
    )
with col3:
    sexo_exp = st.selectbox(
        "Gênero", 
        options=opcoes_sexo, 
        index=0,
        key="sexo_exp",
        help="Selecione 'Todos' para incluir ambos os gêneros ou escolha um gênero específico"
    )

# Aplicar filtros
col_renda = 'RENDA' if 'RENDA' in df.columns else 'Q006'

# Criar máscara para filtros
if uf_exp == 'Todos':
    mask_uf = pd.Series([True] * len(df), index=df.index)
else:
    mask_uf = df['SG_UF_PROVA'] == uf_exp

if renda_exp == 'Todos':
    mask_renda = pd.Series([True] * len(df), index=df.index)
else:
    mask_renda = df[col_renda] == renda_exp

if sexo_exp == 'Todos':
    mask_sexo = pd.Series([True] * len(df), index=df.index)
else:
    mask_sexo = df['SEXO'] == sexo_exp

# Aplicar todas as máscaras
df_exploracao = df[mask_uf & mask_renda & mask_sexo]

if df_exploracao.empty:
    st.warning("Nenhum dado encontrado para a combinação de filtros selecionada.")
else:
    # Mostrar informações sobre o grupo selecionado
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Registros Selecionados", f"{len(df_exploracao):,}")
    
    with col_info2:
        nota_media_filtrada = df_exploracao['NOTA_MEDIA'].mean()
        st.metric("Nota Média", f"{nota_media_filtrada:.2f}")
    
    with col_info3:
        if 'NOTA_MEDIA' in df_exploracao.columns:
            nota_mediana = df_exploracao['NOTA_MEDIA'].median()
            st.metric("Nota Mediana", f"{nota_mediana:.2f}")
    
    # Mostrar resumo dos filtros aplicados
    st.markdown("**Filtros Aplicados:**")
    filtros_info = []
    if uf_exp != 'Todos':
        filtros_info.append(f"Estado: {uf_exp}")
    if renda_exp != 'Todos':
        filtros_info.append(f"Renda: {renda_exp}")
    if sexo_exp != 'Todos':
        filtros_info.append(f"Gênero: {sexo_exp}")
    
    if filtros_info:
        st.info(" | ".join(filtros_info))
    else:
        st.info("Todos os dados incluídos (nenhum filtro específico aplicado)")
    # Gráfico 1: Distribuição das Notas por Área de Conhecimento
    if all(col in df_exploracao.columns for col in ['NOTA_CN', 'NOTA_CH', 'NOTA_LC', 'NOTA_MT']):
        st.info("📊 **Distribuição das Notas por Área de Conhecimento**: Este gráfico de caixa mostra a distribuição das notas em cada área de conhecimento do ENEM para o grupo selecionado. Permite comparar o desempenho entre as diferentes disciplinas e identificar quais áreas têm maior variabilidade nas notas.")
        notas_areas = {
            'Ciências da Natureza': df_exploracao['NOTA_CN'].dropna(),
            'Ciências Humanas': df_exploracao['NOTA_CH'].dropna(),
            'Linguagens': df_exploracao['NOTA_LC'].dropna(),
            'Matemática': df_exploracao['NOTA_MT'].dropna()
        }
        df_notas_areas = pd.DataFrame({
            'Área': [],
            'Nota': []
        })
        for area, notas in notas_areas.items():
            temp_df = pd.DataFrame({'Área': area, 'Nota': notas})
            df_notas_areas = pd.concat([df_notas_areas, temp_df], ignore_index=True)
        fig_box = px.box(
            df_notas_areas,
            x='Área',
            y='Nota',
            color='Área',
            title='Distribuição das Notas por Área de Conhecimento',
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Gráfico 2: Histograma da Nota Média
    if 'NOTA_MEDIA' in df_exploracao.columns:
        st.info("📈 **Histograma da Nota Média**: Este histograma mostra a distribuição das notas médias do grupo selecionado. Permite visualizar a concentração de notas em diferentes faixas e identificar se a distribuição é normal, assimétrica ou tem outras características importantes.")
        df_exploracao['NOTA_MEDIA'] = pd.to_numeric(df_exploracao['NOTA_MEDIA'], errors='coerce')
    fig_hist = px.histogram(
        df_exploracao,
        x='NOTA_MEDIA',
        nbins=20,
        title='Histograma da Nota Média do Grupo Selecionado',
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Gráfico 3: Proporção de Presença/Falta por área
    presence_cols_local = {
        'TP_PRESENCA_CN': 'Ciências da Natureza',
        'TP_PRESENCA_CH': 'Ciências Humanas',
        'TP_PRESENCA_LC': 'Linguagens e Códigos',
        'TP_PRESENCA_MT': 'Matemática',
    }
    available_presence_local = [col for col in presence_cols_local.keys() if col in df_exploracao.columns]
    if not available_presence_local:
        st.info('Não há informações de presença/falta para este recorte.')
    else:
        col_presenca = st.selectbox(
            'Área para analisar presença/falta',
            options=available_presence_local,
            format_func=lambda c: presence_cols_local.get(c, c),
            key='area_presenca_exp'
        )
        serie_presenca = pd.to_numeric(df_exploracao[col_presenca], errors='coerce')
        mapa_presenca = {0: 'Faltou', 1: 'Presente', 2: 'Eliminado', 3: 'Anulado'}
        presenca_counts = serie_presenca.map(mapa_presenca).value_counts(dropna=True).reset_index()
        presenca_counts.columns = ['Situação', 'Quantidade']
        st.info("📋 **Proporção de Presença/Falta**: Este gráfico mostra a distribuição dos candidatos por situação de presença na área selecionada. Inclui presentes, faltantes, eliminados e anulados, permitindo analisar padrões de abandono e participação efetiva no exame.")
        fig_presenca = px.bar(
            presenca_counts,
            x='Situação',
            y='Quantidade',
            text='Quantidade',
            title=f"Proporção de Presença/Falta - {presence_cols_local.get(col_presenca, col_presenca)}",
            template=PLOTLY_TEMPLATE,
            color='Situação',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_presenca.update_traces(textposition='outside')
        fig_presenca.update_layout(showlegend=False, xaxis_title='', yaxis_title='Quantidade')
        st.plotly_chart(fig_presenca, use_container_width=True)