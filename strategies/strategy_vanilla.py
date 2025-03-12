from strategy import Strategy
from agents import AgentLlama3
import json

# The strategy mimics a one supervisor many expert setting.
# One agent acting as the supervisor makes the final decision
# Multiple agents acting as experts provide advice (expert opinion) to the supervisor regarding specific areas they are experts in
# All info/data is distributed to all agents
class StrategyVanilla(Strategy):
    INSTRUCTION_PATH = "prompts/strategy_vanilla_instructions.json"
    SUPERVISOR_PROMPT_FORMAT = "{advices}\n{question}"
    def __init__(self, data):
        self.data = data
        self.experts = {}
        self.supervisor = None

    def init_agents(self):
        instructions = None
        with open(StrategyVanilla.INSTRUCTION_PATH, "r") as f:
            instructions = json.load(f)

        supervisor_instruction = instructions['supervisor'].format(report = self.data['report'])
        risk_expert_instruction = instructions['risk_expert'].format(report = self.data['report'])
        biz_expert_instruction = instructions['biz_expert'].format(report = self.data['report'])

        self.supervisor = AgentLlama3(sys_instruction=supervisor_instruction)
        self.experts['risk'] = AgentLlama3(sys_instruction=risk_expert_instruction)
        self.experts['business'] = AgentLlama3(sys_instruction=biz_expert_instruction)
    
    def execute_strategy(self, question):
        advices = []
        for agent_name, agent in self.experts.items():
            advice = agent.ask(question)
            s = f"{agent_name} expert: {advice}"
            print(s)
            advices.append(s)
        supervisor_prompt = StrategyVanilla.SUPERVISOR_PROMPT_FORMAT.format(advices="\n".join(advices), question=question)
        response = self.supervisor.ask(supervisor_prompt)
        return response

        