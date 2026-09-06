"""
Application entry point for the test repository.

Demonstrates:
- imports
- function calls
- class instantiation
- method calls
- arguments
- return types
"""

from utils import format_response, calculate_total
from services.some_file import UserService, create_user


def build_user_response(
    name: str,
    age: int,
) -> dict:
    """Build a formatted response for a user."""

    user = create_user(
        name=name,
        age=age,
    )

    service = UserService()

    profile = service.get_profile(user["id"])

    return format_response(profile)


def calculate_order_total(
    prices: list[float],
    tax_rate: float,
) -> float:
    """Calculate the final order total including tax."""

    subtotal = calculate_total(prices)

    return subtotal + (
        subtotal * tax_rate
    )


def main() -> None:
    """Run the application."""

    response = build_user_response(
        name="Linga",
        age=30,
    )

    total = calculate_order_total(
        prices=[100.0, 200.0, 50.0],
        tax_rate=0.18,
    )

    print(response)
    print(total)


if __name__ == "__main__":
    main()
