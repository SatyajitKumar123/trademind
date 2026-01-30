from abc import ABC, abstractmethod
from typing import Dict

from trades.domain.trade_dto import TradeDTO


class BrokerAdapter(ABC):
    @abstractmethod
    def normalize(self, row: Dict) -> TradeDTO:
        """Convert broker-specific row to TradeDTO"""
        raise NotImplementedError
