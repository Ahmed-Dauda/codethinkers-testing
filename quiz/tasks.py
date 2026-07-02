from celery import shared_task
from django.core.cache import cache
import json
import time
import re
from openai import OpenAI



from school import settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)

import os, json, time, re, html
from celery import shared_task
from openai import OpenAI
from django.core.cache import cache


@shared_task(bind=True)
def generate_topics_task(self, prompt, task_key, is_programming=False):

    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def clean_response(text):
        if text.startswith("```"):
            text = text.strip("`")
            text = text.lstrip("json").strip()
        match = re.search(r"(\[.*\])", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def format_topics(topics_json):
        heading_keywords = ["include:", "are:", "must:", "consist of:", "types of", "principles of"]
        preview_topics = []

        for topic in topics_json:
            description = topic.get("description", "")
            lines = description.split("\n")
            formatted_lines = []
            in_code_block = False
            current_lang = ""

            for line in lines:
                stripped = line.strip()

                if stripped.startswith("```") and not in_code_block:
                    in_code_block = True
                    current_lang = stripped.replace("```", "").strip().lower()
                    lang_class = f' class="language-{current_lang}"' if current_lang else ""
                    formatted_lines.append(f"<pre><code{lang_class}>")
                    continue
                elif stripped.startswith("```") and in_code_block:
                    in_code_block = False
                    current_lang = ""
                    formatted_lines.append("</code></pre>")
                    continue
                elif stripped.startswith("<pre><code"):
                    in_code_block = True
                    formatted_lines.append(stripped)
                    continue
                elif stripped.startswith("</code></pre>"):
                    in_code_block = False
                    formatted_lines.append(stripped)
                    continue

                if in_code_block:
                    formatted_lines.append(html.escape(line))
                else:
                    safe_line = html.escape(stripped)
                    if any(kw.lower() in stripped.lower() for kw in heading_keywords):
                        formatted_lines.append(f"<h3>{safe_line}</h3>")
                    elif stripped:
                        formatted_lines.append(f"<p>{safe_line}</p>")

            preview_topics.append({
                "title": topic.get("title", ""),
                "desc": "\n".join(formatted_lines),
                "transcript": ""
            })

        return preview_topics

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=16000,
                temperature=0
            )

            topics_text = response.choices[0].message.content.strip()
            topics_text = clean_response(topics_text)
            topics_json = json.loads(topics_text)

            cache.set(task_key, {
                'status': 'done',
                'topics': format_topics(topics_json)
            }, timeout=600)

            return task_key

        except json.JSONDecodeError:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            cache.set(task_key, {
                'status': 'error',
                'message': 'Failed to parse AI response after 3 attempts'
            }, timeout=600)

        except Exception as e:
            cache.set(task_key, {
                'status': 'error',
                'message': str(e)
            }, timeout=600)
            raise