import re
import torch
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"

LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Korean",
    "Japanese",
    "Chinese",
]

print("Loading model... This may take a few minutes the first time.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None,
    trust_remote_code=True,
)

if not torch.cuda.is_available():
    model.to("cpu")


def clean_response(text: str) -> str:
    """Keeps only the translated answer when the model adds extra explanation."""
    text = text.strip()
    text = re.sub(r"^(Translation:|Translated text:|Answer:)\s*", "", text, flags=re.I)
    return text.strip().strip('"')


def translate_text(text: str, source_language: str, target_language: str) -> str:
    if not text.strip():
        return "Please write text to translate."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a translation assistant. Translate accurately and naturally. "
                "Return only the translation, without explanations."
            ),
        },
        {
            "role": "user",
            "content": f"Translate from {source_language} to {target_language}: {text}",
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = outputs[0][inputs["input_ids"].shape[-1]:]
    response = tokenizer.decode(generated, skip_special_tokens=True)
    return clean_response(response)


with gr.Blocks(title="Qwen2 Translator") as demo:
    gr.Markdown("# 🌎 Qwen2 Translator")
    gr.Markdown("Small translation app using **Qwen/Qwen2-0.5B-Instruct** locally. No external API keys required.")

    with gr.Row():
        source_language = gr.Dropdown(LANGUAGES, value="English", label="Source language")
        target_language = gr.Dropdown(LANGUAGES, value="Spanish", label="Target language")

    text_input = gr.Textbox(
        label="Text to translate",
        placeholder="Example: I like soccer",
        lines=3,
    )

    translate_button = gr.Button("Translate")
    output = gr.Textbox(label="Translation", lines=3)

    translate_button.click(
        translate_text,
        inputs=[text_input, source_language, target_language],
        outputs=output,
    )

    gr.Examples(
        examples=[
            ["I like soccer", "English", "Spanish"],
            ["How are you?", "English", "Spanish"],
            ["What time is it?", "English", "Spanish"],
        ],
        inputs=[text_input, source_language, target_language],
    )

if __name__ == "__main__":
    demo.launch()
