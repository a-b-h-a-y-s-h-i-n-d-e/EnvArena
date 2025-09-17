from envarena.envs import GuessTheNumber, MazeNavigation

ENV_REGISTRY = [
    "GuessTheNumber" : GuessTheNumber,
    "MazeNavigation" : MazeNavigation
]


def get_env(env_name : str):
    if env_name not in ENV_REGISTRY:
        raise ValueError(f"Environment {env_name} not found. Available: {list(ENV_REGISTRY.keys())}")
    return ENV_REGISTRY[env_name]
