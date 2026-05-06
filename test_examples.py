"""
Optional quick test file.
Run after installing requirements:

python test_examples.py

This imports the translation function from app.py and prints the three required examples.
"""

from app import translate_text

examples = [
    "I like soccer",
    "How are you?",
    "What time is it?",
]

for example in examples:
    print(f"Input: {example}")
    print(f"Spanish: {translate_text(example, 'English', 'Spanish')}")
    print("-" * 40)
