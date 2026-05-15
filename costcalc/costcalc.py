import argparse
import csv
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]

RECIPES_PATH = ROOT_PATH / "data" / "recipes.csv"
PRICES_PATH = ROOT_PATH / "data" / "vendor_prices.csv"


def load_vendor_prices():
    prices = {}

    with PRICES_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            prices[row["ingredient"]] = {
                "purchase_unit": row["purchase_unit"],
                "cost": float(row["cost"]),
            }

    return prices


def cost_recipe(recipe_name: str):
    prices = load_vendor_prices()

    with RECIPES_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        recipe_rows = [
            row for row in reader
            if row["recipe"] == recipe_name
        ]

    if not recipe_rows:
        print(f"Recipe not found: {recipe_name}")
        return

    base_portions = float(recipe_rows[0]["base_portions"])
    total_cost = 0

    print("\n===================================")
    print(" TenzoToolkit Recipe Cost Calculator")
    print("===================================\n")

    print(f"Recipe: {recipe_name}")
    print(f"Base Portions: {base_portions:g}\n")

    print("Ingredient Costs")
    print("-----------------------------------")

    for row in recipe_rows:
        ingredient = row["ingredient"]
        quantity = float(row["quantity"])
        unit = row["unit"]

        if ingredient not in prices:
            print(f"{ingredient:<20} price missing")
            continue

        ingredient_cost = prices[ingredient]["cost"] * quantity
        total_cost += ingredient_cost

        print(
            f"{ingredient:<20}"
            f"{quantity:>8.2f} {unit:<8}"
            f"${ingredient_cost:>8.2f}"
        )

    cost_per_portion = total_cost / base_portions

    print("-----------------------------------")
    print(f"Total Batch Cost:     ${total_cost:.2f}")
    print(f"Cost Per Portion:     ${cost_per_portion:.2f}")

def main():
    parser = argparse.ArgumentParser(
        description="TenzoToolkit Recipe Cost Calculator"
    )

    parser.add_argument(
        "recipe",
        help="Recipe name to cost"
    )

    args = parser.parse_args()

    cost_recipe(args.recipe)


if __name__ == "__main__":
    main()
