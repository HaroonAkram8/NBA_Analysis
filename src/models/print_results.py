def print_results(model_name: str, stats: dict):
    header = f"=========================================== {model_name} ==========================================="
    print(header)
    for key in stats:
        print(f"{key}: {stats[key]}")
    print("=" * len(header))
    