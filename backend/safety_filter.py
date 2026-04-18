BLOCKED_KEYWORDS = [
    "nude", "naked", "nsfw", "explicit", "violence", "gore",
    "blood", "weapon", "kill", "terrorist", "child", "minor"
]

def check_safety(prompt: str) -> dict:
    prompt_lower = prompt.lower()
    triggered = [kw for kw in BLOCKED_KEYWORDS if kw in prompt_lower]
    return {"safe": len(triggered) == 0, "triggered": triggered}

# kept for any legacy calls
def is_safe(prompt: str) -> bool:
    return check_safety(prompt)["safe"]