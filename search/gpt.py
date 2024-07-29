from openai import OpenAI
from environ import Env
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

env = Env()
env.read_env()

OPEN_AI_PROJECT_KEY=env('OPEN_AI_PROJECT_KEY')

class KeywordExtractor:
    def __init__(self):
        
        self.llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPEN_AI_PROJECT_KEY)
        self.prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template="""
                This GPT extracts key keywords from product information provided by the user. 
                It identifies the most important and relevant terms that describe the product's features, benefits, and unique selling points. 
                The GPT focuses on clarity and precision, ensuring the extracted keywords are concise and relevant. 
                It avoids unnecessary details or overly technical language unless specified. 
                When extracting keywords, it categorizes them into ORGANISATION, QUANTITY, FASHION, HOME, SPORTS, ELECTRONICS, BEAUTY, AUTOMOBILE, EXTRA, and FEATURE as appropriate. 
                For example, 'Paper Plane Women's Rain Boots Fashion Lightweight Comfortable Rain Boots PP1522' would yield keywords like 'Rain Boots', '여자장화', and categorize 'Paper Plane' as ORGANISATION, 'Women's', 'Lightweight', and 'Comfortable' as FEATURE, and exclude product numbers like 'PP1522'.
                Additionally, it calculates the percentage relevance of each primary category (excluding FEATURE, QUANTITY, and ORGANISATION) and includes it in the output. 
                For instance, for a 'MONAMI whiteboard marker', it would identify 'marker' as a key keyword and categorize the product into the EXTRA category. 
                Return the results in the following JSON format: 
                {{ "PRODUCT": 
                    "<Product Name>", 
                    "KEYWORDS": ["<Keyword1>", "<Keyword2>", ...], 
                    "CATEGORIES": {{ 
                        "ORGANISATION": ["<Organisation>", ...], 
                        "QUANTITY": ["<Quantity1>",...], 
                        "FASHION": ["<Fashion1>", ...], 
                        "HOME": ["<Home1>", ...], 
                        "SPORTS": ["<Sports>", ...], 
                        "ELECTRONICS": ["<Electronics>", ...], 
                        "BEAUTY": ["<Beauty>", ...], 
                        "AUTOMOBILE": ["<Automobile>", ...], 
                        "EXTRA": ["<EXTRA>", ...], 
                        "FEATURE": ["<Feature1>", "<Feature2>", ...] 
                    }}, 
                    "EXCLUDED": ["<Excluded1>", "<Excluded2>", ...], 
                    "PERCENTAGE": {{
                        <Category>: <Percentage>, ... 
                    }}
                }}
        
            {user_input}
            """
        )
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def extract_keywords(self, user_input):
        response = self.llm_chain.run({"user_input": user_input})
        return response
    

class CoreWordExtractor:
    def __init__(self):
        
        self.llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPEN_AI_PROJECT_KEY)
        self.prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template="""
                This GPT identifies the core word or concept from a given product name. 
                It should extract only the most essential word representing the product itself. 
                For example, from '삼성 갤럭시 S21 바이올렛 256GB,' the core word is 'S21.' 
                For 'Attack Shark R1 블루투스 마우스, 18000dpi, PAW3311, 트라이 모드 연결, 매크로 게이밍 마우스, 1000Hz,' the core word is '마우스.' 
                For '레노버 TH30 무선 헤드폰 블루투스 5.3 이어폰 접이식 게임 헤드셋 스포츠 헤드폰 마이크 음악 이어폰 250mAh,' the core word is '무선 헤드셋.' 
                Avoid extracting company names, additional descriptions, or product features. 
                For 'Baseus 차량용 디퓨저 가습기, 자동 공기 청정기, LED 조명, 아로마 테라피,' the core word is '디퓨저 가습기.'
                Return the results in the following JSON format: 
                {{ "COREWORD" : <CoreWord> }}
        
            {user_input}
            """
        )
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def extract_corewords(self, user_input):
        response = self.llm_chain.run({"user_input": user_input})
        return response
    

class ProductCategorizer:
    def __init__(self):
        
        self.llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPEN_AI_PROJECT_KEY)
        self.prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template="""
                This GPT identifies the category of a given product name from seven categories: FASHION, HOME, ELECTRONICS, BEAUTY, SPORTS, AUTOMOBILE, and EXTRA. 
                It outputs the category in JSON format with the key 'CATEGORY_ID'. 
                If the product name isn't clear, it returns an error message in JSON format. 
                It strictly provides the category or an error message.
        
                {user_input}
            """
        )
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def categorizer(self, user_input):
        response = self.llm_chain.run({"user_input": user_input})
        return response