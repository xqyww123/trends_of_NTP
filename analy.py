from more_itertools.more import exactly_n
from openai import OpenAI
import PyPDF2
import json
import re

client = OpenAI(
    api_key="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"
)

def extract_json(response_str: str):
    # 使用正则表达式匹配代码块中的 JSON 内容
    pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(pattern, response_str, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = response_str.strip()
    return json.loads(json_str)

def analy(path):
    pdf_file = open('example.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    # Remove images from the text
    text_without_images = ""

    for word in text.split():
        if word.startswith("Image") or word.startswith("IMAGE"):
            continue
        text_without_images += word + " "
    print(text_without_images)

    response = client.chat.completions.create(
        model='o1-mini',
        messages=[
            {"role": "user", "content":
                """You are a professional scholar in theoretical computer science, interactive theorem proving, machine learning, and large language models.
                Neural theorem proving is applying large language models to drive interactive theorem provers to do mathematical proofs.
                Now you need to read the following paper and determine if the paper is about neural theorem proving, that is, if the paper is about applying large language models to drive interactive theorem prover.
                If so, answer what are the theorem provers supported by the work described in the paper.
                The paper may mention many theorem provers but you should only answer with the ones that the work adopts to conduct its experiments.
                You should not answer with the ones that are not supported by the work.
                You should respond a JSON list of the names of the supported theorem provers.
                The name must be a string chosen from "Lean", "Isabelle", "Coq", and "other".
                Note, the paper is not necessarily about neural theorem proving.
                If the paper is not about neural theorem proving, you must answer with an empty list."""

                + '\n\n\n' + text_without_images
             }
        ]
    )

    reply = response.choices[0].message.content.strip()

    return extract_json(reply)
