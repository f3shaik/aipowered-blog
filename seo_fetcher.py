import random

def fetch_metrics(keyword: str) -> dict:
    # Generates mock metric data for different keywords, all random
    # Found online that these were the best metrics for SEO tools, https://markitors.com/seo-metrics/
    seed = sum(ord(c) for c in keyword) # ensures reproducibility for the same keyword
    rng = random.Random(seed)

    # search_volume randomly between 1,000 and 100,000, keyword_difficulty between 1 and 100, CPC between $0.10 and $0.50
    search_volume = rng.randint(1000, 100000)
    keyword_difficulty = rng.randint(1, 100)
    cpc = rng.uniform(0.10, 0.50)
    
    return {
        "search_volume": search_volume,
        "keyword_difficulty": keyword_difficulty,
        "cpc": cpc
    }