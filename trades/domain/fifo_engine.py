from collections import deque
from decimal import Decimal

from trades.domain.position_lot import PositionLot
from trades.domain.realized_pnl import RealizedPnL
from trades.domain.trade_dto import TradeDTO


class FIFOMatchingEngine:
    def process(self, trades: list[TradeDTO]) -> list[RealizedPnL]:
        open_positions: dict[str, deque[PositionLot]] = {}
        realized: list[RealizedPnL] = []

        for trade in trades:
            if trade.side == "BUY":
                open_positions.setdefault(trade.symbol, deque()).append(
                    PositionLot(
                        symbol=trade.symbol,
                        quantity=trade.quantity,
                        price=trade.price,
                    )
                )

            elif trade.side == "SELL":
                remaining_qty = trade.quantity
                lots = open_positions.get(trade.symbol, deque())

                while remaining_qty > 0 and lots:
                    lot = lots[0]
                    matched_qty = min(lot.quantity, remaining_qty)

                    pnl = (trade.price - lot.price) * Decimal(matched_qty)

                    realized.append(
                        RealizedPnL(
                            symbol=trade.symbol,
                            quantity=matched_qty,
                            buy_price=lot.price,
                            sell_price=trade.price,
                            pnl=pnl,
                        )
                    )

                    lot.quantity -= matched_qty
                    remaining_qty -= matched_qty

                    if lot.quantity == 0:
                        lots.popleft()

        return realized
