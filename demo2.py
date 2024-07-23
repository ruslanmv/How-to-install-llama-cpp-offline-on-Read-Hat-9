from llama_cpp import Llama

# Initialize the Llama model with the specified model path
llm = Llama(
    model_path="./models/granite-7b-lab-Q4_K_M.gguf"
)

# Define the system prompt
system_prompt = "You are a knowledgeable assistant."

# Define the user prompt
user_prompt = "Q: Name the planets in the solar system? A: "

# Combine system and user prompts
full_prompt = system_prompt + "\n" + user_prompt

# Generate the completion with additional parameters
output = llm(
    prompt=full_prompt,  # Combined system and user prompt
    max_tokens=32,  # Generate up to 32 tokens, set to None to generate up to the end of the context window
    stop=["Q:", "\n"],  # Stop generating just before the model would generate a new question
    echo=True,  # Echo the prompt back in the output
    temperature=0.7,  # Sampling temperature, lower is more deterministic
    top_p=0.9,  # Top-p sampling, higher value includes more tokens
    frequency_penalty=0.5  # Penalize new tokens based on their existing frequency in the text
)

# Print the output
print(output)
