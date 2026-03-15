"""
Ollama 요청 포맷 :

{
    'model': 'llama3', 
    'messages': [
        {
            'role': 'system | user | assistant', 
            'content': 'system_prompt 내용용'
        }
    'stream': True
}
"""

"""
질문 요청 포맷 중 role-system의 content 값 설정

Args:
    Doesn't exist
Returns:
    user_prompt: 완성된 role-user의 content text
"""
def get_system_content():

    """
    당신은 제공된 맥락만을 사용하여 질문에 답변하는 QA 어시스턴트입니다.

    규칙:

    1. 제공된 맥락의 정보만을 사용하여 질문에 답변해야 합니다.
    2. 맥락이 비어 있거나 답변이 포함되어 있지 않은 경우, "요청하신 질문에 대한 정보가 없습니다."라고 정확하게 답변하십시오.
    3. 자신의 지식을 사용하지 마십시오.
    4. 답을 지어내지 마십시오.
    5. 답변은 간결하게 작성하십시오.
    6. 한국어로 답변하십시오.
    7. 답변을 마크다운 형식으로 작성하세요
    """

    system_prompt = """
    You are a QA assistant that answers questions ONLY using the provided context.

    Rules:
    1. You MUST answer the question only using the information from the provided context.
    2. If the context is empty or does not contain the answer, respond exactly with: "요청하신 질문에 대한 정보가 없습니다.".
    3. Do NOT use your own knowledge.
    4. Do NOT make up an answer.
    5. Keep the answer concise.
    6. Answer in Korean.
    7. Format the answer in Markdown.
    """

    return system_prompt

"""
질문 요청 포맷 중 role-user의 content 값 설정

Args:
    question(str): 질문내용
    results(str): 조회된 chunk text

Returns:
    user_prompt: 완성된 role-user의 content text
"""
def get_user_content(question: str, results: str):

    user_prompt = f"""
    [Context]
    {results}

    [Question]
    {question}
    """

    return user_prompt