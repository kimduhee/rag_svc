def clean_text(text: str) -> str:
    """
    PDF에서 추출한 원시 텍스트를 LLM/임베딩에 적합한 형태로 정제한다.

    - 여러 줄바꿈(\n)이 연속된 부분을 하나로 축약
    - 공백(스페이스, 탭 등)이 연속된 부분을 하나의 스페이스로 축약
    - 앞뒤 공백 제거
    """
    #text = re.sub(r"\n+", "\n", text)
    #text = re.sub(r"\s+", " ", text)
    return text.strip()