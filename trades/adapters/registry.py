from trades.adapters.zerodha import ZerodhaAdapter

_ADAPTERS = {
    "zerodha": ZerodhaAdapter(),
}


def get_adapter(broker: str):
    try:
        return _ADAPTERS[broker.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported broker: {broker}") from exc
