import re
from typing import List


def split_text_for_tts(text: str, max_chars: int = 80) -> List[str]:
    """按句號、問號、驚嘆號與換行切分文本"""
    clean_text = text.strip().replace("\r\n", "\n")
    sentences = re.split(r'([。!?！？\n])', clean_text)

    chunks = []
    current_chunk = ""

    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + sentences[i + 1]
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks if chunks else [text]
