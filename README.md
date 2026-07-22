# Trustpilot Reviews Scraper

Export Trustpilot reviews for any company to JSON or CSV — no API key required. Enter one or more company names and get ratings, review text, reviewer names, dates, and verified badges in a clean structured dataset.

## What it does

- Search Trustpilot by company name — no need to know the URL or slug
- Scrape up to 500 reviews per company per run
- Filter by minimum star rating to focus on positive or negative reviews
- Sort by most recent, helpful, highest, or lowest rated
- Returns structured data ready to export, pipe into a dashboard, or feed into an AI model

## Use cases

- **Reputation monitoring** — track what customers say about your brand on Trustpilot over time
- **Competitor research** — collect competitor reviews to find product gaps and complaints
- **Review sentiment analysis** — feed reviews into NLP models or AI pipelines
- **Client reporting** — build automated reputation dashboards for clients
- **Lead qualification** — identify dissatisfied customers of competitors for outreach
- **Dataset building** — create labeled review datasets for research or fine-tuning

## Input

| Field | Type | Description |
|---|---|---|
| `companies` | string[] | Company names to search on Trustpilot (e.g. `["Shopify", "HubSpot"]`). |
| `maxReviews` | integer | Max reviews per company (default: `50`, max: `500`). |
| `sortBy` | string | `recent` (default), `helpful`, `highest`, `lowest`. |
| `minRating` | integer | Only collect reviews at or above this star rating (1–5). |
| `trustpilotApiKey` | string | Optional. Provide a Trustpilot API key to access additional data. |

At least one company name must be provided.

## Output

Each result is one review:

```json
{
  "company": "Shopify",
  "rating": 5,
  "title": "Best ecommerce platform I've used",
  "body": "We switched from WooCommerce six months ago and haven't looked back. Setup was fast and support is excellent.",
  "reviewer_name": "Marcus T.",
  "date": "2026-06-15",
  "verified": true,
  "review_url": "https://www.trustpilot.com/reviews/abc123"
}
```

**Key fields:**

- `rating` — 1–5 star rating
- `verified` — whether Trustpilot has verified this reviewer purchased or used the product
- `body` — the full review text
- `review_url` — direct link to the review on Trustpilot

## Limits

| Metric | Limit |
|---|---|
| Reviews per company per run | Up to 500 |
| Companies per run | Unlimited |
| Checkpoint/resume | ✅ Supports resume if run is interrupted |

## Pricing

This actor uses **Pay per result** pricing:

- **$1.00 per 1,000 reviews** scraped
- Scraping 100 reviews for 3 companies costs **~$0.30**
- No proxy costs — residential proxies are included

## Example: scrape competitor reviews for sales battlecard

```json
{
  "companies": ["CompetitorA", "CompetitorB"],
  "maxReviews": 200,
  "sortBy": "lowest",
  "minRating": 1
}
```

Filter the output for `rating <= 2`. The most common complaints in `body` become your sales battlecard talking points.

## Scheduling for weekly reputation monitoring

1. Go to **Actors → Schedules → New schedule** in Apify
2. Point it at this actor with your saved input
3. Set `sortBy: "recent"` and `maxReviews: 20–50`
4. Connect the output to Google Sheets or a Slack webhook via Apify integrations

## Frequently asked questions

**Do I need a Trustpilot API key?**
No. The scraper works without one. An optional API key (`trustpilotApiKey`) may unlock additional data fields but is not required.

**How do I find the right company name?**
Use the name as it appears on Trustpilot (e.g. `"Shopify"`, `"monday.com"`). The scraper searches Trustpilot's directory and picks the top match. If the wrong company is returned, try a more specific name or the company's domain (e.g. `"shopify.com"`).

**Can I scrape multiple companies in one run?**
Yes. Add all company names to the `companies` array. Each company is scraped in sequence, and progress is checkpointed so runs can be resumed if interrupted.

**Does this require a proxy?**
Proxies are used internally (residential proxies are included in the price). You don't need to provide your own.

---

## More from dbott23

| Actor | What it does |
|---|---|
| [App Store & Google Play Reviews Scraper](https://apify.com/dbott23/appstore-reviews-scraper) | Export iOS and Android app reviews by keyword or app ID |
| [B2B Reviews Scraper](https://apify.com/dbott23/b2b-reviews-scraper) | Pull reviews from G2, Capterra, and Trustpilot in one run |
| [Bluesky Posts Scraper](https://apify.com/dbott23/bluesky-posts-scraper) | Search and export Bluesky posts by keyword or user profile |
| [AI Brand Visibility Tracker](https://apify.com/dbott23/ai-brand-visibility-tracker) | Track how AI assistants mention your brand vs. competitors |
| [AI Citation Auditor](https://apify.com/dbott23/ai-citation-auditor) | Check if your website is cited by ChatGPT, Perplexity, and Gemini |
