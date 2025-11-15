from envarena.envs import GuessTheNumber, MazeNavigation, SocialQA, boolq
from envarena.wrappers.OllamaWrapper import OllamaWrapper
from envarena.wrappers.GeminiWrapper import GeminiWrapper

ENV_REGISTRY = {
    "guessthenumber": GuessTheNumber,
    "mazenavigation": MazeNavigation,
    "socialqa" : SocialQA,
    "boolq" : boolq
}

MODEL_REGISTRY = {
    "ollama": OllamaWrapper,
    "gemini": GeminiWrapper,
}

def get_env(env_name: str):
    if env_name not in ENV_REGISTRY:
        raise ValueError(f"Unknown env: {env_name}. Available: {list(ENV_REGISTRY.keys())}")
    return ENV_REGISTRY[env_name]

def get_model(provider: str):
    if provider not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model provider: {provider}. Available: {list(MODEL_REGISTRY.keys())}")
    return MODEL_REGISTRY[provider]