# fleet_utils.py
# Utility helpers for Vossberg Mobility fleet reporting.
# Written 2013. Modernized 2024: dead code removed, conversion factor corrected.

KM_TO_MILES = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a value as a whole-number percentage string."""
    return f"{int(value)}%"


def is_due(pct: float, threshold: float) -> bool:
    """Return True when wear percentage meets or exceeds the threshold."""
    return pct >= threshold

# Removed (dead code, never called outside this file):
#   mean()             — superseded by statistics.mean since Python 3.4
#   parse_service_date() — only used by the old 2014 garage form, no longer exists
#   chunk_list()       — copied from Stack Overflow 2013, never called
