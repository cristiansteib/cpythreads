from abc import ABC, abstractmethod


class ThreadRunnable(ABC):
    @abstractmethod
    def run(self):
        ...
