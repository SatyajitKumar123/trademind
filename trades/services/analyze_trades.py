from trades.domain.fifo_engine import FIFOMatchingEngine
from trades.domain.trade_dto import TradeDTO
from trades.services.pnl_service import persist_realized_pnl


def analyze_trades(trades: list[TradeDTO]) -> int:
    engine = FIFOMatchingEngine()
    realized = engine.process(trades)
    return persist_realized_pnl(realized)
