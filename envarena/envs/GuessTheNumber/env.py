import random, re


class GuessTheNumber:

    def __init__(self,
                 max_attempts : int = 10):
        
        self.max_attempts = max_attempts
        self.reset()

    def reset(self):
        self.target_number = random.randint(1, 20)
        self.attempts_left = self.max_attempts
        self.guesses = []
        self.hints = []
        self.rewards = []
        self.numbers_range = range(1, 21)
        self.win_or_loose = None
        return self.get_observation()
    
    def get_observation(self) -> str:
        return f"""
        NUMBER GUESSING GAME
        -----------------------------------------------
        This is a number guessing game, where you have to guess a number initially
        and then you will get hints such as ( lower / higher )
        You will be rewarded for each decision such as 
        0  : First prediction
        -1 : incorrect choice
        +1 : correct choice
        ------------------------------------------------
        Number range          : from 1 to 20
        Your previous guesses : {self.guesses}
        corresponding hints   : {self.hints}
        Attempts remaining    : {self.attempts_left}
        Rewards earned        : {self.rewards}
        -----------------------------------------------
        Format your response as : GUESS : [your number]
        consider below examples for making responses :
        GUESS : 18
        GUESS : 10
        ------------------------------------------------
        Your turn:
        """
    
    def step(self, action : str):
        # observation, reward, done, info
        # if done == True, stop the game, model has won

        guess = self.extract_guess(action)

        if guess is None:
            return (self.attempts_left, -1, False, "INCORRECT FORMAT")
        
        self.guesses.append(guess)
        self.attempts_left -= 1

        reward = self.calculate_reward(guess)
        self.rewards.append(reward)


        if self.attempts_left > 0:

            if guess not in self.numbers_range:
                self.hints.append("select from given range")
                return (self.get_observation(), -1, False, "INVALID")
        
            if guess == self.target_number:
                self.win_or_loose = True
                return (self.get_observation(), reward, True, "WIN")
            
            if guess < self.target_number:
                self.hints.append("higher")
                return (self.get_observation(), reward, False, "")
            
            if guess > self.target_number:
                self.hints.append("lower")
                return (self.get_observation(), reward, False, "")

        else:
            self.win_or_loose = False
            return (self.get_observation(), -1, True, "LOST")
        
    def extract_guess(self, response: str) -> int:
        response = response.strip()
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        response = response.strip()
        
        pattern = r'GUESS\s*:\s*(\d+)'
        match = re.search(pattern, response, re.IGNORECASE)
        
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        
        return None
    
    def calculate_reward(self, current_guess):

        if len(self.guesses) == 0:
            return 0 # first guess to be neutral
        
        if len(self.hints) == 0:
            return 0 # no hints then return neutral
        
        previous_guess = self.guesses[-2] # last value

        previous_hint = self.hints[-1]


        if previous_hint == 'higher':
            if current_guess > previous_guess:
                return 1
            else:
                return -1
            
        elif previous_hint == 'lower':
            if current_guess < previous_guess:
                return 1
            else:
                return -1
            
        return 0
    
    def get_results(self):
        score = sum(self.rewards)
        results = f"""
            FINAL RESULTS 
            --------------------------------------
            Passed             : {self.win_or_loose}
            Target Value       : {self.target_number}
            Attempts remaining : {self.attempts_left}
            Hints              : {self.hints}
            Guesses            : {self.guesses}
            Rewards            : {self.rewards}
            Score              : {score}
            --------------------------------------
        """

        return results

    
    