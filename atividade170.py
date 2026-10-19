import pandas as pd

df = pd.read_csv("datas_170.csv")

# Mostrar o tipo antes da conversão
print("Antes:", df["Data"].dtype)

# Converter as datas
df["Data"] = pd.to_datetime(
    df["Data"],
    format="mixed",
    dayfirst=True
)

# Mostrar o tipo depois da conversão
print("Depois:", df["Data"].dtype)

print(df.head())

print("Datas ausentes:")
print(df["Data"].isna().sum())


df = df.dropna(subset=["Data"])

print(df)
print("Registros restantes:", len(df))

print("Tipo da coluna:", df["Data"].dtype)
print("Datas ausentes:", df["Data"].isna().sum())
print("Total de registros:", len(df))


import pandas as pd

df = pd.DataFrame({
    'Idade': [16, 17, 18, 16, 17, 300, 19, 18, 17, 16]
})

print(df)



import pandas as pd

df = pd.DataFrame({
    'Idade': [16, 17, 18, 16, 17, 300, 19, 18, 17, 16]
})

# Corrigir o valor suspeito no índice 5
df.loc[5, 'Idade'] = 18

print(df)


import pandas as pd

df = pd.DataFrame({
    'Idade': [16, 17, 18, 16, 17, 300, 19, 18, 17, 150]
})

limite = 100

for indice in df.index:
    if df.loc[indice, 'Idade'] > limite:
        df.loc[indice, 'Idade'] = limite

print(df)


import pandas as pd

df = pd.DataFrame({
    'Idade': [16, 17, 18, 16, 17, 300, 19, 18, 17, 150]
})

limite = 100
indices_remover = []

for indice in df.index:
    if df.loc[indice, 'Idade'] > limite:
        indices_remover.append(indice)

df = df.drop(indices_remover)

print(df)


import pandas as pd

df = pd.DataFrame({
    'Data': ['10-09-2026', '11/09/2026', '12-09-2026', '13/09/2026'],
    'Idade': [16, 17, 300, 18]
})

print("Tabela original:")
print(df)

# 1. Corrigir o formato das datas
df['Data'] = pd.to_datetime(
    df['Data'],
    format='mixed',
    dayfirst=True
)

# 2. Remover linhas com idade acima de 100
limite = 100
for indice in df.index:
    if df.loc[indice, 'Idade'] > limite:
        df = df.drop(indice)

print("\nTabela tratada:")
print(df)

print("\nTipos de dados:")
print(df.dtypes)
