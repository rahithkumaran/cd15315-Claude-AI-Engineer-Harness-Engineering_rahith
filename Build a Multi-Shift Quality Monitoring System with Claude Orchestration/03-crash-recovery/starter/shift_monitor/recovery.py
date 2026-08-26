"""Resume-vs-fresh decision logic for crash recovery.

The 30-minute threshold is ~1/16 of an 8-hour shift cycle: a resume inside this
window is still operating on the same shift's working set; anything older is
treated as a stale partial that should be re-started from scratch with whatever
findings the manifest already captured injected as a summary.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Literal

from .manifest import ManifestState

# 30-minute threshold for resume window: ~1/16 of an 8-hour shift.
# Resumes within this window operate on the same shift's working set;
# anything older is treated as stale and restarts fresh with manifest summary injected.
STALE_RESUME_THRESHOLD_MINUTES = 30

Decision = Literal["resume", "fresh"]


def decide(state: ManifestState, now: datetime) -> Decision:
    # Case 1: Empty manifest
    if not state.steps:
        return "fresh"

    # Case 2: Manifest is complete
    if state.complete:
        return "fresh"

    # Case 3: Incomplete manifest — check staleness
    last_step_ts = state.steps[-1].ts
    time_since_last = now - last_step_ts
    threshold = timedelta(minutes=STALE_RESUME_THRESHOLD_MINUTES)

    if time_since_last <= threshold:
        return "resume"
    else:
        return "fresh"
