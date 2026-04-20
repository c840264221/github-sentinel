from app.interfaces.cli.scheduler import Scheduler
from app.storage.repository import SubscriptionRepository
import threading
from app.core.config import Settings
from app.services.github_client import GitHubClient
from app.interfaces.cli.command_handler import CommandHandler
from app.core.logger import setup_logger, get_logger
import shlex


def run_scheduler_thread(scheduler):
    scheduler.start()


def main():
    setup_logger()
    logger = get_logger(__name__)
    config = Settings()
    github_client = GitHubClient(config.github_token)
    subscription_manager = SubscriptionRepository()
    command_handler = CommandHandler(github_client, subscription_manager)
    scheduler = Scheduler(
        github_client=github_client,
        notifier=None,
        report_generator=None,
        subscription_manager=None,
        interval=config.update_interval
    )
    print("🚀 GitHub Sentinel (Interactive Mode)")
    scheduler_thread = threading.Thread(target=run_scheduler_thread, args=(scheduler,))
    scheduler_thread.daemon = True
    scheduler_thread.start()

    parser = command_handler.parser
    command_handler.print_help()

    while True:
        try:
            user_input = input("GitHub Sentinel> ")
            if user_input in ['exit', 'quit']:
                break
            try:

                args = parser.parse_args(shlex.split(user_input))

                if args.command is None:
                    continue
                args.func(args)
            except ValueError:
                continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            logger.exception("Unexpected error")


if __name__ == "__main__":
    main()
