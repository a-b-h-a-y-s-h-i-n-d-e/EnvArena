from envarena.envs.GuessTheNumber.env import GuessTheNumber
from envarena.wrappers.OllamaWrapper import OllamaWrapper
from envarena.ui.dashboard import Dashboard
import time


env = GuessTheNumber()
llama_1b = OllamaWrapper(model_name="qwen3:8b")
ui = Dashboard()


obs = env.reset()
done = False

ui.start()
try:
    while not done:

        state = env.get_observation()
        ui.update_game_state(f"🎮 State: {state}")


        response_collected = ""
        for token in llama_1b.stream_response(prompt=obs):
            response_collected += token
            ui.update_agent_state(response_collected)

        action = response_collected.strip()

        obs, reward, done, info = env.step(action)

        if done:
            ui.is_win()

        time.sleep(2)

except Exception as e:
    ui.stop()
    print(e)

ui.stop()
results = env.get_results()
print(results)



"""

best model :-
qwen3:4b and later versions
exaone-deep:2.4b

"""