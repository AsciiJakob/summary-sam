from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from config import makeTranscriptsAnonymousParagraph
from prompt_generator import generate_prompt
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN")

model_id = "meta-llama/Llama-3.2-1B"
tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto",
    token=hf_token
)

def summarize_transcript(text):
    print("running language model on transcript")
    prompt = generate_prompt(text, False, False)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=20,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.encode("\n")[0]
    )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    full_response = result.split(prompt)[1] if prompt in result else result
    print(f"---\nfull thing:", full_response, "\n----\n")

    result = result.split("{Summary}:")[-1].split("\n")[0].strip()
    print("llm returning")
    return result

