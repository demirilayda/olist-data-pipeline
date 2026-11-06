# LLM Labeling Prompt

The exact instructions given to the LLM that labeled the 1,000-review sample.

**Setup:** Claude Opus 5.5, run through Claude Code as fresh sub-sessions (one per batch of 250 reviews). Each sub-session received only this prompt, the taxonomy (`02_complaint_taxonomy.md`) and its batch of reviews. It had **no access to the hand labels** in `data/labels/manual_100.csv`, so the validation in notebook 05 is a fair test.

The batch files are built and merged by `src/llm_labeling.py`.

---

## Prompt

You are labeling customer reviews from Olist, a Brazilian e-commerce marketplace. Every review in your batch got 1 or 2 stars. The reviews are in Portuguese.

**Your task:** for each review, decide the main reason the customer is unhappy, using the complaint taxonomy below.

Rules:
1. Read the taxonomy carefully. Use its definitions and apply its ordered tie-break rules: the first rule that matches wins.
2. Give each review **exactly one** `primary_label` from this list:
   `not_received`, `late_delivery`, `incomplete_order`, `wrong_product`, `damaged_or_defective`, `poor_quality_or_not_as_described`, `cancellation_or_refund`, `delivery_service`, `customer_service`, `other_or_unclear`
3. Set `seller_unresponsive` to `true` only if the customer says they contacted the seller or store and got no answer or help. Otherwise `false`.
4. Set `confidence` to `high` when the text clearly fits one label, `low` when it is borderline between two labels.
5. Label from the **text only**. Do not guess a reason the text does not state. If no reason is given, use `other_or_unclear`.
6. Add a short English `reason` (max 15 words) explaining the choice.

Output one JSON object per line (JSONL), one line per review, in the same order as the input, with exactly these keys:

```json
{"id": "r0001", "primary_label": "not_received", "seller_unresponsive": false, "confidence": "high", "reason": "Customer says the product never arrived."}
```

Label every review in the batch. Do not skip any, and do not add any other text to the output file.
