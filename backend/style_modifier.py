STYLE_SUFFIXES = {
    "realistic": "photorealistic, 4K, highly detailed, natural lighting, DSLR quality",
    "anime": "anime style, Studio Ghibli inspired, vibrant colors, cel shading",
    "sketch": "pencil sketch, hand drawn, black and white, fine line art",
    "oil_painting": "oil painting, textured canvas, classical art, rich colors, brushstrokes",
    "cyberpunk": "cyberpunk, neon lights, futuristic city, dark atmosphere, blade runner style",
    "watercolor": "watercolor painting, soft edges, pastel colors, artistic, fluid"
}

def apply_style(prompt: str, style: str) -> str:
    suffix = STYLE_SUFFIXES.get(style, STYLE_SUFFIXES["realistic"])
    return f"{prompt}, {suffix}"