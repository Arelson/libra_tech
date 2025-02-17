from abc import ABC, abstractmethod

# Interface para ações
class Action(ABC):
    @abstractmethod
    def execute(self):
        pass