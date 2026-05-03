from src.pipelines.collect_daily_rss import main as collect_daily_rss
from src.pipelines.build_recent_datasets import main as build_recent_datasets
from src.pipelines.run_recent_experiments import main as run_recent_experiments
from src.analysis.cross_section_summary import main as run_cross_section_summary


def main() -> None:
    collect_daily_rss()
    build_recent_datasets()
    run_recent_experiments()
    run_cross_section_summary()

    print("\nPipeline finished.")


if __name__ == "__main__":
    main()