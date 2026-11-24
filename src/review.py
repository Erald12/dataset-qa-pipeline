import json

import anthropic

from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

GUIDELINE = (
    "Label a text 'time_sensitive' if it contains information that can change "
    "over time (prices, current events, rankings, opening hours, latest versions). "
    "Otherwise label it 'not_time_sensitive'."
)


def review_row(row):
    prompt = (
        f"You are a dataset QA reviewer. Guideline: {GUIDELINE}\n\n"
        f"Text: {row['text']}\n"
        f"Assigned label: {row['label']}\n\n"
        'Reply only with JSON, no other text: {"correct": true or false, "reason": "one sentence"}'
    )

    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    text_blocks = [block.text for block in message.content if block.type == "text"]
    raw = text_blocks[0] if text_blocks else ""

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"correct": None, "reason": "could not parse Claude response"}
