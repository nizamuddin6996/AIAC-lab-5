from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Iterable, Tuple, Set


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    category: str
    brand: str
    popularity_score: float  # 0.0 - 1.0 proxy for rating/sales


CATALOG: List[Product] = [
    Product("p1", "Noise-Canceling Headphones", "electronics", "AcoustiCo", 0.92),
    Product("p2", "Wireless Mouse", "electronics", "ClickRight", 0.78),
    Product("p3", "Python for Everyone", "books", "Bookify", 0.85),
    Product("p4", "Mystery Novel", "books", "PageTurner", 0.65),
    Product("p5", "Cotton T-Shirt", "clothing", "ComfyWear", 0.74),
    Product("p6", "Running Shoes", "clothing", "FleetFeet", 0.81),
    Product("p7", "Blender 600W", "home", "HomeEase", 0.68),
    Product("p8", "Ceramic Cookware Set", "home", "KitchenPro", 0.88),
    Product("p9", "STEM Building Kit", "toys", "EduPlay", 0.79),
    Product("p10", "Board Game Classic", "toys", "FunBox", 0.72),
    Product("p11", "Hydrating Face Serum", "beauty", "GlowLab", 0.83),
    Product("p12", "Sunscreen SPF50", "beauty", "SunSafe", 0.76),
]


def parse_csv_words(value: str) -> Set[str]:
    return {part.strip().lower() for part in value.split(",") if part.strip()}


def build_user_profile_from_console() -> Tuple[Set[str], Set[str], int]:
    print("We only use the inputs you provide here (interests and exclusions). No personal data is stored.")
    interests_input = input(
        "Enter a few categories you like (comma-separated, e.g., electronics, books), or leave blank: "
    ).strip()
    exclude_input = input(
        "Optionally enter categories to exclude (comma-separated), or leave blank: "
    ).strip()
    top_n_raw = input("How many recommendations would you like? (default 6): ").strip()

    interests = parse_csv_words(interests_input)
    excluded = parse_csv_words(exclude_input)
    try:
        top_n = int(top_n_raw) if top_n_raw else 6
    except ValueError:
        top_n = 6

    return interests, excluded, max(1, min(top_n, 12))


def score_product(product: Product, preferred_categories: Set[str], alpha: float = 0.7, beta: float = 0.3) -> float:
    category_match = 1.0 if product.category in preferred_categories else 0.0
    return alpha * category_match + beta * product.popularity_score


def enforce_category_diversity(
    ranked_products: Iterable[Tuple[Product, float, List[str]]],
    top_n: int,
    max_per_category: int = 2,
) -> List[Tuple[Product, float, List[str]]]:
    results: List[Tuple[Product, float, List[str]]] = []
    per_category: Dict[str, int] = {}

    for product, score, reasons in ranked_products:
        if len(results) >= top_n:
            break
        count = per_category.get(product.category, 0)
        if count >= max_per_category:
            continue
        per_category[product.category] = count + 1
        results.append((product, score, reasons))

    if len(results) < top_n:
        seen_ids = {p.product_id for p, _, _ in results}
        for product, score, reasons in ranked_products:
            if len(results) >= top_n:
                break
            if product.product_id in seen_ids:
                continue
            results.append((product, score, reasons + ["included for diversity"]))
            seen_ids.add(product.product_id)

    return results[:top_n]


def recommend_products(
    catalog: List[Product],
    preferred_categories: Set[str],
    excluded_categories: Set[str],
    top_n: int = 6,
) -> List[Tuple[Product, float, List[str]]]:
    filtered = [p for p in catalog if p.category not in excluded_categories]

    annotated: List[Tuple[Product, float, List[str]]] = []
    for product in filtered:
        reasons: List[str] = []
        if product.category in preferred_categories:
            reasons.append(f"matches your interest in '{product.category}'")
        if product.popularity_score >= 0.8:
            reasons.append("popular with similar shoppers")
        score = score_product(product, preferred_categories)
        annotated.append((product, score, reasons or ["balanced relevance and popularity"]))

    annotated.sort(key=lambda t: (t[1], t[0].product_id), reverse=True)
    diversified = enforce_category_diversity(annotated, top_n=top_n, max_per_category=2)
    return diversified


def print_transparency_notice() -> None:
    print("\nTransparency and fairness policy:")
    print("- We recommend based on the categories you provided and product popularity (no personal or sensitive data).")
    print("- Scoring: 70% category match + 30% popularity. We cap recommendations to avoid over-concentration in one category.")
    print("- We avoid using protected attributes and include variety to reduce filter bubbles. You can exclude categories explicitly.")


def print_recommendations(recommendations: List[Tuple[Product, float, List[str]]]) -> None:
    print("\nRecommended products:")
    for rank, (product, score, reasons) in enumerate(recommendations, start=1):
        reason_text = "; ".join(reasons)
        print(f"{rank}. {product.name} (Category: {product.category}, Brand: {product.brand})")
        print(f"   Why: {reason_text} | Score: {score:.2f}")

    categories = {}
    for product, _, _ in recommendations:
        categories[product.category] = categories.get(product.category, 0) + 1
    print("\nFairness check (category distribution):")
    for category, count in sorted(categories.items()):
        print(f"- {category}: {count}")


def main() -> None:
    print_transparency_notice()
    interests, excluded, top_n = build_user_profile_from_console()

    proceed = input("Proceed with these inputs? (y/n): ").strip().lower()
    if proceed not in {"y", "yes", ""}:
        print("No recommendations generated.")
        return

    recs = recommend_products(CATALOG, preferred_categories=interests, excluded_categories=excluded, top_n=top_n)
    print_recommendations(recs)
    print("\nNote: You can re-run and adjust interests or exclusions to influence results.")


if __name__ == "__main__":
    main()



