"""Case-facts extraction into a persistent block at the top of context.

Extraction is LLM-driven: one Claude call against the full transcript that returns
strict JSON for the 12 required fields. This is commonly called a *scratchpad* — same
concept, different word: a dense structured block that survives compression and is
placed at the top boundary of context so the model can recover transactional facts
without scanning thousands of tokens of narrative.

Missing-field behavior raises `CaseFactExtractionError` listing the gaps — silent
null-fill is forbidden.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from retail_context.client import complete_with_system, get_model
from retail_context.transcript import Transcript

REQUIRED_FIELDS: tuple[str, ...] = (
    "customer_id",
    "refund_order_id",
    "refund_amount_usd",
    "refund_status",
    "subscription_id",
    "subscription_plan",
    "subscription_cancel_reason",
    "subscription_status",
    "active_payment_method_last4",
    "new_payment_method_last4",
    "payment_update_failure_code",
    "payment_update_status",
)


@dataclass
class CaseFacts:
    customer_id: str
    refund_order_id: str
    refund_amount_usd: float
    refund_status: str
    subscription_id: str
    subscription_plan: str
    subscription_cancel_reason: str
    subscription_status: str
    active_payment_method_last4: str
    new_payment_method_last4: str
    payment_update_failure_code: str
    payment_update_status: str

    def to_markdown(self) -> str:
        """Render the 12-field case facts block as Markdown."""
        lines = ["# Case Facts", ""]

        lines.append("**Customer:** " + self.customer_id)
        lines.append("")

        lines.append("**Refund (resolved):** Order " + self.refund_order_id +
                    f" — ${self.refund_amount_usd:.2f} — " + self.refund_status)
        lines.append("")

        lines.append("**Subscription (resolved):** " + self.subscription_plan +
                    " (" + self.subscription_id + ") — Cancelled: " +
                    self.subscription_cancel_reason + " — " + self.subscription_status)
        lines.append("")

        lines.append("**Payment update (active):** " + self.active_payment_method_last4 +
                    " → " + self.new_payment_method_last4 + " — " +
                    self.payment_update_failure_code + " — " + self.payment_update_status)

        return "\n".join(lines)


class CaseFactExtractionError(ValueError):
    def __init__(self, missing: list[str], raw: dict[str, Any]):
        super().__init__(f"case-facts extraction missing required fields: {missing}")
        self.missing = missing
        self.raw = raw


_SYSTEM_PROMPT = """Extract the following 12 fields from the customer support transcript into a strict JSON object.

**Extraction rules:**
1. Return ONLY a JSON object with exactly these 12 keys (no prose, markdown, or code fences):
   - customer_id (string: customer identifier)
   - refund_order_id (string: order identifier)
   - refund_amount_usd (number: refund amount)
   - refund_status (string: one of "processed", "pending", "denied", or "in_progress")
   - subscription_id (string: subscription identifier)
   - subscription_plan (string: subscription plan name)
   - subscription_cancel_reason (string: reason for cancellation)
   - subscription_status (string: one of "active", "cancelled", "cancelled_with_prorated_refund", etc.)
   - active_payment_method_last4 (string: zero-padded 4-digit card number)
   - new_payment_method_last4 (string: zero-padded 4-digit card number)
   - payment_update_failure_code (string: error code like "AVS_MISMATCH" or "TIMEOUT")
   - payment_update_status (string: one of "in_progress", "failed", "success", etc.)

2. Preserve all status tokens and identifiers EXACTLY as they appear in the transcript.
3. For numeric amounts, use the actual number (e.g., 22.14, not "22.14").
4. If a field is not mentioned in the transcript, use null (do NOT invent or guess).
5. Output is ONLY the JSON object, no additional text."""


def _parse_json(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.rstrip().endswith("```"):
            raw = raw.rsplit("```", 1)[0]
    return json.loads(raw)


def extract(
    transcript: Transcript,
    *,
    model: str | None = None,
    log_path: Path | None = None,
) -> CaseFacts:
    """Extract 12 case facts from the transcript via LLM call."""
    # Build user message
    user_message = f"Transcript:\n\n{transcript.full_text}"

    # Call complete_with_system
    response_text, input_tokens, output_tokens = complete_with_system(
        _SYSTEM_PROMPT, user_message, model=model, max_tokens=2048
    )

    # Parse JSON response
    parsed = _parse_json(response_text)

    # Log if requested
    if log_path:
        log_data = {
            "model": model or get_model(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "extracted": parsed,
        }
        log_path.write_text(json.dumps(log_data, indent=2))

    # Validate all required fields are present and non-empty
    missing = [
        field
        for field in REQUIRED_FIELDS
        if field not in parsed or parsed[field] is None or parsed[field] == ""
    ]
    if missing:
        raise CaseFactExtractionError(missing=missing, raw=parsed)

    # Construct and return CaseFacts with proper type casting
    return CaseFacts(
        customer_id=str(parsed["customer_id"]),
        refund_order_id=str(parsed["refund_order_id"]),
        refund_amount_usd=float(parsed["refund_amount_usd"]),
        refund_status=str(parsed["refund_status"]),
        subscription_id=str(parsed["subscription_id"]),
        subscription_plan=str(parsed["subscription_plan"]),
        subscription_cancel_reason=str(parsed["subscription_cancel_reason"]),
        subscription_status=str(parsed["subscription_status"]),
        active_payment_method_last4=str(parsed["active_payment_method_last4"]),
        new_payment_method_last4=str(parsed["new_payment_method_last4"]),
        payment_update_failure_code=str(parsed["payment_update_failure_code"]),
        payment_update_status=str(parsed["payment_update_status"]),
    )


def to_dict(facts: CaseFacts) -> dict[str, Any]:
    return asdict(facts)
