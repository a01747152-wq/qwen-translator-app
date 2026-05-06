# Qwen2 Translator App

Small translation app that uses **Qwen/Qwen2-0.5B-Instruct** locally through Hugging Face Transformers.

No API keys from any external model are used.

## Features

- Translate text from one language to another.
- Uses Qwen2-0.5B locally.
- Includes the three required examples:
  - `I like soccer`
  - `How are you?`
  - `What time is it?`

## Requirements

- Python 3.10 or newer recommended.
- Internet connection is required only the first time to download the model from Hugging Face.
- After the model is cached, it can run locally.

## Installation

```bash
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

Then open the local Gradio link shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

## Example expected translations

| Input | Source | Target | Expected output |
|---|---|---|---|
| I like soccer | English | Spanish | Me gusta el fútbol |
| How are you? | English | Spanish | ¿Cómo estás? |
| What time is it? | English | Spanish | ¿Qué hora es? |

## Important note

Qwen2-0.5B is a small language model, so its translations may vary slightly. The app constrains the model with a translation-only prompt to improve results.
