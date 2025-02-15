import subprocess
import os
import requests

def download_model(repo_id, filename, target_path):
    """Downloads a model file from Hugging Face Hub."""
    base_url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
    response = requests.get(base_url)
    response.raise_for_status()  # Ensure the request was successful
    with open(target_path, "wb") as f:
        f.write(response.content)
    print(f"Model downloaded to '{target_path}'")

def run_llama_cpp_inference(prompt, repo_id, filename, n_predict=256, top_k=40, temperature=0.7):
    """Runs inference using llama.cpp for a single prompt."""
    
    llama_cpp_executable = "./llama.cpp/llama-cli"
    if not os.path.exists(llama_cpp_executable):
        raise FileNotFoundError(f"llama.cpp executable not found: {llama_cpp_executable}")

    model_dir = "./models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, filename)
    
    if not os.path.exists(model_path):
        print(f"Downloading model '{filename}'...")
        download_model(repo_id, filename, model_path)
    else:
        print(f"Using locally cached model '{filename}'")

    try:
        result = subprocess.run([
            llama_cpp_executable,
            "-m", model_path,
            "-n", str(n_predict),
            "--top_k", str(top_k),
            "--temp", str(temperature),
            "-p", prompt
        ], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running llama.cpp for prompt '{prompt}':\n{e.stderr}")
        return "Error during inference"

# Example usage
prompt = "What is the capital of Italy?"
repo_id = "instructlab/granite-7b-lab-GGUF"
filename = "granite-7b-lab-Q4_K_M.gguf"

output = run_llama_cpp_inference(prompt, repo_id, filename)
print(f"Prompt: {prompt}\nResponse: {output}")
