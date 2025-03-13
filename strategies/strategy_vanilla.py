from .strategy import Strategy
from agents import AgentLlama3
from ..data.get10KSections import SEC10KExtractor
import json

class StrategyVanilla(Strategy):
    INSTRUCTION_PATH = "prompts/strategy_vanilla.json"
    CATEGORY_PATH = "prompts/categories.json"
    def __init__(self, ticker = 'NVDA'):
        self.agent = AgentLlama3()
        with open(StrategyVanilla.INSTRUCTION_PATH, "r") as f:
            self.prompts = json.load(f)
        with open(StrategyVanilla.CATEGORY_PATH, "r") as f:
            self.categories = json.load(f)
        self.doc_retriever = SEC10KExtractor()
        self.ticker = ticker

    # Step 1
    def _get_necessary_documents(self, user_query):
        USER_PROMPT = self.prompts['get_necessary_documents'].format(user_query=user_query, categories=str(self.categories))
        return self.agent.ask(USER_PROMPT).split("<begin of answer>")[1].split("<end of answer>")[0].replace("\n", "").strip()
    
    # Step 2
    def _get_doc_details(self, list_docs):
        details_dict = self.doc_retriever.getSectionsByName(ticker=self.ticker, sections=list_docs)
        return details_dict

    # Step 3
    def execute_strategy(self, user_query):
        try: list_docs = eval(self._get_necessary_documents(user_query))
        except: list_docs = ["Business"]
    
        docs_details = """"""
        details_dict = self._get_doc_details(list_docs)
        for doc_id in list_docs: docs_details += doc_id +"\n\n" + details_dict[doc_id] + "\n-----------------------------"
    
        GET_ANSWER_PROMPT = self.prompts['get_answer'].format(docs_details=docs_details, user_query=user_query)
        return self.agent.ask(GET_ANSWER_PROMPT)

        