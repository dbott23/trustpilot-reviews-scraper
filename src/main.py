"""Trustpilot Reviews Scraper — scrapes reviews for one or more companies."""

import asyncio

from apify import Actor

from src.scrapers import trustpilot

CHECKPOINT_KEY = "SCRAPER_CHECKPOINT"


async def main() -> None:
    async with Actor:
        inp = await Actor.get_input() or {}
        Actor.log.info(f"Input: {list(inp.keys())}")

        companies: list[str] = inp.get("companies") or []
        max_per_company: int = int(inp.get("maxReviews") or 50)
        sort_by: str = inp.get("sortBy") or "recent"
        min_rating: int | None = inp.get("minRating")
        api_key: str | None = inp.get("trustpilotApiKey") or None

        if not companies:
            await Actor.fail(status_message="Input must include at least one company name.")
            return

        proxy_config = None
        proxy_url = None
        try:
            proxy_config = await Actor.create_proxy_configuration(groups=["RESIDENTIAL"])
            proxy_url = await proxy_config.new_url() if proxy_config else None
            Actor.log.info("Using RESIDENTIAL proxy")
        except Exception as exc:
            Actor.log.warning(f"Proxy setup failed ({exc}) — running without proxy")

        checkpoint = await Actor.get_value(CHECKPOINT_KEY) or {}
        done: set[str] = set(checkpoint.get("done") or [])
        total_pushed: int = checkpoint.get("total_pushed") or 0

        for company in companies:
            if company in done:
                Actor.log.info(f"Skipping {company} (already done)")
                continue

            Actor.log.info(f"Scraping Trustpilot for: {company}")
            try:
                records = await trustpilot.scrape(
                    company=company,
                    max_reviews=max_per_company,
                    sort_by=sort_by,
                    min_rating=min_rating,
                    proxy_url=proxy_url,
                    api_key=api_key,
                    get_proxy_url=proxy_config.new_url if proxy_config else None,
                )
            except Exception as exc:
                Actor.log.warning(f"Error scraping {company}: {exc}")
                records = []

            if records:
                await Actor.push_data(records)
                total_pushed += len(records)

            done.add(company)
            await Actor.set_value(CHECKPOINT_KEY, {"done": list(done), "total_pushed": total_pushed})
            Actor.log.info(f"  → {len(records)} reviews for {company} (total: {total_pushed})")

        Actor.log.info(f"Done. Total reviews pushed: {total_pushed}")


if __name__ == "__main__":
    asyncio.run(main())
