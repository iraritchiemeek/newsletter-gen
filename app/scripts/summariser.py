import json
from openai import OpenAI
import os

client = OpenAI()

SUMMARIZE_PROMPT = """
You are an expert at generating concise, entity-dense summaries of user provided email newsletters.

#Important

- Generate multiple summaries per file, categorized by topic.

- Each summary should be concise (4-5 sentences, ~80 words).

- Make every word count. Do not fill with additional words which are not critical to summarize the original document.

- Do not include sentences like "here is a summary". Only provide the summary itself.

- Do not summarise non-content text such as greetings or contact details.

- Return the results in JSON format with each topic as a key and the corresponding summary as the value.

- Do not include newlines or special characters in the response.

#Example output
[{"topic1": "summary1"}, {"topic2": "summary2"}, {"topic3": "summary3"}, ...]
"""

def get_json_summaries(text):
  print("Beginning summarisation")
  completion = client.chat.completions.create(
    model="gpt-4o",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": SUMMARIZE_PROMPT},
      {"role": "user", "content": f"Document: {text}"},
    ],
  )
  print("Summarised file")
  completion = completion.choices[0].message
  return parse_json_completion(completion)

def parse_json_completion(completion):
  print("Parsing JSON")
  parsed_completion = json.loads(completion.content)
  return parsed_completion
