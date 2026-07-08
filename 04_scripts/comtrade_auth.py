"""Comtrade credential loading helpers.

Keep API keys outside the repository. Set either:

    COMTRADE_API_KEYS="key1,key2"

or individual variables such as ``COMTRADE_API_KEY_1`` and
``COMTRADE_API_KEY_2`` before running download scripts.
"""

import os


def load_comtrade_keys() -> list[str]:
    keys: list[str] = []

    combined = os.environ.get("COMTRADE_API_KEYS", "")
    keys.extend(
        item.strip()
        for item in combined.replace(";", ",").split(",")
        if item.strip()
    )

    for name in ("COMTRADE_API_KEY", "COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"):
        value = os.environ.get(name, "").strip()
        if value:
            keys.append(value)

    deduped = list(dict.fromkeys(keys))
    if not deduped:
        raise RuntimeError(
            "No Comtrade API key configured. Set COMTRADE_API_KEYS or "
            "COMTRADE_API_KEY_1/COMTRADE_API_KEY_2 before running downloads."
        )
    return deduped
