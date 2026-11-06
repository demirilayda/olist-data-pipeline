# Complaint Taxonomy

The list of complaint reasons used to label 1–2 star reviews. The same rules are used by **both** the human labeler (`data/labels/manual_100.csv`) and the LLM classifier, so their labels can be compared directly.

## How it was built
- Read **300 written 1–2 star reviews**, drawn at random (seed 7) from `outputs/negative_reviews.csv`.
- The 1,000-review classification sample was **excluded** from this draw, so the rules were not written while looking at the reviews they will be tested on.
- Grouped the complaints by *what went wrong for the customer*, then wrote a definition, real examples and boundary rules for each group.

## Labels

Each review gets **exactly one primary label**: the problem the customer is mainly unhappy about.

| Label | What went wrong | Example (translated) |
|---|---|---|
| `not_received` | Nothing has arrived (yet): lost, stuck in transit, still waiting, or "delivered" in tracking but not received | *"Até o momento não recebi nenhum produto."* "So far I haven't received any product." |
| `late_delivery` | The order arrived, but late or much slower than expected | *"O produto foi entregue com atraso."* "The product was delivered late." |
| `incomplete_order` | Part of the order is missing: fewer units, one of several items, or missing parts/accessories | *"Comprei 2 cortinas e só veio 1."* "I bought 2 curtains and only 1 came." |
| `wrong_product` | A different item was sent: other model, color, size, brand, or a counterfeit | *"Comprei um cavalinho e mandaram um urso."* "I bought a little horse and they sent a bear." |
| `damaged_or_defective` | The right item arrived broken, damaged, used, or does not work | *"Os copos chegaram todos quebrados."* "The glasses all arrived broken." |
| `poor_quality_or_not_as_described` | The item works and is the one listed, but the quality is low or it does not match the photo/description | *"O material é de péssima qualidade, veio com fiapos."* "Very poor material, came with loose threads." |
| `cancellation_or_refund` | The order was cancelled (often out of stock), a cancellation was ignored, or a refund is not being paid | *"O fornecedor informou que não há estoque. Gostaria do reembolso."* "The supplier said there's no stock. I want a refund." |
| `delivery_service` | It arrived, but the delivery itself was the problem: had to pick it up at the post office, carrier did not try to deliver | *"Tive que ir buscar em um correio super longe."* "I had to pick it up at a post office far away." |
| `customer_service` | The only complaint is that the seller or store does not answer or help | *"Não consegue falar com o vendedor quando tem problemas."* "You can't reach the seller when there's a problem." |
| `other_or_unclear` | No reason given, positive text with a low score, a question, or not about the order | *"Super recomendo, veio antes do prazo."* "Highly recommend, came early." (1 star) |

### Secondary flag
`seller_unresponsive` (true/false): the customer says they contacted the seller/store and got no answer. Many reviews add this to another problem ("came broken **and nobody answers**"), so it is recorded separately instead of competing with the primary label.

## Rules for hard cases

Apply these in order. The first rule that matches wins.

1. **Nothing received → `not_received`**, even if the customer also says it is late. Exception: if the text says the seller cancelled it or it is out of stock, use `cancellation_or_refund`.
2. **Some items received, some missing → `incomplete_order`**, even if the order system says "delivered".
3. **Received the wrong item → `wrong_product`.** If they also complain about its quality, the wrong item is still the main problem.
4. **Received the right item, but broken or not working → `damaged_or_defective`.**
5. **Right item, works, but disappointing → `poor_quality_or_not_as_described`.** Includes "smaller than in the photo", "thin material", "not the color shown in the ad" (when the product is the one listed, not a swap).
6. **Received complete and intact, only late → `late_delivery`.**
7. **Only the delivery method was the problem → `delivery_service`.**
8. **Only the lack of response → `customer_service`.**
9. Anything else → `other_or_unclear`. Do not guess a reason the text does not state.

Wrong item vs not as described: if the customer says *"they sent something else"*, it is `wrong_product`. If they say *"it is not like the photo"*, it is `poor_quality_or_not_as_described`.

## What reading 300 reviews already showed
These are first impressions to check with the labeled data, not results:

- **"Delivered" in the data does not always mean the customer got everything.** Many orders marked as delivered on time have reviews saying *"I only received 1 of 2"* or *"tracking says delivered but nothing arrived"*. Incomplete orders look like a large, hidden group.
- **Wrong products are common.** Different color, size or model, sometimes cheaper than what was paid for.
- **Stock-outs reach the customer late.** Several customers learned on or after the promised date that the item was out of stock, which turns a stock problem into a delivery and refund problem.
- **Low scores with positive text exist** (e.g. "Highly recommend, came early" with 1 star). The customer probably picked the wrong score; these go to `other_or_unclear`.
- 27% of 1–2 star reviews on delivered orders were written **before** the order arrived, almost all of them on late orders. The review captures the waiting, not the product.
