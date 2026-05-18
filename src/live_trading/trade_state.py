from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

from config.live_config import LiveConfig


@dataclass
class PositionState:
    symbol: str
    side: str
    entry_date: str
    sentiment_value: float
    sentiment_strength: float
    hold_days: int
    lot: float

    @property
    def exit_date(self) -> str:
        dt = datetime.fromisoformat(self.entry_date) + timedelta(days=self.hold_days)
        return dt.date().isoformat()


def _state_path() -> Path:
    path = Path(LiveConfig.STATE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_state() -> Dict[str, dict]:
    path = _state_path()
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: Dict[str, dict]) -> None:
    path = _state_path()
    with path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_position_state(symbol: str) -> Optional[PositionState]:
    state = load_state()
    raw = state.get(symbol)
    if raw is None:
        return None
    return PositionState(**raw)


def set_position_state(position: PositionState) -> None:
    state = load_state()
    state[position.symbol] = asdict(position)
    save_state(state)


def remove_position_state(symbol: str) -> None:
    state = load_state()
    state.pop(symbol, None)
    save_state(state)