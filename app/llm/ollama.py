import requests
import json
import time

from app.llm.prompt import get_system_content, get_user_content
from app.core.config import settings
from app.core.logging import get_logger
from app.common.utils.string_util import build_context

logger = get_logger(__name__)

class OllamaClient:

    def __init__(self):
        self.model = settings.llm_model
        self.url = settings.llm_url

    def generate(self, question: str, results: str):

        # LLM 전달을 위한 chunk 병합
        join_context = build_context(results, 3000) # TODO 길이는 환경변수로 빼야함
        
        # 조회된 chunk 없을 경우 처리
        if len(join_context) == 0:
            yield f"data: [TOKEN]내부의 관련 자료를 찾을수 없습니다. \n\n"
            time.sleep(0.5)
            yield f"data: [DONE]"
            return

        messages = []
        # system message 영역
        system_block = {
            "role": "system",
            "content": get_system_content()
        }
        
        # history message 영역
        # TODO 문맥 유지를 위해 이전 5개 정도의 대화 내역 가져오기

        # question message 영역
        question_block = {
            "role": "user",
            "content": get_user_content(question, join_context)
        }

        messages.append(system_block)
        # TODO 대화 이력 셋팅
        messages.append(question_block)

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }

        logger.debug("LLM 최종 요청 값: %s", payload)

        try:
            r = requests.post(
                self.url, 
                json=payload, 
                stream=True,
                timeout=(5, 60) # (connect timeout, read timeout)
            )

            if r.status_code != 200:

                logger.debug("llm status_code: %s", r.status_code)
                logger.debug("llm massage: %s", r.text)

                yield f"data: [ERROR]llm 요청 처리중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
                return

            #전체 답변
            full_answer = ""
            
            # 질문 TOKEN 전달
            for line in r.iter_lines():
                if line:
                    data = json.loads(line)

                    logger.debug("LLM TOKEN 응답값: %s", data)

                    if data.get("done"):
                        break

                    if "message" in data:
                        content = data["message"]["content"]
                        if content == "":
                            continue
                        full_answer += content
                        yield f"data: [TOKEN]{content}\n\n"

            # 참조 문서 내역 전달
            for idx, r in enumerate(results):
                reference = {
                    "page": r["page"],
                    "file_name": r["doc"],
                    "uid": r["uid"],
                    "content": r["content"]
                }
                
                yield f"data: [REFERENCE]{reference}\n\n"

            logger.debug("# 답변 완성값: \n %s", full_answer)

            # 완료 처리
            yield f"data: [DONE]\n\n"

        except requests.exceptions.ConnectTimeout:
            logger.exception("LLM 연결 timeout")
            yield f"data: [ERROR]llm 연결이 지연되고 있습니다. 잠시 후 다시 시도해 주세요. \n\n"
            return
        except requests.exceptions.ReadTimeout:
            logger.exception("LLM 응답 timeout")
            yield f"data: [ERROR]llm 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요. \n\n"
            return
        except requests.exceptions.ConnectionError:
            logger.exception("LLM 서버 연결 실패")
            yield f"data: [ERROR]llm 서버 연결에 실패하였습니다. 잠시 후 다시 시도해 주세요. \n\n"
            return
        except Exception as e:
            logger.exception("기타에러: %s", str(e))
            yield f"data: [ERROR]일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요. \n\n"
            return

    def save_chat_history(self, question, answer):
        logger.debug("채팅 내역 DB 저장!!!!")
        logger.debug("Q:%s", question)
        logger.debug("A:%s", answer)