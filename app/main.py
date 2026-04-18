from app.interfaces.cli.run import run
from app.core.scheduler import start_scheduler
import argparse
from app.storage.repository import SubscriptionRepository
import threading


def scheduler_thread():
    start_scheduler(job_func=run, interval_seconds=60)


def cli_loop():
    repo = SubscriptionRepository()

    while True:
        cmd = input("👉 Enter command (add/remove/list/exit): ").strip()

        if cmd.startswith("add "):
            repo_name = cmd.split(" ", 1)[1]
            repo.add(repo_name)

        elif cmd.startswith("remove "):
            repo_name = cmd.split(" ", 1)[1]
            repo.remove(repo_name)

        elif cmd == "list":
            subs = repo.get_all()
            if not subs:
                print("📭 No subscriptions")
            else:
                print("📦 Subscriptions:")
                for sub in subs:
                    print(f"- {sub['repo_name']}")

        elif cmd == "exit":
            print("👋 Exiting...")
            break

        else:
            print("❓ Unknown command")


def main():
    # parser = argparse.ArgumentParser(description="GitHub Sentinel CLI")
    #
    # subparsers = parser.add_subparsers(dest="command")
    #
    # # add 命令
    # add_parser = subparsers.add_parser("add")
    # add_parser.add_argument("repo", help="Repository name (e.g. owner/repo)")
    #
    # # remove 命令
    # remove_parser = subparsers.add_parser("remove")
    # remove_parser.add_argument("repo", help="Repository name")
    #
    # # list 命令
    # subparsers.add_parser("list")
    #
    # # run 命令  启动程序
    # subparsers.add_parser("run")
    #
    # args = parser.parse_args()
    #
    # repo = SubscriptionRepository()
    #
    # if args.command == "add":
    #     repo.add(args.repo)
    #
    # elif args.command == "remove":
    #     repo.remove(args.repo)
    #
    # elif args.command == "list":
    #     subs = repo.get_all()
    #     if not subs:
    #         print("📭 No subscriptions")
    #     else:
    #         print("📦 Subscriptions:")
    #         for sub in subs:
    #             print(f"- {sub['repo_name']}")
    #
    # elif args.command == "run":
    #     print("🚀 Starting scheduler...")
    #     start_scheduler(job_func=run, interval_seconds=60)
    #
    # else:
    #     parser.print_help()

    # run()
    print("🚀 GitHub Sentinel (Interactive Mode)")

    # 启动后台线程
    t = threading.Thread(target=scheduler_thread, daemon=True)
    t.start()

    # 主线程处理输入
    cli_loop()


if __name__ == "__main__":
    main()
    # run()
