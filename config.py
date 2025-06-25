# all values in seconds
# the bot will record voice chat for contextTime amount of seconds, then it will transcribe it, feed it
# to the language model, update the status and then wait sleepTime seconds before repeating.
contextTime = 30 # how long recordings will be
sleepTime = 60 # duration to sleep between recordings
makeTranscriptsAnonymousParagraph = False # makes option below irrelevant. experiement thing, probably broken, i'd leave it off
# UNIMPLEMENTED # feedDummyNamesToLanguageModel = False # whether names in transcript should be replaced with more typical names (i.e. "John") when fed to the language model to make it less likely to hallcuinate
writeOutStatuses = True # whether discord statuses of the voice chat users should be fed to the language model
sendTranscripts = False # whether transcripts and summaries should be sent as a discord messages
sendSummaries = True # whether summaries should be sent as discord message

# model to be used
model_name = "llama_3_2_1B"
# model_name = "phi2"
# model_name = "openai_babbage"
# model_name = "openai_gpt4"
