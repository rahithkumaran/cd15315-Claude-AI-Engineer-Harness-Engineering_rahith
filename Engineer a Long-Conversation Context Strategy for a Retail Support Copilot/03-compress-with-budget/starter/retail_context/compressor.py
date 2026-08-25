"""Tiered compression: summarize resolved segments; preserve active verbatim.

Resolved segments are condensed by a single Claude call per segment using the
prompt template at `retail_context/prompts/compression_prompt.md`. The active
segment is **never** summarized — it is preserved byte-exact.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import resources

from retail_context.client import complete_with_system
from retail_context.transcript import Segment, Transcript


@dataclass
class Summary:
    issue_id: str
    text: str
    input_tokens: int
    output_tokens: int


@dataclass
class Compressed:
    summaries: dict[str, Summary]
    active_text: str
    active_issue_id: str


def _load_prompt() -> str:
    return resources.files("retail_context.prompts").joinpath(
        "compression_prompt.md"
    ).read_text()


def summarize_segment(segment: Segment, *, model: str | None = None) -> Summary:
    """Summarize ONE resolved segment via Claude."""
    # Guard: only compress resolved segments
    if segment.status != "resolved":
        raise ValueError(
            f"Cannot compress segment {segment.issue_id}: status={segment.status}. "
            "Only 'resolved' segments are compressed. The active segment must be preserved byte-exact."
        )

    # Load compression prompt
    system_prompt = _load_prompt()

    # Build user message with segment context
    user_message = (
        f"Source segment — issue_id `{segment.issue_id}`, turns "
        f"{segment.turn_range[0]}-{segment.turn_range[1]}:\n\n{segment.text}"
    )

    # Call Claude for summarization
    response_text, input_tokens, output_tokens = complete_with_system(
        system_prompt, user_message, model=model, max_tokens=1024
    )

    # Return Summary with token counts
    return Summary(
        issue_id=segment.issue_id,
        text=response_text,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


def compress(transcript: Transcript, *, model: str | None = None) -> Compressed:
    """Orchestrate compression across all segments."""
    summaries: dict[str, Summary] = {}
    active_text: str | None = None
    active_issue_id: str | None = None

    for segment in transcript.segments:
        if segment.status == "resolved":
            # Compress resolved segments
            summary = summarize_segment(segment, model=model)
            summaries[segment.issue_id] = summary
        elif segment.status == "active":
            # Preserve active segment byte-exact
            active_text = "\n\n".join(t.render() for t in segment.turns)
            active_issue_id = segment.issue_id

    # Ensure exactly one active segment exists
    if active_text is None or active_issue_id is None:
        raise RuntimeError(
            "No active segment found in transcript. The assembled context requires "
            "exactly one active segment at the bottom boundary."
        )

    return Compressed(
        summaries=summaries,
        active_text=active_text,
        active_issue_id=active_issue_id,
    )
