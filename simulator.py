import argparse
import concurrent.futures
import logging
import logging.config
import os
import shutil
import statistics
from collections import defaultdict

import numba as nb
import pandas as pd

from smart_queue import config
from smart_queue.analysis import CONDITION_TABLE, CONFIGURATION_PATH
from smart_queue.analysis.classes.Patient import Patient
from smart_queue.analysis.classes.Queue import Queue
from smart_queue.analysis.configurations.generator import (
    generate_configuration
)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Get priority of conditions with given time"
)

parser.add_argument(
    "-i",
    "--iterations",
    dest="iterations",
    required=False,
    help="Number of iterations",
)

args = parser.parse_args()

def dump_to_file(configurations):
    logger.info("Dumping file")
    with open(
        file=f"{CONFIGURATION_PATH}/data", mode="a", encoding="utf-8"
    ) as configuration_file:
        for iter in configurations:
            for patient in configurations[iter]:    
                print(
                    f"{iter},{patient[0]},{patient[1]}",
                    file=configuration_file,
                )

def create_data(number_of_iterations):
    logger.info("Creating iterations data")

    shutil.rmtree(CONFIGURATION_PATH)
    os.makedirs(CONFIGURATION_PATH)

    configurations = dict()

    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        for index in range(1, number_of_iterations + 1):
            executor.submit(generate_configuration, SEED=index, conf_obj=configurations)

    # Dump configurations
    dump_to_file(configurations)
   
    logger.info("Done! Data created")


def load_data_from_csv(df, iter_num):
    patients = []

    filtered_df = df.loc[df["iter"] == iter_num].sort_values(by=["timestamp"])

    for index, row in filtered_df.iterrows():
        patients.append(
            Patient(index, CONDITION_TABLE[row["condition"]], row["timestamp"])
        )

    # return sorted(patients, key=lambda x: x.time_arrived)
    return patients


def simulation_process(queue):
    res_dict = {}

    for condition, wait_values in queue.simulate().items():
        if condition in res_dict:
            res_dict[condition] += wait_values
        else:
            res_dict[condition] = wait_values

    return res_dict

def simulate_process_wrapper(df, iter, res_naive, res_smart):
    iter_data = load_data_from_csv(df, iter)

    logger.debug(f"Simulation {iter} starting")

    naive = Queue(
        open_time="08:00:00",
        close_time="16:00:00",
        iter_data=iter_data[:],
        naive=True,
    )

    smart = Queue(
        open_time="08:00:00",
        close_time="16:00:00",
        iter_data=iter_data[:],
        naive=False,
    )

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        naive_result = executor.submit(simulation_process, queue=naive).result()
        smart_result = executor.submit(simulation_process, queue=smart).result()
        
        for key in naive_result:
            if key in res_naive:
                res_naive[key] += naive_result[key]
            else:
                res_naive[key] = naive_result[key]
            
            if key in res_smart:
                res_smart[key] += smart_result[key]
            else:
                res_smart[key] = smart_result[key]    

        logger.debug(f"Simulation {iter} Done")


def simulate(number_of_iterations):
    logger.info("Starting simulation")
    df = pd.read_csv(
        f"{CONFIGURATION_PATH}/data",
        sep=",",
        names=["iter", "condition", "timestamp"],
        header=None,
        encoding='utf8'
    )

    iter_results_naive = dict()
    iter_results_smart = dict()

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for iter in range(1, number_of_iterations + 1):

            sim = executor.submit(
                simulate_process_wrapper,
                df=df,
                iter=iter,
                res_naive=iter_results_naive,
                res_smart=iter_results_smart,
            )

    logger.info("Gathering data")
    # Create medians
    for con in iter_results_naive:

        iter_results_naive[con] = (
            statistics.median(iter_results_naive[con]),
            len(iter_results_naive[con]),
        )
        iter_results_smart[con] = (
            statistics.median(iter_results_smart[con]),
            len(iter_results_smart[con]),
        )

    logger.info("Simulation done. Results:\r\n")

    print(f"# NAIVE Q WAITING_TIME_MEDIAN [{number_of_iterations} iters]:")
    for condition, stats in iter_results_naive.items():
        print(f"{condition} [{stats[1]}] - {stats[0]} min")

    print()

    print(f"# SMART Q WAITING_TIME_MEDIAN [{number_of_iterations} iters]:")
    for condition, stats in iter_results_smart.items():
        print(f"{condition} [{stats[1]}] - {stats[0]} min")
    print()


if __name__ == "__main__":
    logging.config.dictConfig(config.logging)

    create_data(int(args.iterations))
    # simulate(100)
