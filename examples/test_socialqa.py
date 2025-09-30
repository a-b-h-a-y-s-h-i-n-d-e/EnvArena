from envarena.envs import SocialQA
from envarena.wrappers.OllamaWrapper import OllamaWrapper
from envarena.ui.dashboard import Dashboard
import time


# the dataset contains thousands of questions, so if you have compute you can increase the n_samples
env = SocialQA(n_samples = 2)
model = OllamaWrapper(model_name="deepseek-r1:7b")
ui = Dashboard()


done = False

ui.start()
try:
    while not done:

        state = env.get_observation()
        ui.update_game_state(f"🎮 State: {state}")

        if env.done:
            break


        response_collected = ""
        for token in model.stream_response(prompt=state):
            response_collected += token
            ui.update_agent_state(response_collected)

        action = response_collected.strip()

        obs, reward, done, info = env.step(action)
        time.sleep(2)

except Exception as e:
    ui.stop()
    print(e)

finally:
    ui.stop()

print(env.get_results())
