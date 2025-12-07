from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .reference import refresh_reference_cache

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(
        refresh_reference_cache,
        "cron",
        hour=7,
        minute=0,
        id="refresh_reference_cache",
        replace_existing=True,
    )

    scheduler.start()