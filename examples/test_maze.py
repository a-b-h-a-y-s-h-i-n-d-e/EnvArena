from envarena.envs import MazeNavigation
from envarena.wrappers.OllamaWrapper import OllamaWrapper
from envarena.ui.dashboard import Dashboard
import time

env = MazeNavigation()
model = OllamaWrapper(model_name="deepseek-r1:8b")
ui = Dashboard()


done = False

ui.start()
try:
    while not done:

        state = env.get_observation()
        ui.update_game_state(f"🎮 State: {state}")


        response_collected = ""
        for token in model.stream_response(prompt=state):
            response_collected += token
            ui.update_agent_state(response_collected)

        action = response_collected.strip()

        obs, reward, done, info = env.step(action)

        if done:
            ui.win()

        time.sleep(2)

except Exception as e:
    ui.stop()
    print(e)

finally:
    ui.stop()
