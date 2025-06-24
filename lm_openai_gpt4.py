from openai import OpenAI
from config import makeTranscriptsAnonymousParagraph
from dotenv import load_dotenv

from prompt_generator import generate_prompt

load_dotenv()
client = OpenAI()

def summarize_transcript(text):
    print("running language model on transcript")

    prompt = generate_prompt(text, True, True)

    response = client.chat.completions.create(
        # model="gpt-4o-mini",
        model="gpt-4o-nano",
        max_completion_tokens=20,
        stop="\n",
        messages= [
            {"role": "system", "content": prompt["system_prompt"]},
            {"role": "user", "content": prompt["user_prompt"]}
        ]
    )

    result = response.choices[0].message.content

    full_response = result
    print(f"---\nfull thing:", full_response, "\n----\n")
    result = result.split("\n")
    result = result[0].strip()
    print("llm returning")
    return result

# with open("testText.txt", 'r') as file:
#     testText = file.read()
#
# print("Input text:", testText)
#
# topic = summarize_transcript(testText)
# print("Detected Topic:", topic)
