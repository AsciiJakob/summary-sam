import config
system_prompt_task = "You are Summary Sam, a language model for summarizing transcripts. Every transcript must be followed by a summary. Keep summaries as consice as possible and under 20 words. avoid words like \"group conversations about...\" and \"discussion about...\", just write the general topic of conversation or what is happening. Use emojis, be humorous when possible."
# system_prompt = "You are tasked with transforming dialogue transcripts into concise summaries that capture the main theme or event of the conversation. Consider the key topics, emotions or actions, and provide a brief yet accurate depiction."

with open("example_summaries.txt", 'r', encoding="utf-8") as file:
    example_summaries = file.read()

if not config.writeOutStatuses: # remove statuses from examples
  new_examples = [] 
  for line in example_summaries.split("\n"):
      if not line.startswith("{Statuses}:"):
          new_examples.append(line)
  example_summaries = "\n".join(new_examples)


def examples_make_transcripts_paragraphed(examples):
    output = ""
    firstSentenceInDialogue = False
    for line in examples.split("\n"):
        if (line == "" or line.startswith("{Dialogue}") or line.startswith("{Summary}:")):
            if (line.startswith("{Summary}:")):
                output += "\n"
            if (firstSentenceInDialogue):
                line = line[1:] # remove first character (a space)
                firstSentenceInDialogue = False
            output += line+"\n"
            if (line.startswith("{Dialogue}")):
                firstSentenceInDialogue = True
            continue
        else:
            output += line.split(":")[1]
    return output


def generate_prompt(text, is_assistance_model, seperate_system_prompt):
    system_prompt = ""
    if is_assistance_model:
        system_prompt += system_prompt_task
        system_prompt += "\nBelow are some examples to demonstrate adequate summaries:"
        system_prompt += "\n\n"

    if config.makeTranscriptsAnonymousParagraph:
        system_prompt += examples_make_transcripts_paragraphed(example_summaries)
    else:
        system_prompt += example_summaries

    if (not example_summaries[-1] == "\n"):
        system_prompt += "\n"
    if (not example_summaries[-2] == "\n"):
        system_prompt += "\n"
    if is_assistance_model:
        system_prompt += "\nYou will now be given real input and must summarize it and provide nothing else than the summary.\n"

    user_prompt = ""
    user_prompt += "{Dialogue}\n"
    user_prompt += f"{text}\n"
    user_prompt += "{Summary}:"

    if seperate_system_prompt:
        output = {}
        output["system_prompt"] = system_prompt
        output["user_prompt"] = user_prompt
        return output
    else:
        return system_prompt+user_prompt

# with open("testText.txt", 'r') as file:
#     testText = file.read()
# prompt = generate_prompt(testText, True, True)
# print("system prompt:", prompt["system_prompt"])
# print("user prompt:", prompt["user_prompt"])

# with open("testText.txt", 'r') as file:
#     testText = file.read()
# prompt = generate_prompt(testText, True, False)
# print("prompt:", prompt)
