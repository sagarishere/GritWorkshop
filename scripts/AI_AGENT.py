import neat.nn

class AI_AGENT:
    def __init__(self, genome, config):
        self.genome = genome
        self.network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.inputs = []
    
    def TARGET_FUNCTION(self):
        #declare what game state gives reward / fitness
        pass

    def SAVE_AGENT(self):
        pass

    def AI_INPUT(self, inputs):
        # Here, you'd prepare your game's state as input to the neural network
        # This should return a list of normalized inputs for the network
        self.inputs = inputs

    def GET_AI_OUTPUT(self):
        # Activate the neural network and get the outputs
        raw_outputs = self.network.activate(self.inputs)
        # Adjust outputs to the range [0.5, 1.5]
        adjusted_outputs = [o + 0.5 for o in raw_outputs]
        return adjusted_outputs