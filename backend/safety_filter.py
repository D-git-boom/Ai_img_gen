# Keyword-based filter for now (Week 4 we'll upgrade to ML classifier)
BLOCKED_KEYWORDS = [
    "nude", "naked", "nsfw", "explicit", "violence", "gore",
    "blood", "weapon", "kill", "terrorist", "child", "minor"
]

def is_safe(prompt: str) -> bool:
    prompt_lower = prompt.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in prompt_lower:
            return False
    return True