import random

class AI_AGENT:
    def __init__(self):
        # You can initialize any internal states or variables here
        pass

    def GET_AI_OUTPUT(self):
        """
        This method returns AI outputs for controlling the car.

        For demonstration purposes, we're using random values.
        In a real implementation, you'd replace this logic with your AI's decision-making process.

        Returns:
        - A list of floats representing the AI's decisions. 
          [turn_left_value, turn_right_value, move_forward_value, brake_value]
        """
        return [random.random() for _ in range(4)]