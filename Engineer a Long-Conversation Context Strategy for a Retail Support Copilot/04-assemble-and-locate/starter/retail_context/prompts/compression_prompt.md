You are tasked with creating a structured summary of a resolved customer support segment. Follow the exact output format below:

**Output Format (3-part structure - Outcome, Facts, Resolution):**
1. **Outcome** (Opening): ONE sentence (past-tense) stating what issue was resolved.
2. **Facts** (Key Facts): 3–6 bullet points with only decision-relevant facts:
   - Order/subscription identifiers (e.g., ORD-77310)
   - Amounts (e.g., $22.14 — byte-exact)
   - Status tokens as they appear in the transcript (e.g., processed, in_progress, AVS_MISMATCH)
   - Dates and deadlines if relevant
3. **Resolution**: ONE sentence (past-tense) naming the terminal state of the issue.

**Rules:**
- **Total output ≤ 500 tokens.** Be concise.
- **Preserve all identifiers and amounts byte-exact.** No rounding, no approximations (e.g., "exactly $22.14", not "around $20").
- **Preserve status tokens verbatim** in snake_case as they appear in the transcript (e.g., cancelled_with_prorated_refund, AVS_MISMATCH).
- **No prose preambles, no closing remarks, no code fences.** Output only the structure above.

**Example:**
> The customer's refund request was processed and the payment method was updated to resolve the failed charge.
> - Order ORD-77310: $22.14 refund status processed
> - Refund eligible until 2026-05-12 (within 30-day window)
> - Subscription SUB-22119 (Pantry Plus Monthly) cancelled due to duplicate_charge
> - New payment method 7782 registered; previous method 4242 retired
> The refund was successfully applied and the subscription cancellation with prorated refund is complete.

Do not include backticks, markdown, or any formatting outside the structure above.
