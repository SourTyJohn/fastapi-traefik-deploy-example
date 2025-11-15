import subprocess
import argparse


parser = argparse.ArgumentParser(
    prog="migrate",
    description="Script for apply alembic migrations",
)


def main():
    command = [
        "alembic",
        "-c",
        "task_manager/adapters/alembic/alembic.ini",
        "upgrade",
        "head",
    ]

    print(f"EXECUTING: {' '.join(command)}")
    exit(subprocess.call(command))


if __name__ == "__main__":
    main()
