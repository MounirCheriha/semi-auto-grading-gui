import json
import re
from openai import OpenAI
from core import utils
import os

client = OpenAI(api_key=utils.read_api_key_from_file()) 

def grade(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=64
        )

        content = response.choices[0].message.content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            result = json.loads(match.group().replace('\n', ' '))
            return float(result.get('grade', -1)), result.get('feedback', ''), float(result.get('confidence', 0))
        else:
            return -1, "Formato JSON no encontrado", 0
    except Exception as e:
        return -1, f"Error GPT-4o: {e}", 0