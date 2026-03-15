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