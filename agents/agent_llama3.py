from vllm import LLM, SamplingParams
from agent import Agent

class AgentLlama3(Agent):
    SYSTEM_PROMPT_FORMAT= "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_instruction}"
    INTERACTION_PROMPT_FORMAT= "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    MAX_TOKENS = 200

    def __init__(self, sys_instruction, model_name="meta-llama/Llama-3.1-8B-Instruct"):
        self.sp = SamplingParams(temperature=0.3, top_p=0.9, max_tokens=AgentLlama3.MAX_TOKENS)
        self.model = LLM(model=model_name, tensor_parallel_size=1, trust_remote_code=True)
        self.sys_prompt = AgentLlama3.SYSTEM_PROMPT_FORMAT.format(sys_instruction)
        self.input_hist = []
        self.output_hist = []

    #Currently not aware of past interactions
    def ask(self, question):
        current_interaction = AgentLlama3.INTERACTION_PROMPT_FORMAT.format(user_prompt=question)
        outputs = self.model.generate(prompts=[self.sys_prompt + current_interaction], sampling_params=self.sp)
        response = outputs[0].outputs[0].text
        
        self.input_hist.append(question)
        self.output_hist.append(response)
        return response