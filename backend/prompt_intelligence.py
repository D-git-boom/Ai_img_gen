# Week 2 we'll hook a real NLP model here
# For now: rule-based expansion so the pipeline works end to end

def expand_prompt(prompt: str) -> str:
    additions = [
        "highly detailed",
        "professional composition",
        "dramatic lighting",
        "8K resolution",
        "award winning photography"
    ]
    return f"{prompt}, {', '.join(additions)}"