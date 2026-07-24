import argparse
from pathlib import Path

from day17_composite import CompositeScoreExporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Day 17 composite screener results")
    parser.add_argument("input", type=Path, help="Company fundamentals CSV")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/screener_output.xlsx"),
    )
    args = parser.parse_args()

    exporter = CompositeScoreExporter(args.input)
    output = exporter.export(args.output)
    for name, result in exporter.results().items():
        print(f"{name}: {len(result)} companies")
    print(f"Saved workbook: {output}")


if __name__ == "__main__":
    main()
