from envarena.envs import boolq
from envarena.wrappers.OllamaWrapper import OllamaWrapper
from envarena.ui.dashboard import Dashboard
import time


# increase or decrease the size of num_examples as per compute 
env = boolq(split="validation", num_examples=10)
llama_1b = OllamaWrapper(model_name="gemma3:4b")
ui = Dashboard()

obs = env.reset()
done = False

ui.start()
try:
    while not done:

        state = env.get_observation()
        ui.update_game_state(f"🎮 State: {state}")

        response_collected = ""
        for token in llama_1b.stream_response(prompt=state):
            response_collected += token
            ui.update_agent_state(response_collected)

        action = response_collected.strip()

        obs, reward, done, info = env.step(action)

        if done:
            ui.complete()

        time.sleep(1)


except Exception as e:
    ui.stop()
    print(e)

ui.stop()
results = env.get_results()
print(results)