"""Comtrade credential loading helpers.

Keep API keys outside the repository. Supported sources, in priority order:

1. Environment variables:

       COMTRADE_API_KEYS="key1,key2"

   or individual variables such as ``COMTRADE_API_KEY_1`` and
   ``COMTRADE_API_KEY_2``.

2. A user-local env file referenced by ``COMTRADE_ENV_FILE`` or one of the
   default paths:

       ~/.config/comtrade/credentials.env
       ~/.config/comtrade.env
       ~/.comtrade.env

   The file should contain standard ``KEY=value`` lines.

3. Optional macOS Keychain entries under one of these service names:

       COMTRADE_API_KEYS
       COMTRADE_API_KEY
       COMTRADE_API_KEY_1
       COMTRADE_API_KEY_2
       comtrade
       comtrade-api
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


DEFAULT_ENV_PATHS = (
    Path.home() / ".config" / "comtrade" / "credentials.env",
    Path.home() / ".config" / "comtrade.env",
    Path.home() / ".comtrade.env",
)

KEY_NAMES = ("COMTRADE_API_KEY", "COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2")
KEYCHAIN_SERVICES = (
    "COMTRADE_API_KEYS",
    "COMTRADE_API_KEY",
    "COMTRADE_API_KEY_1",
    "COMTRADE_API_KEY_2",
    "comtrade",
    "comtrade-api",
)


def _extend_combined(keys: list[str], combined: str) -> None:
    keys.extend(
        item.strip()
        for item in combined.replace(";", ",").split(",")
        if item.strip()
    )


def _parse_env_file(path: Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return parsed

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip("'").strip('"')
        if name:
            parsed[name] = value
    return parsed


def _load_from_env_file() -> list[str]:
    configured = os.environ.get("COMTRADE_ENV_FILE", "").strip()
    candidates = [Path(configured).expanduser()] if configured else list(DEFAULT_ENV_PATHS)

    for path in candidates:
        if not path.exists():
            continue
        values = _parse_env_file(path)
        keys: list[str] = []
        _extend_combined(keys, values.get("COMTRADE_API_KEYS", ""))
        for name in KEY_NAMES:
            value = values.get(name, "").strip()
            if value:
                keys.append(value)
        deduped = list(dict.fromkeys(keys))
        if deduped:
            return deduped
    return []


def _load_from_keychain() -> list[str]:
    if os.uname().sysname != "Darwin":
        return []

    keys: list[str] = []
    for service in KEYCHAIN_SERVICES:
        try:
            result = subprocess.run(
                ["security", "find-generic-password", "-w", "-s", service],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            return []
        if result.returncode != 0:
            continue
        secret = result.stdout.strip()
        if not secret:
            continue
        if service == "COMTRADE_API_KEYS":
            _extend_combined(keys, secret)
        else:
            keys.append(secret)
    return list(dict.fromkeys(keys))


def load_comtrade_keys() -> list[str]:
    keys: list[str] = []

    combined = os.environ.get("COMTRADE_API_KEYS", "")
    _extend_combined(keys, combined)

    for name in KEY_NAMES:
        value = os.environ.get(name, "").strip()
        if value:
            keys.append(value)

    if not keys:
        keys.extend(_load_from_env_file())

    if not keys:
        keys.extend(_load_from_keychain())

    deduped = list(dict.fromkeys(keys))
    if not deduped:
        raise RuntimeError(
            "No Comtrade API key configured. Set COMTRADE_API_KEYS or "
            "COMTRADE_API_KEY_1/COMTRADE_API_KEY_2, provide COMTRADE_ENV_FILE, "
            "populate ~/.config/comtrade/credentials.env, or store a matching "
            "macOS Keychain secret."
        )
    return deduped
