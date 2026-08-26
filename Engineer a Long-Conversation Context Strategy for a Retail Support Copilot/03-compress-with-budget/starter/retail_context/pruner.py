"""Deterministic tool-output pruning for the verbose `lookup_order` response.

The "Tool Context Pruning" pattern: application-side filtering
of a verbose tool result so only the fields needed for the immediate decision survive
into context. For return/refund reasoning, exactly five fields matter — order identity,
when it was placed, what it cost, whether it shipped, and the return-window deadline.

# Why each kept field is the only one that matters for return/refund reasoning:
#   - order_id: Identifies the order in all downstream systems and is required to process any return.
#   - order_date: Determines whether the order is within the return window and affects refund eligibility.
#   - order_total_usd: Sets the maximum refund amount and must match the original charge.
#   - fulfillment_status: Only delivered orders can be returned; other statuses bypass return logic.
#   - return_eligible_until: The explicit return deadline; if today > this date, the return is denied.

Implementation: deterministic field selection (no LLM call). The pruner has no
`anthropic` import — enforced by an AST audit.
"""
from __future__ import annotations

KEPT_FIELDS: tuple[str, ...] = (
    "order_id",
    "order_date",
    "order_total_usd",
    "fulfillment_status",
    "return_eligible_until",
)


class PrunerMissingFieldError(KeyError):
    """Raised when the raw tool response is missing one of the required kept fields."""


def prune_lookup_order(raw: dict) -> dict:
    """Prune verbose lookup_order response to exactly 5 decision-relevant fields.

    Raises PrunerMissingFieldError if any required field is missing from the raw dict.
    Returns dict with exactly KEPT_FIELDS in declaration order.
    """
    missing = [field for field in KEPT_FIELDS if field not in raw]
    if missing:
        raise PrunerMissingFieldError(f"Missing fields: {', '.join(missing)}")

    return {field: raw[field] for field in KEPT_FIELDS}
