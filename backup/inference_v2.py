import subprocess
import os
from huggingface_hub import hf_hub_download

def run_llama_cpp_inference(prompt, repo_id, filename, n_predict=256, top_k=40, temperature=0.7):
    """Runs inference using llama.cpp for a single prompt."""
    
    llama_cpp_executable = "./llama.cpp/llama-cli"
    if not os.path.exists(llama_cpp_executable):
        raise FileNotFoundError(f"llama.cpp executable not found: {llama_cpp_executable}")

    model_path = os.path.join("./models", filename)  # Define the model path
    
    if not os.path.exists(model_path):
        print(f"Downloading model '{filename}'...")
        model_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir="./models")
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
