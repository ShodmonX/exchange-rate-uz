import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from services.cbu import cbu_main

async def scheduled_job():
    print("Running async scraper job...")
    await cbu_main()
    print("Scraper job finished.")

async def main():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        scheduled_job,
        CronTrigger(hour=8, minute=0)
    )

    scheduler.start()
    print("Scheduler started. Waiting for jobs...")

    # ASYNC scheduler doimiy ishlashi uchun event loopni bloklamaslik lozim
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
