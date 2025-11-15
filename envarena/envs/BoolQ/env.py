from datasets import load_dataset, Dataset
import random, re

class boolq:

    def __init__(self,
                split : str ="validation",
                num_examples : int = 10):
        
        self.split = split
        self.num_examples = num_examples
        self.data_path = self.download_data(self.split)
        self.data = self.load_data(self.data_path)

        self.reset()
    
    def reset(self):
        self.indices = random.sample(list(range(1, len(self.data))), self.num_examples)
        self.current_step = 0
        self.attempts_left = self.num_examples
        self.rewards = []
        self.actions = []


    def get_observation(self):
        
        return f"""
        BoolQ question answering environment
        ---------------------------------------------------------------
        This is a question answer environment in which you will get a passage and a question
        based on that passage you just need to answer it in True/False
        You will be rewarded for each decision as 
        +1 : correct choice
        0  : incorrect choice
        ----------------------------------------------------------------
        passage : 
        {self.data[self.current_step]['passage']}

        Question:
        {self.data[self.current_step]['question']}

        ----------------------------------------------------------------
        Format your response as : GUESS : [your answer either True or False]
        consider below examples for making responses: 
        GUESS : True
        GUESS : False
        -----------------------------------------------------------------
        Your turn: 

        """.strip()

    def step(self, action : str):
        """
        action : True / False
        """
        action = self.extract_guess(action)
        self.actions.append(action)

        reward = self.calculate_reward(action)
        self.rewards.append(reward)

        # just update the current_step so that index for questions move forward
        self.attempts_left -= 1
        self.current_step += 1

        if self.attempts_left > 0:

            if reward == 1:
                return (self.get_observation(), reward, False, "")
            else:
                return (self.get_observation(), reward, False, "")
        
        else:
            return (self.get_observation(), -1, True, "")



    def calculate_reward(self, action):
        label = self.data[self.current_step]['answer']
        if label is True and action == "true":
            return 1
        else:
            return 0


    def download_data(self, split):
        ds = load_dataset("google/boolq", trust_remote_code=True)
        if split == "validation":
            ds_path = ds["validation"].cache_files[0]["filename"]
        else:
            ds_path = ds["train"].cache_files[0]["filename"]
        return ds_path
    
    def load_data(self, file_path):
        data = Dataset.from_file(file_path)
        return data
    

    def extract_guess(self, action):
        response = re.sub(r'<think>.*?</think>', '', action, flags=re.DOTALL)
        response = action.strip()

        pattern = r'GUESS\s*:\s*(true|false)'
        match = re.search(pattern, response, re.IGNORECASE)

        return match.group(1).lower() if match else None
    
    def get_results(self):
        score = sum(self.rewards)
        results = f"""
        FINAL RESULTS
        --------------------------------------------
        number of questions : {self.num_examples}
        final score         : {score}

        """.strip()
        return results        


