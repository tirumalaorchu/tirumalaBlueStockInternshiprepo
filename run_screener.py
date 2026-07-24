import argparse
from pathlib import Path

from engine import ScreenerEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the financial company screener")
    parser.add_argument("input", type=Path, help="CSV or Excel-compatible input file")
    parser.add_argument("--output", type=Path, default=Path("results/screened_companies.csv"))
    parser.add_argument("--min-roe", type=float, default=15)
    parser.add_argument("--max-de", type=float, default=1)
    parser.add_argument("--min-roce", type=float)
    args = parser.parse_args()

    engine = ScreenerEngine(args.input)
    result = engine.screen(args.min_roe, args.max_de, args.min_roce)
    output = engine.save(result, args.output)
    print(f"Companies found: {len(result)}")
    print(f"Saved result: {output}")


if __name__ == "__main__":
    main()