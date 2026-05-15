import argparse
import csv
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "recipes.csv"
)


def scale_recipe(recipe_name: str, target_portions: float):
    with DATA_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        rows = [
            row for row in reader
            if row["recipe"] == recipe_name
        ]

    if not rows:
        print(f"Recipe not found: {recipe_name}")
        return

    base_portions = float(rows[0]["base_portions"])

    scale_factor = target_portions / base_portions

    print("\n===================================")
    print(" TenzoToolkit Prep Calculator")
    print("===================================\n")

    print(f"Recipe: {recipe_name}")
    print(f"Base Portions: {base_portions:g}")
    print(f"Target Portions: {target_portions:g}")
    print(f"Scale Factor: {scale_factor:.2f}\n")

    print("Scaled Ingredients")
    print("-----------------------------------")

    for row in rows:
        quantity = float(row["quantity"])

        scaled_quantity = quantity * scale_factor

        print(
            f"{row['ingredient']:<20}"
            f"{scaled_quantity:>8.2f} "
            f"{row['unit']}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="TenzoToolkit Kitchen Prep Calculator"
    )

    subparsers = parser.add_subparsers(dest="command")

    scale_parser = subparsers.add_parser(
        "scale",
        help="Scale a recipe"
    )

    scale_parser.add_argument(
        "recipe",
        help="Recipe name"
    )

    scale_parser.add_argument(
        "portions",
        type=float,
        help="Target portions"
    )

    args = parser.parse_args()

    if args.command == "scale":
        scale_recipe(
            args.recipe,
            args.portions
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
