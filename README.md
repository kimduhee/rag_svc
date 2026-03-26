# 환경구성
+ Framework: Fast API(0.128.0)
+ lang: Python(3.12.0)

# 설치
### python
+ https://www.python.org
+ 상단 메뉴에서 'Downloads'
+ 운영체제(Windows, macOS, Linux)에 맞는 버전의 설치 파일 다운로
+ 설치중 'Add Python to PATH' 옵션 체크

### FastAPI, Uvicorn(서버) 설치
<pre><code>설치
pip install fastapi uvicorn

실행
uvicorn app.main:app --reload
</code></pre>
+ app.main: 메인 파일 명
+ FastAPI: 객체 이름
+ --reload: 코드 변경 시 자동 재시작

### ollama
+ https://ollama.com/download
+ OllamaSetup.exe 설치
<pre><code>버전 확인
ollama --version or ollama -v</code></pre>
<pre><code>설치 모델 확인
ollama list</code></pre>
<pre><code>모델 설치
ollama run llama3.1:8b</code></pre>
<pre><code>모델 삭제
ollama rm llama3.1:8b</code></pre>


# 모델 및 라이브러리
+ Embedding Model: BAAI/bge-m3
+ Vector Database: Elasticsearch
+ Retrieval: Hybrid Search (BM25 + kNN)
+ LLM: llama3.1:8b (Ollama)
+ Vision Model: llava

# 기능구현
### 파일 업로드
+ 추후 백엔드 서버에서 파일 업로드 후 문서의 유일값(UUID)을 채번하여 파일경로와 함께 요청
+ PDF, Excel 파일 등 문서 업로드

### 문서 로딩
+ PDF: pdfplumber
+ Excel: openpyxl

### 임베딩
+ BAAI/bge-m3 모델 임베딩 처리
+ SentenceTransformer

### 답변 생성
+ 질문에 대해 LLM에 답변 요청
+ Hybrid 검색(bm25+knn)
<pre><code>[화면]
질문요청
 ↓
[백엔드]
LLM 플랫폼에 질문요청
 ↓
[LLM플랫폼]
질문 문자 임베딩 → Elasticsearch 검색(bm25+knn) → LLM에 질의(Ollama_llama3.1:8b)
 ↓
[event-stream]
 ↓
[백엔드]
화면에 답변 TOKEN 전송 → 출처문서 전송 → 질문/답변/출처문서 내역 DB저장
 ↓
[화면]
event-stream 기반 답변 및 출처문서 view
</code></pre>


# 실행
### PDF 문서내 이미지 추출 및 저장, 벡터DB(Elasticsearch) 저장
<img width="1510" height="240" alt="Image" src="https://github.com/user-attachments/assets/649490f1-cbe5-4cba-af2f-e57d525979c5" />

### 질문에 대한 vertorDB 조회
<img width="1136" height="437" alt="Image" src="https://github.com/user-attachments/assets/2f859cd3-b31e-4c37-b984-203d05a33b20" />

### 질문에 대한 LLM 답변
<img width="1515" height="423" alt="Image" src="https://github.com/user-attachments/assets/33ebd737-a465-4c77-bbc8-1e42f71b9d63" />

### 화면에 전달되는 데이터(답변token 및 출처문서정보)
<img width="1276" height="339" alt="Image" src="https://github.com/user-attachments/assets/fb054745-7861-41cd-a2a6-79c954140750" />








