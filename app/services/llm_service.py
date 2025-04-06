from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from app.core.config import settings
from sqlalchemy.orm import Session

from app.models.contract_keyword import ContractKeyword
from app.repositories.contract_keyword import ContractKeywordRepository


class LLMService:
    def __init__(self, db: Session):
        self.db = db
        self.api_key = settings.OPENAI_API_KEY
        self.llm = ChatOpenAI(openai_api_key=self.api_key)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

    """
         텍스트 파일에서 계약 키워드 추출, 저장
    """
    async def extract_contract_keywords(self, transcription: str, client_id: int):
        result = self.query_llm(transcription, self.setup_question())
        result_dict = self.result_parsing(result)

        keyword_model = ContractKeyword(client_id=client_id,
                                        construction_type=result_dict.get("construction_type"),
                                        construction_cost=result_dict.get("construction_cost"),
                                        start_date=result_dict.get("start_date"),
                                        end_date=result_dict.get("end_date"))

        ContractKeywordRepository.save(self.db, keyword_model)

    def query_llm(self, transcription: str, question: str):
        vectorstore = self._setup_vectorstore(transcription)
        chain = self._setup_chain(vectorstore)
        return chain.invoke(question).content

    @staticmethod
    def setup_question():
        return """
                이 텍스트에서 다음 정보를 추출하세요. 정보가 없으면 "unknown"이라고 답하세요.
                1. 공사 종류:
                2. 공사 비용:
                3. 작업 시작일:
                4. 작업 종료일:
                """

    def _setup_vectorstore(self, text: str):
        docs = [Document(page_content=text)]
        return FAISS.from_documents(docs, self.embeddings)

    def _setup_chain(self, vectorstore):
        # 검색기 설정
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # 문서 매핑 프롬프트
        map_doc_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                다음 문서 부분을 사용하여 질문에 관련된 내용이 있는지 확인하세요.
                관련 텍스트가 있으면 그대로 반환하고, 없으면 'unknown'이라고 반환하세요.
                간결하고 직접적인 답변을 제공하세요.
                -------
                {context}
                """,
            ),
            ("human", "{question}"),
        ])

        # 문서 매핑 체인
        map_doc_chain = map_doc_prompt | self.llm

        # 검색된 문서 처리 함수
        def map_docs(inputs):
            documents = inputs["documents"]
            question = inputs["question"]
            return "\n\n".join(
                map_doc_chain.invoke({
                    "context": doc.page_content,
                    "question": question
                }).content
                for doc in documents
            )

        # 문서 매핑 설정
        map_chain = {
                        "documents": retriever,
                        "question": RunnablePassthrough(),
                    } | RunnableLambda(map_docs)

        # 최종 답변 생성 프롬프트
        final_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                다음 문서 부분과 질문을 바탕으로 최종 답변을 생성하세요.
                질문과 동일한 언어로 답변하세요.
                ------
                {context}
                """,
            ),
            ("human", "{question}"),
        ])

        # 최종 체인
        return {"context": map_chain, "question": RunnablePassthrough()} | final_prompt | self.llm

    @staticmethod
    def result_parsing(result: str) -> dict:
        lines = result.splitlines()
        construction_type = lines[0].split(": ")[1].strip()
        construction_cost = lines[1].split(": ")[1].strip()
        start_date = lines[2].split(": ")[1].strip()
        end_date = lines[3].split(": ")[1].strip()

        return {
            "construction_type": construction_type,
            "construction_cost": construction_cost,
            "start_date": start_date,
            "end_date": end_date,
        }