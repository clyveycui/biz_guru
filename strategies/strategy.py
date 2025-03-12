from abc import ABC, abstractmethod

# Just a template, you can either inherit or build something similar to this
class Strategy(ABC):
    @abstractmethod
    def init_agent_workers(self):
        pass

    @abstractmethod
    def execute_strategy(self):
        pass
