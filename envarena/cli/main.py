import argparse, time
from envarena.registry import get_env, get_model
from envarena.ui.dashboard import Dashboard

def main():
    parser = argparse.ArgumentParser(description="Run Envarena environments with LLMs")
    parser.add_argument("--env", required=True, help="Environment name (e.g., MazeNavigation)")
    parser.add_argument("--model", required=True, help="Model spec (e.g., ollama:llama3.2:1b)")
    args = parser.parse_args()

    # Setup env + model
    EnvClass = get_env(args.env)
    env = EnvClass()

    provider, model_name = args.model.split(":", 1)
    ModelClass = get_model(provider)
    model = ModelClass(model_name=model_name)

    # Setup UI
    ui = Dashboard()
    ui.start()

    done = False
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
        print(f"Error: {e}")
    finally:
        ui.stop()
