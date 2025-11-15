from envarena.ui import Dashboard
import time


class Simulator:

    def __init__(self, env, model_wrapper, delay=1):

        self.env = env
        self.model = model_wrapper
        self.delay = delay

        self.ui = Dashboard()

    def run(self):        
        self.ui.start()
        done = False
        obs = self.env.reset()

        try:
            while not done:
                
                state = self.env.get_observation()
                self.ui.update_game_state(f"🎮 State: {state}")

                response_collected = ""
                for token in self.model.stream_response(prompt=obs):
                    response_collected += token
                    self.ui.update_agent_state(response_collected)

                action = response_collected.strip()

                obs, reward, done, info = self.env.step(action)

                if done:
                    self.ui.win()

                time.sleep(1)

        except KeyboardInterrupt:
            self.ui.stop()
            print("\n Simulation interrupted by user")

        except Exception as e:
            self.ui.stop()
            print(e)

        finally:
            self.ui.stop()

        print(self.env.get_results())
