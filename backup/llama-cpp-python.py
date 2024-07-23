import os
import requests
from llama_cpp import Llama, LlamaPromptLookupDecoding
import instructor
from pydantic import BaseModel
from typing import List
from rich.console import Console

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
        draft_model=LlamaPromptLookupDecoding(num_pred_tokens=2),
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

    create = instructor.patch(
        create=llama.create_chat_completion_openai_v1,
        mode=instructor.Mode.JSON_SCHEMA,
    )

    text_block = """
    In our recent online meeting, participants from various backgrounds joined to discuss
    the upcoming tech conference. The names and contact details of the participants were as follows:

    - Name: John Doe, Email: johndoe@email.com, Twitter: @TechGuru44
    - Name: Jane Smith, Email: janesmith@email.com, Twitter: @DigitalDiva88
    - Name: Alex Johnson, Email: alexj@email.com, Twitter: @CodeMaster2023

    During the meeting, we agreed on several key points. The conference will be held on March 15th, 2024,
    at the Grand Tech Arena located at 4521 Innovation Drive. Dr. Emily Johnson, a renowned AI researcher,
    will be our keynote speaker.

    The budget for the event is set at $50,000, covering venue costs, speaker fees, and promotional activities.
    Each participant is expected to contribute an article to the conference blog by February 20th.

    A follow-up meeting is scheduled for January 25th at 3 PM GMT to finalize the agenda and confirm the list of speakers.
    """

    class User(BaseModel):
        name: str
        email: str
        twitter: str

    class MeetingInfo(BaseModel):
        users: List[User]
        date: str
        location: str
        budget: int
        deadline: str

    extraction_stream = create(
        response_model=instructor.Partial[MeetingInfo],
        messages=[
            {
                "role": "user",
                "content": f"Get the information about the meeting and the users {text_block}",
            },
        ],
        stream=True,
    )

    console = Console()

    for extraction in extraction_stream:
        obj = extraction.model_dump()
        console.clear()
        console.print(obj)

# Example usage
prompt = "What is the capital of Italy?"
repo_id = "instructlab/granite-7b-lab-GGUF"
filename = "granite-7b-lab-Q4_K_M.gguf"

run_llama_cpp_inference(prompt, repo_id, filename)
