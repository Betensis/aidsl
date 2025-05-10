from aidsl.pai_executor.print_strategy import PrintStrategy


class SpyPrintStrategy(PrintStrategy):
    def __init__(self):
        self.__printed_values = []

    def print(self, value):
        self.__printed_values.append(value)

    def get_printed_values(self):
        return self.__printed_values
