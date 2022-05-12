import os

from smart_queue.analysis.classes.Condition import Condition
from smart_queue.db.database import get_all_conditions

CONFIGURATION_PATH = os.path.abspath(
    os.path.join("smart_queue", "analysis", "configurations", "generated")
)
RESULT_PATH = os.path.abspath(
    os.path.join("smart_queue", "analysis", "results")
)

CONDITION_TABLE = {
    condition.name: Condition(
        condition.name, condition.burst_time, condition.urgency
    )
    for condition in get_all_conditions()
}
