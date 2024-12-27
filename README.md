# TERRAi

## Instalar Python e Terraform CLI

Certifique-se de ter o Python 3.8+ instalado em sua máquina.  
Instale o Terraform CLI de acordo com a documentação oficial.

### Criar um Ambiente Virtual

```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### Instalar Dependências Python

```sh
pip install fastapi uvicorn transformers torch
```

### Executar o Código

Salve o código atualizado em um arquivo, por exemplo, `main.py`.  
Inicie o servidor:

```sh
uvicorn main:app --reload
```

### Testar os Endpoints

Use ferramentas como Postman ou curl para enviar requisições aos endpoints.  
Por exemplo:

```sh
curl -X POST "http://127.0.0.1:8000/generate-terraform" -H "Content-Type: application/json" -d '{"description": "Criar uma instância EC2 com segurança", "provider": "aws"}'
```

---

## Explicação das Bibliotecas Python

Os programas que você está instalando no seu terminal são bibliotecas Python que serão usadas no seu projeto. Aqui está uma explicação detalhada de cada uma delas e sua utilidade:

### fastapi

- **Descrição**: FastAPI é um framework web moderno e de alto desempenho para construir APIs com Python.
- **Utilidade**: Permite criar endpoints HTTP de forma rápida e eficiente. No seu projeto, é usado para criar a API que expõe funcionalidades como geração, validação e explicação de código Terraform.

### uvicorn

- **Descrição**: Uvicorn é um servidor ASGI rápido para rodar aplicações web baseadas em ASGI, como FastAPI.
- **Utilidade**: Serve para rodar a aplicação FastAPI. Ele é otimizado para desempenho e é capaz de lidar com muitas conexões simultâneas.

### transformers

- **Descrição**: Transformers é uma biblioteca da Hugging Face que fornece ferramentas para trabalhar com modelos de linguagem natural.
- **Utilidade**: No seu projeto, é usado para carregar modelos pré-treinados e tokenizadores, permitindo a geração de texto e outras tarefas de NLP (Processamento de Linguagem Natural).

### torch

- **Descrição**: PyTorch é uma biblioteca de aprendizado profundo que fornece ferramentas para construir e treinar redes neurais.
- **Utilidade**: Necessária para rodar modelos de linguagem natural que foram treinados usando PyTorch. No seu projeto, é usada em conjunto com a biblioteca transformers para executar o modelo de linguagem.

### Dependências Adicionais Instaladas

Durante a instalação, várias outras dependências são instaladas automaticamente. Aqui estão algumas delas e suas utilidades:

- **starlette**: Framework web leve usado internamente pelo FastAPI.
- **pydantic**: Biblioteca para validação de dados e criação de modelos de dados, usada pelo FastAPI.
- **requests**: Biblioteca para fazer requisições HTTP, usada internamente por várias bibliotecas.
- **tokenizers**: Biblioteca para tokenização de texto, usada pela transformers.
- **numpy**: Biblioteca para computação numérica, usada por muitas bibliotecas de aprendizado profundo.
- **tqdm**: Biblioteca para mostrar barras de progresso, útil para acompanhar o progresso de operações longas.
- **huggingface-hub**: Biblioteca para interagir com o hub da Hugging Face, onde os modelos pré-treinados são armazenados.

Essas bibliotecas e suas dependências são essenciais para o funcionamento do seu projeto, permitindo a criação de uma API robusta e eficiente que utiliza modelos de linguagem natural para diversas tarefas.

---

## Execução do Código

O código é executado no ambiente Python como uma aplicação web utilizando o framework FastAPI. Ele conta com três principais endpoints, cada um com funcionalidades específicas. Aqui está uma explicação detalhada de como o código será executado e como os arquivos serão gerenciados:

### 1. Início do Servidor

O código utiliza uvicorn para iniciar o servidor na porta 8000. Quando o arquivo Python é executado diretamente (`__name__ == "__main__"`), o comando `uvicorn.run(app, host="0.0.0.0", port=8000)` inicia o servidor.  
Após o servidor iniciar, a API estará disponível para interagir via HTTP.

### 2. Endpoints e Fluxo de Execução

#### a) /generate-terraform

- **Descrição**: Este endpoint recebe uma descrição textual da infraestrutura desejada e o nome do provedor de nuvem (padrão é aws).
- **Funcionamento**:
    - Constrói um prompt a partir dos dados fornecidos (description e provider).
    - Usa o modelo de linguagem (via transformers) para gerar o código Terraform.
    - Retorna o código gerado no formato JSON.
- **Arquivos**: Não cria ou lê arquivos no sistema. Todo o processamento ocorre em memória.

#### b) /validate-terraform

- **Descrição**: Este endpoint valida o código Terraform gerado ou fornecido.
- **Funcionamento**:
    - Escreve o código fornecido em um arquivo temporário chamado `main.tf` na mesma pasta onde o script está sendo executado.
    - Executa o comando `terraform init` para configurar o ambiente Terraform.
    - Executa `terraform validate` para verificar se o código é válido.
    - Retorna o status da validação (success ou failure).
- **Arquivos**:
    - Cria o arquivo temporário `main.tf`.
    - Este arquivo é necessário para que os comandos do Terraform CLI possam operar corretamente.

#### c) /explain-terraform

- **Descrição**: Este endpoint recebe um código Terraform e o explica em linguagem natural.
- **Funcionamento**:
    - Constrói um prompt contendo o código Terraform fornecido.
    - Usa o modelo de linguagem para gerar uma explicação textual.
    - Retorna a explicação no formato JSON.
- **Arquivos**: Não cria ou lê arquivos. Todo o processamento é realizado em memória.

### 3. Gerenciamento de Arquivos

Apenas o endpoint `/validate-terraform` interage diretamente com o sistema de arquivos.

- **Arquivos criados**:
    - `main.tf`: Contém o código Terraform a ser validado. Ele é sobrescrito a cada requisição ao endpoint.
- **Recomendações**:
    - Se houver muitas requisições simultâneas, pode ser interessante gerar nomes únicos para os arquivos temporários (e.g., usando UUIDs ou timestamps).
    - Após a validação, o arquivo temporário poderia ser removido para evitar o acúmulo de arquivos no sistema.

### 4. Requisitos de Ambiente

- **Módulos Python**:
    - `transformers`: Para carregar o modelo de linguagem e gerar respostas.
    - `fastapi`: Para criar a API.
    - `uvicorn`: Para rodar o servidor.
- **Terraform CLI**:
    - O comando `terraform` precisa estar instalado e configurado no ambiente para que a validação funcione.