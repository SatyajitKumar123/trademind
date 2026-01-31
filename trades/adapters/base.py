import csv
from abc import ABC, abstractmethod
from typing import Iterable, TextIO


class BrokerAdapter(ABC):
    """
    Base contract for all broker adapters.
    """

    def get_reader(self, file: TextIO) -> Iterable[dict]:
        """
        Returns a DictReader for the broker CSV.
        """
        return csv.DictReader(file)

    @abstractmethod
    def normalize(self, row: dict):
        """
        Convert a broker-specific CSV row into TradeDTO.
        """
        raise NotImplementedError
