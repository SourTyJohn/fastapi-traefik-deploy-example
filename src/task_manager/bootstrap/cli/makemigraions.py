import subprocess
import argparse


parser = argparse.ArgumentParser(
    prog="makemigrations",
    description="Script for creating alembic migrations for sqlalchemy",
)
parser.add_argument(
    "message",
    help="Migration Message",
)
parser.add_argument(
    "--empty",
    help="If provided, generates empty migration ",
    action="store_true",
    default=False,
)


def main():
    args = parser.parse_args()

    command = [
        "alembic",
        "-c",
        "task_manager/adapters/alembic/alembic.ini",
        "revision",
        "-m",
        args.message,
    ]
    if not args.empty:
        command.insert(-2, "--autogenerate")

    print(f"EXECUTING: {' '.join(command)}")
    exit(subprocess.call(command))


if __name__ == "__main__":
    main()
