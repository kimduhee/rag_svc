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

def build_context(results, max_chars=3000):
    """
    검색된 passage 리스트에서 LLM에 넘길 최종 컨텍스트 문자열을 구성한다.

    - 점수 순으로 passage를 이어붙이다가 max_chars를 초과하면 중단
    - 너무 긴 컨텍스트는 LLM 입력 토큰 수를 초과할 수 있으므로 상한을 둔다.
    """
    context_parts = []
    total = 0
    for r in results:
        text = r["content"]
        if total + len(text) > max_chars:
            break
        context_parts.append(text)
        total += len(text)
    return "\n\n".join(context_parts)