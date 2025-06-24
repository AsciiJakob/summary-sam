from lm_llama_3_2_1B import summarize_transcript

# summarize_transcript("[hebbian]: hello\n[misha]: good evening hebbian!")
with open("testText.txt", 'r') as file:
    testText = file.read()

print("Input text:", testText)

topic = summarize_transcript(testText)
print("Detected Topic:", topic)
