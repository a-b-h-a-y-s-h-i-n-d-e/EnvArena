import random, re
from datasets import Dataset, load_dataset

class SocialQA:

    def __init__(self, 
                 n_samples : int = 10):
        
        self.n_samples = n_samples
        
        self.answer_map = {'A' : 1, 'B' : 2, 'C' : 3}
        self.data_path = self.download_data()
        self.data = self.load_data(self.data_path)
        self.done = False
        self.current_question_idx = None
        self.reset()
        

    def reset(self):
        self.indices = random.sample(range(1, len(self.data)), self.n_samples)
        self.current_step = 0
        self.rewards = []
        

    def get_observation(self) -> str:
        if self.current_step >= self.n_samples:
            self.done = True
            return " All Questions completed "
        
        self.current_question_idx = self.indices[self.current_step]
        
        # prompt
        return f"""
        Context :
        {self.data[self.current_question_idx]['context']}
        -----------------------------------------------------------
        Question : 
        {self.data[self.current_question_idx]['question']}
        -----------------------------------------------------------
        Options : 
        A - {self.data[self.current_question_idx]['answerA']}
        B - {self.data[self.current_question_idx]['answerB']}
        C - {self.data[self.current_question_idx]['answerC']}
        -----------------------------------------------------------
        Format your response as : GUESS : [action]
        consider below examples for making responses:
        GUESS : A
        GUESS : B
        -----------------------------------------------------------
        Your turn : 

        """

    def step(self, action : str):
        # observation, reward, done, info

        if self.current_step >= self.n_samples:
            self.done = True
            return (self.get_observation(), 0, True, "GAME_OVER")

        guess = self.extract_guess(action)

        if guess is None:
            return (self.get_observation(), -1, False, "INCORRECT FORMAT")
        
        reward = self.calculate_reward(guess)
        self.rewards.append(reward)

        self.current_step += 1
        return (self.get_observation(), 1, False, "")


    # helper functions
    def calculate_reward(self, guess):
        label = self.data[self.current_question_idx]['label']
        is_correct = self.answer_map.get(guess.upper()) == label
        return 1 if is_correct else 0

    def download_data(self):
        ds = load_dataset("allenai/social_i_qa",trust_remote_code=True)
        validation_path = ds["validation"].cache_files[0]["filename"]

        return validation_path
        
    def load_data(self, file_path):
        data = Dataset.from_file(file_path)
        return data
    
    def extract_guess(self, response: str) -> str:
        response = response.strip()
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        response = response.strip()
        
        pattern = r'GUESS\s*:\s*(A|B|C|D)'
        match = re.search(pattern, response, re.IGNORECASE)
        
        if match:
            return match.group(1).upper()
        
        return None
    
    def get_results(self):
        score = sum(self.rewards)
        results = f"""
            FINAL RESULTS 
            --------------------------------------------
            n_samples   : {self.n_samples}
            score       : {score}
        """
        return results
    
        