import re

class MazeNavigation:

    def __init__(self):

        self.maze = None
        self.reset()

        self.valid_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def reset(self):
        self.maze = [
            ['#', '#', '#', '#', '#', '#', '#'],
            ['#', 'P', '.', '#', '.', '.', '@'],
            ['#', '#', '.', '#', '.', '.', '#'],
            ['#', '.', '.', '.', '.', '#', '#'],
            ['#', '#', '#', '.', '.', '.', '#'],
            ['#', '.', '.', '.', '#', '.', '#'],
            ['#', '#', '#', '#', '#', '#', '#'],
        ]
        self.player_pos = (1, 1) # P
        self.goal_pos = (1, 6) # @
        self.actions = []
        self.feedbacks = []

    def get_maze(self) -> str:
        result = ""
        for row in self.maze:
            result += " ".join(row) + "\n"
        return result.strip()
    
    def get_observation(self) -> str:
        maze = self.get_maze()
        return f"""
Maze Navigation Game
---------------------------------------------------------
This is a maze navigation game where you need to reach to the goal
position
current position     : P
goal position        : @
previous actions     : {self.actions[-5:]}
feedback for actions : {self.feedbacks[-5:]}

-------------------------------------------------------------

{maze}
-------------------------------------------------------------
available actions : UP, DOWN, LEFT, RIGHT
Format your response as : GUESS : [action]
consider below examples for making responses:
GUESS : UP
GUESS : LEFT
--------------------------------------------------------------
Your Turn :

        """

    def step(self, action : str):
        # observation, reward, done, info
        """
        action : UP, DOWN, LEFT, RIGHT

        """
        action = self.extract_guess(action)
        print("inside action -> ", action)
        self.actions.append(action)

        if action not in self.valid_actions:
            self.feedbacks.append("WRONG_MOVE")
            return (self.get_observation(), -1, False, "WRONG_MOVE")

        row, col = self.player_pos

        if action == "UP":
            new_row, new_col = row - 1, col
        elif action == "DOWN":
            new_row, new_col = row + 1, col
        elif action == "LEFT":
            new_row, new_col = row, col - 1
        elif action == "RIGHT":
            new_row, new_col = row, col + 1
        
        if self.maze[new_row][new_col] == '#':
            self.feedbacks.append("HIT_BY_WALL")
            return (self.get_observation(),  -1, False, "HIT_BY_WALL")

        # if we reach the end goal pos                
        if self.maze[new_row][new_col] == '@':
            return (self.get_observation(), 1, True, "WIN")
        

        # now if everything is okay, we will update the maze
        self.maze[row][col] = '.'
        self.maze[new_row][new_col] = 'P'
        self.player_pos = (new_row, new_col)
        self.feedbacks.append("CORRECT_MOVE")


        return (self.get_observation(), 1, False, None)
    
    def extract_guess(self, response: str) -> str:
        print("inside extract action")
        response = response.strip()
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        response = response.strip()
        
        pattern = r'GUESS\s*:\s*(UP|DOWN|LEFT|RIGHT)'
        match = re.search(pattern, response, re.IGNORECASE)
        
        if match:
            return match.group(1).upper()
        
        return None



        


        







    