import argparse

from smart_queue.analysis.configurations.generator import (
    generate_configuration,
)

parser = argparse.ArgumentParser(
    description="Get priority of conditions with given time"
)

parser.add_argument(
    "-i",
    "--iterations",
    dest="iterations",
    required=True,
    help="Number of iterations",
)

args = parser.parse_args()

if __name__ == "__main__":
    for index in range(1, int(args.iterations) + 1):
        generate_configuration(NAME=f"configuration_{index}", SEED=index)
