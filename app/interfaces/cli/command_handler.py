import argparse


class MYCommandHandler(argparse.ArgumentParser):
    def error(self, message):
        print(f"\n❌ {message}\n")
        self.print_help()
        raise ValueError(message)


class CommandHandler:

    def __init__(self, github_client, subscription_manager):
        super(CommandHandler, self).__init__()
        self.github_client = github_client
        self.subscription_manager = subscription_manager
        # self.report_generator = report_generator
        self.parser = self.create_parser()

    def create_parser(self):
        parser = MYCommandHandler(
            description='GitHub Sentinel Command Line Interface',
            formatter_class=argparse.RawTextHelpFormatter
        )
        subparsers = parser.add_subparsers(title='Commands', dest='command', parser_class=MYCommandHandler)

        parser_add = subparsers.add_parser('add', help='Add a subscription')
        parser_add.add_argument('repo', type=str, help='The repository to subscribe to (e.g., owner/repo)')
        parser_add.set_defaults(func=self.add_subscription)

        parser_remove = subparsers.add_parser('remove', help='Remove a subscription')
        parser_remove.add_argument('repo', type=str, help='The repository to unsubscribe from (e.g., owner/repo)')
        parser_remove.set_defaults(func=self.remove_subscription)

        parser_list = subparsers.add_parser('list', help='List all subscriptions')
        parser_list.set_defaults(func=self.list_subscriptions)

        parser_help = subparsers.add_parser('help', help='Show help message')
        parser_help.set_defaults(func=self.print_help)

        return parser

    def add_subscription(self, args):
        self.subscription_manager.add(args.repo)
        print(f"Added subscription for repository: {args.repo}")

    def remove_subscription(self, args):
        self.subscription_manager.remove(args.repo)
        print(f"Removed subscription for repository: {args.repo}")

    def list_subscriptions(self, args):
        subscriptions = self.subscription_manager.get_all()
        print("Current subscriptions:")
        for sub in subscriptions:
            print(f"  - {sub}")

    def print_help(self, args=None):
        self.parser.print_help()