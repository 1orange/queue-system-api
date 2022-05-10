from smart_queue.analysis.configurations.generator import generate_configration

if __name__ == "__main__":
    for index in range(1, 101):
        generate_configration(NAME=f"configuration_{index}", SEED=index)
