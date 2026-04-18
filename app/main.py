from app.core.scheduler import Scheduler
from app.storage.repository import SubscriptionRepository
import threading
from app.core.config import Settings
from app.data.github_client import GitHubClient
from app.core.command_handler import CommandHandler
import shlex


def run_scheduler_thread(scheduler):
    scheduler.start()


def main():
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
            except SystemExit as e:
                print("Invalid command. Type 'help' to see the list of available commands.")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
