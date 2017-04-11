# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #print some value 
#         print(self.mdp.getStartState())
#         print(self.mdp.getStates())
#         print(self.mdp.getPossibleActions(self.mdp.getStartState()))
#         print(self.mdp.getTransitionStatesAndProbs(self.mdp.getStartState(),"north"))
        
        #initialization of values are 0
        states = self.mdp.getStates() 
        
        #doing iteration
        for i in range(self.iterations):
            #record all values from last step
            values_copy = self.values.copy()
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                max_v = -float("Inf")
                for action in actions:
                    max_v = max(max_v, self.getQValue(state, action)) 
                #if max_v is intialized value which means the state doesn't have possible actions
                if max_v == -float("Inf"):
                    max_v =self.values[state]
                #save new Qvalue to copy dictionary
                values_copy[state] = max_v
            #update new iteration values
            self.values = values_copy

        
        
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #get state successors (next states)
        successors = self.mdp.getTransitionStatesAndProbs(state,action)
        temp_value = 0
        #calculate expected value
        for next_state,prob in successors:
            temp_reward = self.mdp.getReward(state, action, next_state)
            temp_value += prob * (temp_reward + (self.discount * self.values[next_state]))
#       
        return(temp_value)
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        if not actions:
#         if state == "TERMINAL_STATE":
            return(None)
        
        
        max_value = self.values[state]
        res = None
        #find the action wiht maximum value
        for action in actions:
            if max_value <= self.getQValue(state, action): 
                max_value = self.getQValue(state, action)  
                res = action
        return(res)
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
