import time
from app.interfaces.cli.run import run
from app.core.logger import get_logger


logger = get_logger(__name__)

class Scheduler:
    def __init__(self,github_client, notifier, report_generator, subscription_manager, interval=86400):
        self.github_client = github_client
        self.notifier = notifier
        self.report_generator = report_generator
        self.subscription_manager = subscription_manager
        self.interval = interval
    def start(self):
        self.run()

    def run(self):
        print("⏰ Scheduler started...")
        logger.info("Scheduler started")
        while True:
            print("🔄 Running scheduled job...")
            logger.info(f"Running scheduled job...")
            try:
                run()
            except Exception as e:
                logger.exception(e)
                print(f"❌ Error: {e}")
            print(f"😴 Sleeping for {self.interval} seconds...\n")
            logger.info(f"Sleeping for {self.interval} seconds")
            time.sleep(self.interval)