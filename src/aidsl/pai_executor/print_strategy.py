from abc import ABC, abstractmethod

from aidsl.shared.procols import Printable


class PrintStrategy(ABC):
    @abstractmethod
    def print(self, value: Printable):
        pass


class ConsolePrintStrategy(PrintStrategy):
    def print(self, value: Printable):
        print(value)


class DoNothingPrintStrategy(PrintStrategy):
    def print(self, value: Printable):
        pass
