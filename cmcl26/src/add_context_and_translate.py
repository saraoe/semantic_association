"""
Add a longer context to the Federmeier and Kutas data as well as translating it all the Dutch.
"""

from pathlib import Path
import pandas as pd
import re
from openai import OpenAI

with open("openai_api_key.txt") as f:
    key = f.read()

client = OpenAI(api_key=key)

data_path = Path("cmcl26", "data")
df = pd.read_excel(data_path / "federmeier_kutas_1999.xlsx")


def add_context(row: pd.DataFrame):
    "add context to the two sentences ending in the expected target"
    context_prompt = "Write a context of approximately 100 words that could proceed the following two sentence. The context should be semantically sound with the last two sentence. Output only the proceeding context and not the two final sentences. \n"
    sentences = f"{row['context']} {row['expected']}"
    response = client.responses.create(
        model="gpt-5.2", input=context_prompt + sentences
    )
    response_text = response.output_text
    assert (
        re.search(sentences, response_text) is None
    )  # check sentences are not part of the response
    assert len(response_text.split(" ")) > 80 and len(response_text.split(" ")) < 120
    return response_text


def translate(row: pd.DataFrame, col_name: str):
    "translate context, longer_context, and target words from English to Dutch"
    if col_name in ["expected", "within", "between", "unexpected"]:
        translate_prompt = "Translate the following word from English into Dutch. Only output the word.\n"
    elif col_name == "context":
        translate_prompt = "Translate the following two sentences from English into Dutch. The translation should also consist of two sentences. The last sentence is missing the sentence-final word, so it should not end in a full stop and it should be possible to insert a noun at the end to finish the context.\n"
    elif col_name == "longer_context":
        translate_prompt = "Translate the following text from English into Dutch. The translation should also consist of approximately 100 words.\n"
    else:
        raise ValueError(f"Col_name {col_name} is not defined!")

    response = client.responses.create(
        model="gpt-5.2", input=translate_prompt + row[col_name]
    )
    response_text = response.output_text
    if col_name in ["expected", "within", "between", "unexpected"]:
        # check it is just one word
        if len(response_text.split(" ")) != 1:
            print(
                f"The response was not one word. The translation of {row[col_name]} was {response_text}. Returning None!"
            )
            return None
    if col_name == "context":
        # check it is two sentences
        assert len(response_text.split(".")) == 2
    if col_name == "longer_context":
        # check number of words being correct
        assert (
            len(response_text.split(" ")) > 70 and len(response_text.split(" ")) < 130
        )
    return response_text


df["longer_context"] = df.apply(add_context, axis=1)
for col_name in [
    "context",
    "expected",
    "within",
    "between",
    "unexpected",
    "longer_context",
]:
    df[f"translated_{col_name}"] = df.apply(translate, axis=1, col_name=col_name)
df.to_csv(data_path / "federmeier_kutas_1999.csv")
