from envarena import Simulator
from envarena.envs import GuessTheNumber
from envarena.wrappers import OllamaWrapper


simulator = Simulator(
    env=GuessTheNumber(),
    model=OllamaWrapper("deepseek-r1:1.5b")
)

simulator.run()
