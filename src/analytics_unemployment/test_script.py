import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Criando um DataFrame simples com pandas
data = {
    'Ano': [2020, 2021, 2022, 2023],
    'Valor': [150, 200, 250, 300]
}
df = pd.DataFrame(data)

# Exibindo o DataFrame
print("DataFrame:")
print(df)

# Criando um gráfico simples com seaborn e matplotlib
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))
sns.barplot(x='Ano', y='Valor', data=df, palette="Blues_d")
plt.title('Gráfico de Valores por Ano')
plt.show()
