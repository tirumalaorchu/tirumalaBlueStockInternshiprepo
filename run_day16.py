import argparse
from pathlib import Path

from day16_screeners import PresetScreeners


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the six Day 16 preset screeners")
    parser.add_argument("input", type=Path, help="92-company fundamentals CSV")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/day16_screeners"),
    )
    args = parser.parse_args()

    screeners = PresetScreeners(args.input)
    results = screeners.run_all()

    print(f"Universe size: {screeners.data['company_id'].nunique()} companies")
    for name, result in results.items():
        status = "PASS" if 5 <= len(result) <= 50 else "CHECK"
        print(f"{status}: {name}: {len(result)} companies")

    screeners.save_all(args.output)
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()