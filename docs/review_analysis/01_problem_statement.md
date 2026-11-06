# Problem Statement: Why Do Customers Give 1 Star?

## Business question
**What are the main reasons behind 1–2 star reviews, and which one should we fix first to protect the most revenue?**

## Who this is for
The **operations manager** at Olist, the person responsible for delivery, carriers and seller processes.
They need a short, ranked answer to "what do we fix first?", backed by numbers they can defend.

## Why it matters
- Earlier analysis in this repo showed that 1-star orders took **21.3 days** to arrive on average, compared with **10.7 days** for 5-star orders.
- Only **3.1%** of customers ever order again. Every unhappy first order is likely a lost customer.
- Star ratings tell us *that* customers are unhappy, not *why*. The reasons are hidden in **10,867 written 1–2 star reviews** (one per order) (in Portuguese), which nobody can read one by one.

## Hypotheses
| # | Hypothesis | How we test it |
|---|---|---|
| H1 | Most complaints are about **delivery** (late or missing orders), not the product. | Share of each complaint reason in the classified sample. |
| H2 | **Product quality** problems are concentrated in a few categories. | Complaint reasons broken down by product category. |
| H3 | Missing the **promised delivery date** lowers the rating sharply, regardless of total delivery time. | Ratings of orders delivered before vs after the estimated date, using structured data only (no AI). |

My expectation before looking at the data: late delivery is the main driver (H1).
The point of the analysis is to check that expectation, not to confirm it.

## Approach
1. Build a dataset of written 1–2 star reviews joined with order, delivery, product, seller and revenue data.
2. Test H3 with structured data only, before using any AI.
3. Define a complaint taxonomy (6–9 reasons) by reading a sample of reviews.
4. Label 100 reviews by hand as a validation set.
5. Classify a random sample of 1,000 reviews with an LLM (Claude Haiku 5.5) and measure its agreement with the hand labels.
6. Estimate the revenue affected by each complaint reason.

## Definition of success
- A **ranked list of the top 3 problems** to fix, each with:
  - how often it occurs,
  - the revenue of the orders it affects,
  - where it concentrates (category, state or seller).
- LLM labels agree with the hand-labeled set on **at least 85%** of reviews. If not, the taxonomy or the prompt is fixed and re-measured before results are used.
- A Power BI page that the operations manager can read without help.

## Out of scope
- Classifying all 40,977 written reviews. A 1,000-review random sample is enough to estimate shares within about ±3 percentage points.
- Reviews with 3–5 stars.
- Predicting future ratings or building a real-time system.
- Translating reviews for publication. Translations are only used to help with hand labeling.
