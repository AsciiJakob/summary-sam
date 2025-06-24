from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from config import makeTranscriptsAnonymousParagraph
from prompt_generator import generate_prompt

model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

def summarize_transcript(text):
    print("running language model on transcript")
    prompt = generate_prompt(text, True, False)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=20,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.encode("\n")[0]  # soft stop at newline

    )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    full_response = result.split(prompt)[1]
    print(f"---\nfull thing:", full_response, "\n----\n")
    result = result.split("{Summary}:")
    result = result[len(result)-1]
    result = result.split("\n")
    result = result[0].strip()
    print("llm returning")
    return result

