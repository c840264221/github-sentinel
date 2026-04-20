import functools
from datetime import datetime
from app.core.logger import get_logger
from app.core.constants import SKIP


logger = get_logger(__name__)

def verify_md_exist(repo_repository):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            repo = kwargs.get("repo") or args[1]
            since = kwargs.get("since")
            if not since:
                return func(*args, **kwargs)

            if isinstance(since, datetime):
                since = since.date()

            repo_data = repo_repository.get_one(repo)
            if len(repo_data) == 0:
                return func(*args, **kwargs)

            start_time = repo_data.get('start_time', 'None')
            end_time = repo_data.get('end_time', 'None')

            today = datetime.now().date().isoformat()

            if start_time == since.isoformat() and end_time == today:
                # print('The data is already fetched!')
                logger.info(f"⏭ Skip {repo}, already fetched today")
                return SKIP

            return func(*args, **kwargs)
        return wrapper
    return decorator


def add_fetch_time(repo_repository):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # ❗ 如果被跳过，不更新
            if result is None:
                return None

            repo = kwargs.get("repo") or args[1]
            since = kwargs.get("since")

            if isinstance(since, datetime):
                since = since.date()

            all_data = repo_repository.get_all()

            for repo_data in all_data:
                if repo_data.get('repo_name') == repo:
                    repo_data['start_time'] = since.isoformat()
                    repo_data['end_time'] = datetime.now().date().isoformat()
            repo_repository.save(all_data)
            return result
        return wrapper
    return decorator

