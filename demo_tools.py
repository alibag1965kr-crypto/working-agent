"""Test tools without involving the AI model."""

from tools import calculate_budget, check_resources


# Test 1: Normal budget calculation
result = calculate_budget(30, 2, 200, 15000)

assert result["total_estimated_cost"] == 12000
assert result["remaining_budget"] == 3000
assert result["within_budget"] is True


# Test 2: Over-budget scenario
result = calculate_budget(30, 2, 200, 10000)

assert result["total_estimated_cost"] == 12000
assert result["remaining_budget"] == -2000
assert result["within_budget"] is False


# Test 3: Equipment aliases and missing equipment
result = check_resources(
    "beamer, WIFI, wifi, microphones"
)

assert result == {
    "available": ["projector", "wi-fi"],
    "missing": ["microphones"],
}


# Test 4: Invalid numerical inputs
invalid_values = [
    True,
    0,
    -1,
    "30",
    1.5,
    1_000_001,
]

for bad_value in invalid_values:
    try:
        calculate_budget(
            bad_value, 2, 200, 15000
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            f"Invalid input was accepted: {bad_value!r}"
        )


# Test 5: Empty resource list
try:
    check_resources(" , , ")
except ValueError:
    pass
else:
    raise AssertionError(
        "An empty resource list was accepted"
    )


print("All direct tool checks passed successfully.")