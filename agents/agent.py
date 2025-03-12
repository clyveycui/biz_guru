from abc import ABC, abstractmethod

# Just a template, you can either inherit or build something similar to this
class Agent(ABC):
    @abstractmethod
    def ask(self):
        pass