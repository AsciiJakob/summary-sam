﻿# summary-sam
discord bot for transcribing voice-chat conversations and then summarizing them using language models. Supports both running models locally (phi-2 and llama 3.2 1B) and using cloud hosted apis (OpenAI gpt-4o-nano)

The summarization has partially been made to quite primitive and dumb as it is usually funnier than way. If you want proper, professional summarizes edit the `example_summaries.txt` file to suit your preferences and use GPT4 (and maybe something smarter than the nano model). 


## Running
creating a python virtual environment is highly recommended. I personally had issues with crackling/hacky audio before doing so, so there seems to be a risk of insidious dependency conflicts.

`python -m venv venv`

Windows:

`.\venv\Scripts\Activate.ps1` (powershell, if using normal command prompt run activate.bat instead)

Linux/MacOS:

`source venv/bin/activate`

then the virtual environment will be set up and you can install the requirements and run with the following three commands:

`pip install torch==2.2.2+cu118 torchvision==0.17.2+cu118 torchaudio==2.2.2 --extra-index-url https://download.pytorch.org/whl/cu118`

`pip install -r requirements.txt`

`py bot.py`

see `config.py` for configuration and make sure to fill up `.env` with secrets.
