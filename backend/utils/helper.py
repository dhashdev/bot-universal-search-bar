from typing import List, Tuple

def process_history(history) -> str:
    history_template = ""
    for (input, output) in history:
        history_template += f"User: {input}\n" + f"Assistant: {output}\n"
    return history_template

def add_source_numbers(lst, source_name="Source", use_source=True):
    if use_source:
        return [f'[{idx + 1}]\t "{item[0]}"\n{source_name}: {item[1]}' for idx, item in enumerate(lst)]
    else:
        return [f'[{idx + 1}]\t "{item}"' for idx, item in enumerate(lst)]


def add_details(lst, lst_src):
    nodes = []
    for idx, (txt, src) in enumerate(zip(lst, lst_src)):
        nodes.append(
            f"{txt[:4]}{src}\n{txt[4:]}"
        )
    return nodes
