"""Three invocation shapes.

thin     — prompt only.
rich     — hot state + new defects.
resumed  — prior partial findings + new defects since the last manifest step.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from .state import HotState

InvocationShape = Literal["thin", "rich", "resumed"]


@dataclass(frozen=True)
class Invocation:
    shape: InvocationShape
    prompt: str


def thin(prompt: str) -> Invocation:
    return Invocation(shape="thin", prompt=prompt)


def rich(
    role: str, hot_state: HotState, new_defects: Sequence[Mapping[str, Any]]
) -> Invocation:
    lines = [
        f"You are the on-call {role} for Northridge Plant 3.",
        "",
        "## Current hot state",
        "",
        f"Recent defect hashes: {hot_state.recent_defect_hashes}",
        f"Current shift summary: {hot_state.current_shift_summary or '(none)'}",
        f"Active alerts: {hot_state.active_alerts or '(none)'}",
        f"Threshold statuses: {hot_state.threshold_statuses or '(none)'}",
        "",
        "## New defects since last shift",
        "",
    ]

    if new_defects:
        for d in new_defects:
            lines.append(
                f"- {d['id']} ({d['ts']}, shift {d['shift']}): "
                f"{d['component']} / {d['severity']} — {d['description']}"
            )
    else:
        lines.append("- (none)")

    lines.extend(
        [
            "",
            "## Your analysis",
            "",
            "Please provide:",
            "- **Summary**: One-line summary of the situation.",
            "- **Findings**: Key observations from the new defects and trends.",
            "- **Recommended actions**: What should the quality team focus on?",
            "- **Updated hot state**: Propose an updated JSON representation of the hot state for the next shift.",
            "",
            "Format the updated hot state as a JSON block:",
            "```json",
            "{ \"current_shift_summary\": \"...\", \"active_alerts\": [...], \"threshold_statuses\": {...} }",
            "```",
        ]
    )

    prompt = "\n".join(lines)
    return Invocation(shape="rich", prompt=prompt)


def resumed(
    session_id: str,
    summary: str,
    latest_message: str,
    prior_steps: Sequence[Mapping[str, Any]],
    new_defects: Sequence[Mapping[str, Any]],
) -> Invocation:
    lines = [
        "## Prior partial findings",
        "",
    ]

    if prior_steps:
        for step in prior_steps:
            name = step.get("name", "unknown")
            payload = step.get("payload", "")
            truncated = (payload[:100] + "...") if len(str(payload)) > 100 else str(payload)
            lines.append(f"- {name}: {truncated}")
    else:
        lines.append("- (none)")

    lines.extend(
        [
            "",
            "## Prior summary",
            "",
            summary,
            "",
            "## New defects since last partial step",
            "",
        ]
    )

    if new_defects:
        for d in new_defects:
            lines.append(
                f"- {d['id']} ({d['ts']}): {d['component']} / {d['severity']} — {d['description']}"
            )
    else:
        lines.append("- (none)")

    lines.extend(
        [
            "",
            "## Latest instruction",
            "",
            latest_message,
        ]
    )

    prompt = "\n".join(lines)
    return Invocation(shape="resumed", prompt=prompt)
