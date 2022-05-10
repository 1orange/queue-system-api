import argparse

from smart_queue.db.database import get_all_conditions

parser = argparse.ArgumentParser(
    description="Get priority of conditions with given time"
)

parser.add_argument(
    "-t",
    "--time",
    dest="wait_time",
    required=True,
    help="Wait time in minutes",
)

args = parser.parse_args()


def eval_priority_by_wait_time(elapsed_minutes):
    """
    Eval algo: (duration.seconds * urgency) / burst_time
    """
    eval_result = dict()

    for condition in get_all_conditions():
        eval_result[condition.name] = (
            int(elapsed_minutes) * 60 * condition.urgency
        ) / condition.burst_time

    return eval_result


if __name__ == "__main__":
    result = eval_priority_by_wait_time(args.wait_time)

    print(f"Result for {int(args.wait_time)} minutes:")

    for condition in sorted(
        result.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"{condition[0]} - {condition[1]}")
