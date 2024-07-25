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