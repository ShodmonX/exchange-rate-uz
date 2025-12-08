import asyncio
import signal
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
        CronTrigger(hour=19, minute=10)
    )
    scheduler.start()

    print("Scheduler started. Waiting for jobs...")

    # shutdown uchun event
    stop_event = asyncio.Event()

    # signal handlers
    def shutdown():
        print("Received stop signal. Shutting down gracefully...")
        scheduler.shutdown(wait=False)
        stop_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, shutdown)
    loop.add_signal_handler(signal.SIGINT, shutdown)

    # stop event set bo'lguncha kutish
    await stop_event.wait()
    print("Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
