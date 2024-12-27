
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import os

# Inicializa o modelo e o tokenizador
# Define o nome do modelo a ser utilizado (pode ser ajustado conforme necessário)
MODEL_NAME = "EleutherAI/gpt-neo-2.7B"  # Substitua pelo modelo desejado

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)  # Carrega o tokenizador do modelo
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)  # Carrega o modelo para geração de texto

# Inicializa o pipeline de geração de texto
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Cria a aplicação FastAPI
app = FastAPI()

class TerraformRequest(BaseModel):
    description: str
    provider: str

# Endpoint para gerar código Terraform
@app.post("/generate-terraform")
async def generate_terraform(request: TerraformRequest):
    
    description = request.description
    provider = request.provider
    
    """
    Gera código Terraform com base em uma descrição textual e no provedor de nuvem especificado.
    
    Args:
        description (str): Descrição da infraestrutura desejada.
        provider (str): Provedor de nuvem (e.g., aws, azure, gcp). Padrão é 'aws'.

    Returns:
        dict: Código Terraform gerado.
    """
    try:
        # Monta o prompt para o modelo de IA
        prompt = (
            f"Generate a Terraform script with all resources in .tf files for the following description: {description}. "
            f"The cloud provider is {provider}. Include best practices, VPC and comments in portuguese in the scripts."
        )
        
        # Gera o código Terraform com o modelo
        generated_code = text_generator(prompt, max_length=512, num_return_sequences=1)[0]['generated_text']
        return {"terraform_code": generated_code}

    except Exception as e:
        # Lida com erros e retorna uma mensagem de erro detalhada
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")

# Endpoint para validar código Terraform
@app.post("/validate-terraform")
async def validate_terraform_code(terraform_code: str):
    """
    Valida o código Terraform usando o CLI do Terraform.

    Args:
        terraform_code (str): Código Terraform a ser validado.

    Returns:
        dict: Resultados da validação.
    """
    try:
        # Escreve o código Terraform em um arquivo temporário
        with open("main.tf", "w") as f:
            f.write(terraform_code)

        # Executa o comando 'terraform init' para inicializar o ambiente (silenciado)
        os.system("terraform init > /dev/null")
        
        # Executa o comando 'terraform validate' para validar o código (silenciado)
        validation_result = os.system("terraform validate > /dev/null")

        # Retorna o resultado da validação
        if validation_result == 0:
            return {"validation": "success", "details": "Terraform code is valid."}
        else:
            return {"validation": "failure", "details": "Terraform code is invalid."}

    except Exception as e:
        # Lida com erros e retorna uma mensagem de erro detalhada
        raise HTTPException(status_code=500, detail=f"Error validating code: {str(e)}")

# Endpoint para explicar código Terraform
@app.post("/explain-terraform")
async def explain_terraform_code(terraform_code: str):
    """
    Explica o código Terraform em linguagem natural.
    
    Args:
        terraform_code (str): Código Terraform a ser explicado.

    Returns:
        dict: Explicação do código Terraform.
    """
    try:
        # Monta o prompt para o modelo de IA
        prompt = (
            f"Explain the following Terraform code in plain English: \n{terraform_code}\n"
        )
        
        # Gera a explicação do código
        explanation = text_generator(prompt, max_length=512, num_return_sequences=1)[0]['generated_text']
        return {"explanation": explanation}

    except Exception as e:
        # Lida com erros e retorna uma mensagem de erro detalhada
        raise HTTPException(status_code=500, detail=f"Error explaining code: {str(e)}")

# Inicia a aplicação FastAPI
if __name__ == "__main__":
    # Executa o servidor na porta 8000
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
