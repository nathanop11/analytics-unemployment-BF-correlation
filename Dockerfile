# Usar uma imagem oficial do Python como base
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo pyproject.toml e poetry.lock para dentro do contêiner
COPY pyproject.toml poetry.lock /app/

# Instalar o Poetry
RUN pip install poetry

# Instalar as dependências do projeto
RUN poetry install --no-root

# Copiar o restante do código-fonte para dentro do contêiner
COPY . /app/

# Expôr a porta do Jupyter (caso esteja usando Jupyter no projeto)
EXPOSE 8888

# Definir o comando para rodar o Jupyter Notebook (ou o script principal)
CMD ["poetry", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root"]
