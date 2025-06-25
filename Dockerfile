FROM python:3.13-slim

# Instala make e dependências básicas
RUN apt-get update && apt-get install -y make gcc && rm -rf /var/lib/apt/lists/*

# Cria um usuário não-root
RUN adduser --disabled-password --gecos '' devuser

# Define diretório de trabalho
WORKDIR /home/devuser/app

# Copia só o requirements e instala dependências (melhor cache)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Permissões para devuser e troca de usuário
RUN chown -R devuser:devuser /home/devuser
USER devuser

# Comando padrão do container (você pode mudar ou sobrescrever no devcontainer)
CMD ["pytest"]
