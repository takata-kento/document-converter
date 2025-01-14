import base64
from os import environ

from injector import singleton
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import HumanMessagePromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI

from packages.domain.image_summarizer import ImageSummarizer

@singleton
class AzureOaiImgSummarizer(ImageSummarizer):
    def __init__(self) -> None:
        self.key = environ.get('AZURE_OPENAI_API_KEY')
        self.endpoint = environ.get('AZURE_OPENAI_ENDPOINT')
        self.api_version = environ.get('AZURE_OPENAI_API_VERSION')
        self.deployment = environ.get('AZURE_OPENAI_DEPLOYMENT')

    def summarize(
            self,
            img_path: str
    ) -> str:
        llm = AzureChatOpenAI(
            azure_endpoint = self.endpoint,
            azure_deployment = self.deployment,
            openai_api_version = self.api_version
        )

        with open(img_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')

        image_template = {"image_url": {"url": f"data:image/png;base64,{img_base64}"}}

        system = (
            "あなたは有能なアシスタントです。ユーザーの問いに回答してください"
        )
        human_prompt = "{question}"
        human_message_template = HumanMessagePromptTemplate.from_template([human_prompt, image_template])
        prompt = ChatPromptTemplate([("system", system), human_message_template])

        chain = prompt | llm

        res = chain.invoke({"question": "何についての画像なのか、内容を要約して回答してください。"})

        return res.content
