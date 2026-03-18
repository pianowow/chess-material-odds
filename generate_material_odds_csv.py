#!/usr/bin/env python3
import argparse
import csv
from fractions import Fraction
from pathlib import Path


PIECE_VALUES = {
    "pawns": Fraction(1, 1),
    "knights": Fraction(3, 1),
    "bishops": Fraction(7, 2),  # 3.5
    "rooks": Fraction(11, 2),  # 5.5
    "queens": Fraction(19, 2),  # 9.5
}


def format_one_decimal(value: Fraction) -> str:
    scaled = value * 10
    if scaled.denominator != 1:
        raise ValueError(f"Expected 0.1 increments, got {value!r}")
    n = scaled.numerator
    sign = "-" if n < 0 else ""
    n = abs(n)
    return f"{sign}{n // 10}.{n % 10}"


def generate_rows():
    for pawns in range(0, 9):
        for knights in range(0, 3):
            for bishops in range(0, 3):
                for rooks in range(0, 3):
                    for queens in range(0, 2):
                        total_pieces = pawns + knights + bishops + rooks + queens
                        total_value = (
                            PIECE_VALUES["pawns"] * pawns
                            + PIECE_VALUES["knights"] * knights
                            + PIECE_VALUES["bishops"] * bishops
                            + PIECE_VALUES["rooks"] * rooks
                            + PIECE_VALUES["queens"] * queens
                        )
                        yield {
                            "handicapped_pawns": pawns,
                            "handicapped_knights": knights,
                            "handicapped_bishops": bishops,
                            "handicapped_rooks": rooks,
                            "handicapped_queens": queens,
                            "handicapped_total_value": total_value,
                            "handicapped_total_pieces": total_pieces,
                        }


def sort_key(row):
    return (
        row["handicapped_total_value"],
        row["handicapped_total_pieces"],
        row["handicapped_queens"],
        row["handicapped_rooks"],
        row["handicapped_bishops"],
        row["handicapped_knights"],
        row["handicapped_pawns"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a CSV ladder of handicapped (stronger) side material-odds configurations."
    )
    parser.add_argument(
        "--out",
        default="material_odds.csv",
        help="Output CSV path (default: material_odds.csv)",
    )
    args = parser.parse_args()

    out_path = Path(args.out)
    rows = sorted(generate_rows(), key=sort_key)

    fieldnames = [
        "row_id",
        "handicapped_pawns",
        "handicapped_knights",
        "handicapped_bishops",
        "handicapped_rooks",
        "handicapped_queens",
        "handicapped_total_pieces",
        "handicapped_total_value",
    ]

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for idx, row in enumerate(rows, start=1):
                writer.writerow(
                    {
                        "row_id": idx,
                        "handicapped_pawns": row["handicapped_pawns"],
                        "handicapped_knights": row["handicapped_knights"],
                        "handicapped_bishops": row["handicapped_bishops"],
                        "handicapped_rooks": row["handicapped_rooks"],
                        "handicapped_queens": row["handicapped_queens"],
                        "handicapped_total_pieces": row["handicapped_total_pieces"],
                        "handicapped_total_value": format_one_decimal(
                            row["handicapped_total_value"]
                        ),
                    }
                )
    except OSError as e:
        parser.error(f"Failed to write {out_path}: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
