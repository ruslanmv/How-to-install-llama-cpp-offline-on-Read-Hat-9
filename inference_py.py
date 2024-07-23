import os
import requests
from llama_cpp import Llama

def download_model(repo_id, filename, target_path):
    """Downloads a model file from Hugging Face Hub."""
    base_url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
    response = requests.get(base_url)
    response.raise_for_status()  # Ensure the request was successful
    with open(target_path, "wb") as f:
        f.write(response.content)
    print(f"Model downloaded to '{target_path}'")

def setup_llama(model_path):
    """Sets up the Llama model."""
    return Llama(
        model_path=model_path,
        n_gpu_layers=-1,
        chat_format="chatml",
        n_ctx=2048,
        logits_all=True,
        verbose=False,
    )

def run_llama_cpp_inference(prompt, repo_id, filename):
    """Runs inference using llama.cpp for a single prompt."""
    model_dir = "./models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, filename)

    if not os.path.exists(model_path):
        print(f"Downloading model '{filename}'...")
        download_model(repo_id, filename, model_path)
    else:
        print(f"Using locally cached model '{filename}'")

    llama = setup_llama(model_path)

    response = llama.create_chat_completion_openai_v1(
        prompt={"role": "user", "content": prompt}
    )

    return response["choices"][0]["message"]["content"]

# Ask for the capital of Italy
prompt = "What is the capital of Italy?"
repo_id = "instructlab/granite-7b-lab-GGUF"
filename = "granite-7b-lab-Q4_K_M.gguf"

output = run_llama_cpp_inference(prompt, repo_id, filename)
print(f"Prompt: {prompt}\nResponse: {output}")