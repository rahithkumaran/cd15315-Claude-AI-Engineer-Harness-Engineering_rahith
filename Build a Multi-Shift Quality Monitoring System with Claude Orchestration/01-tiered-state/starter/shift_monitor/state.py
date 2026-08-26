"""Hot-state schema and atomic disk I/O."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, Field

MAX_RECENT_HASHES = 20
HOT_STATE_BYTE_BUDGET = 5_120


class HotState(BaseModel):
    """In-context shift state. Kept under ~5 KB so it fits in every prompt."""

    model_config = ConfigDict(frozen=True)

    recent_defect_hashes: list[str] = Field(default_factory=list, max_length=MAX_RECENT_HASHES)
    current_shift_summary: str = ""
    active_alerts: list[str] = Field(default_factory=list)
    threshold_statuses: dict[str, str] = Field(default_factory=dict)

    def to_json_bytes(self) -> bytes:
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def from_json_bytes(cls, payload: bytes) -> Self:
        return cls.model_validate_json(payload)

    @classmethod
    def from_path(cls, path: Path) -> Self:
        return cls.from_json_bytes(path.read_bytes())

    def write_atomic(self, path: Path) -> None:
        # Make sure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Serialize and check byte budget
        payload = self.to_json_bytes()
        if len(payload) > HOT_STATE_BYTE_BUDGET:
            raise ValueError(
                f"Serialized state is {len(payload)} bytes, exceeds budget of {HOT_STATE_BYTE_BUDGET}"
            )

        # Write to temp file in same directory, then atomically swap
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
            tmp.write(payload)
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp_path = tmp.name

        try:
            os.replace(tmp_path, path)
        except Exception:
            os.unlink(tmp_path)
            raise
