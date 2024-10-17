import coloredlogs

from uss.behave import count_scenarios_by_status, find_scenarios, parse_behave_report

coloredlogs.install(level="DEBUG")
import argparse
from os import listdir
from os.path import isfile, join

MAX_RUNS = 500


def summarize(reports_dir):
    files = [f for f in listdir(reports_dir) if isfile(join(reports_dir, f))]
    final_count = {
        "passed": 0,
        "skipped": 0,
        "failed": 0,
    }

    total_scenarios = 0
    total_runs = 0

    for file in files:
        report = parse_behave_report(join(reports_dir, file))

        scenarios = find_scenarios(report)
        count = count_scenarios_by_status(scenarios)

        for s in final_count:
            final_count[s] = final_count[s] + count[s]
            total_scenarios += count[s]
        total_runs += 1

        if total_runs == MAX_RUNS:
            break

    print(f"{total_scenarios=}")
    print(f"{final_count=}")
    print(f"{total_runs=}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Summarize Reports ",
        description="Summarizes the behave reports into a table",
    )
    parser.add_argument("reports_dir")
    args = parser.parse_args()
    reports_dir = args.reports_dir
    summarize(reports_dir)
