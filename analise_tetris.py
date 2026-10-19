
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# OPERAÇÃO TETRIS - ANÁLISE DE DADOS
# ==========================================

ARQUIVO = "operacao_tetris_base_jogos.csv"
ARQUIVO_TRATADO = "operacao_tetris_base_jogos_tratado.csv"

# Verificar se o arquivo existe
if not Path(ARQUIVO).exists():
    print("ERRO: CSV não encontrado.")
    print("Coloque o arquivo na mesma pasta do código.")
    raise SystemExit

# ==========================================
# ETAPA 3 - LEITURA E EXPLORAÇÃO
# ==========================================

df_original = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

print("\n=== PRIMEIRAS LINHAS ===")
print(df_original.head())

print("\n=== DIMENSÕES DA BASE ===")
print(df_original.shape)

print("\n=== NOMES DAS COLUNAS ===")
print(df_original.columns.tolist())

print("\n=== INFORMAÇÕES GERAIS ===")
df_original.info()

print("\n=== RESUMO ESTATÍSTICO ===")
print(df_original.describe(include="all"))

print("\n=== VALORES AUSENTES ===")
print(df_original.isna().sum())

print("\n=== LINHAS DUPLICADAS ===")
print(df_original.duplicated().sum())

print("\n=== JOGOS POR GÊNERO ===")
print(df_original["Gênero"].value_counts())

print("\n=== JOGOS POR PLATAFORMA ===")
print(df_original["Plataforma"].value_counts())

# Exemplo de consulta filtrada
print("\n=== JOGOS LANÇADOS EM 2010 ===")
print(
    df_original[
        df_original["Ano de Lançamento"] == 2010
    ][["Nome do Jogo", "Plataforma", "Gênero"]]
)

# ==========================================
# ETAPA 4 - LIMPEZA DOS DADOS
# ==========================================

df = df_original.copy()

# Remover espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Remover espaços extras nos campos de texto
for coluna in df.select_dtypes(include="object").columns:
    df[coluna] = df[coluna].str.strip()

# Padronizar nomes das plataformas e gêneros
df["Plataforma"] = df["Plataforma"].str.upper()
df["Gênero"] = df["Gênero"].str.strip().str.title()

# Converter colunas numéricas
colunas_numericas = [
    "Ano de Lançamento",
    "Vendas Globais (milhões)",
    "Avaliação"
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(
        df[coluna], errors="coerce"
    )

# Identificar anos inválidos
ano_atual = pd.Timestamp.now().year

anos_invalidos = (
    (df["Ano de Lançamento"] < 1970)
    | (df["Ano de Lançamento"] > ano_atual)
)

df.loc[anos_invalidos, "Ano de Lançamento"] = float("nan")

# Vendas negativas são inválidas
df.loc[
    df["Vendas Globais (milhões)"] < 0,
    "Vendas Globais (milhões)"
] = float("nan")

# Avaliações precisam estar entre 0 e 100
df.loc[
    (df["Avaliação"] < 0)
    | (df["Avaliação"] > 100),
    "Avaliação"
] = float("nan")

# Remover somente linhas completamente duplicadas
df = df.drop_duplicates()

# Não preencher valores históricos desconhecidos
# Salvar em outro arquivo, preservando o original
df.to_csv(
    ARQUIVO_TRATADO,
    index=False,
    encoding="utf-8-sig"
)

print("\n=== COMPARAÇÃO ANTES E DEPOIS ===")
print("Linhas originais:", len(df_original))
print("Linhas tratadas:", len(df))

print("\nValores ausentes após a limpeza:")
print(df.isna().sum())

print("\nArquivo tratado salvo:", ARQUIVO_TRATADO)

# ==========================================
# ETAPA 5 - ANÁLISE E VISUALIZAÇÃO
# ==========================================

sns.set_theme()

# GRÁFICO 1 - Jogos por gênero
plt.figure(figsize=(10, 5))

df["Gênero"].value_counts().plot(kind="bar")

plt.title("Quantidade de jogos por gênero")
plt.xlabel("Gênero")
plt.ylabel("Quantidade de registros")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig("grafico_generos.png")
plt.show()

# GRÁFICO 2 - Jogos por plataforma
plt.figure(figsize=(10, 5))

df["Plataforma"].value_counts().plot(kind="bar")

plt.title("Quantidade de jogos por plataforma")
plt.xlabel("Plataforma")
plt.ylabel("Quantidade de registros")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig("grafico_plataformas.png")
plt.show()

# GRÁFICO 3 - Jogos por ano
anos = df["Ano de Lançamento"].dropna()

if not anos.empty:
    contagem_anos = (
        anos.astype(int).value_counts().sort_index()
    )

    plt.figure(figsize=(10, 5))
    contagem_anos.plot(kind="line", marker="o")

    plt.title("Quantidade de jogos por ano")
    plt.xlabel("Ano de lançamento")
    plt.ylabel("Quantidade de registros")
    plt.tight_layout()
    plt.savefig("grafico_anos.png")
    plt.show()

# ==========================================
# ANÁLISE NUMÉRICA - VENDAS E AVALIAÇÕES
# ==========================================

vendas = df["Vendas Globais (milhões)"].dropna()

if not vendas.empty:
    print("\n=== MAIORES VENDAS REGISTRADAS ===")

    print(
        df.dropna(subset=["Vendas Globais (milhões)"])
        .sort_values(
            "Vendas Globais (milhões)",
            ascending=False
        )[
            ["Nome do Jogo", "Plataforma",
             "Vendas Globais (milhões)"]
        ].head(10)
    )
else:
    print(
        "\nNão há vendas verificadas suficientes "
        "para comparar os jogos."
    )

avaliacoes = df["Avaliação"].dropna()

if not avaliacoes.empty:
    print(
        "\nMédia das avaliações disponíveis:",
        round(avaliacoes.mean(), 2)
    )
else:
    print(
        "\nNão há avaliações verificadas suficientes "
        "para calcular uma média."
    )

# ==========================================
# DESCOBERTAS PARA A EMPRESA
# ==========================================

print("\n=== RESUMO PARA A DIRETORIA ===")

print("\nGêneros com mais registros:")
print(df["Gênero"].value_counts().head(3))

print("\nPlataformas com mais registros:")
print(df["Plataforma"].value_counts().head(3))

print("\nAnos com mais lançamentos:")
print(
    df["Ano de Lançamento"]
    .value_counts()
    .head(5)
)

print("\nAnálise concluída!")
print("Confira os gráficos e o CSV tratado.")
