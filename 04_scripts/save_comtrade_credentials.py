"""Persist Comtrade API credentials to a user-local env file.

Usage:

    COMTRADE_API_KEY_1=... COMTRADE_API_KEY_2=... \
    /Users/elgask0/miniconda/bin/python 04_scripts/save_comtrade_credentials.py

By default this writes to ``~/.config/comtrade/credentials.env`` with ``0600``
permissions so local automations can reuse the keys without committing them.
"""

from __future__ import annotations

import os
from pathlib import Path

from comtrade_auth import load_comtrade_keys


DEFAULT_TARGET = Path.home() / ".config" / "comtrade" / "credentials.env"


def main() -> None:
    keys = load_comtrade_keys()

    target = Path(os.environ.get("COMTRADE_ENV_FILE", DEFAULT_TARGET)).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"COMTRADE_API_KEY_{idx}={key}" for idx, key in enumerate(keys, start=1)]
    target.write_text("\n".join(lines) + "\n")
    os.chmod(target, 0o600)

    print(f"Saved {len(keys)} Comtrade key(s) to {target}")


if __name__ == "__main__":
    main()
