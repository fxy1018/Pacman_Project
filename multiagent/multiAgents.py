# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print("action:", action)
        #print("successorGameState:", successorGameState)
        #print("newPos:", newPos)
        #print("newFood:", newFood.asList())
        #print("newGhostStates:", newGhostStates)
        #print("newScaredTimes",newScaredTimes)
        
        #assume weight of food and ghost
        food_weight = 1
        ghost_weight = 5
        score = successorGameState.getScore()
        foods_dis = [manhattanDistance(newPos, food) for food in newFood.asList()]
        if len(foods_dis) > 0:
            food_dis = min(foods_dis)
        else:
            food_dis = 0
    
        ghosts_dis = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        
        for i in range(len(newScaredTimes)):
            if newScaredTimes[i] == 0:
                ghosts_dis[i] = -1*ghosts_dis[i] 

        if food_dis > 0:
            for g in ghosts_dis:
                if g != 0:
                    score = score + food_weight*(1.0/food_dis) + ghost_weight*(1.0/g)
        return(score)
    
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        actions = gameState.getLegalActions(0)
        score = -float("Inf")
        res_action = actions[0]
        for a in actions:
            min_value = self.Min_Value(gameState.generateSuccessor(0,a),self.depth,1)
            if score < min_value:
                score = min_value
                res_action = a
    
        return(res_action)
        util.raiseNotDefined()
        
    def Max_Value(self, gameState,depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return(self.evaluationFunction(gameState))
        
        v = -float("Inf")
        actions = gameState.getLegalActions(0)
        
        for a in actions:
            v = max(v, self.Min_Value(gameState.generateSuccessor(0,a),depth,1))
        
        return(v)
    
    def Min_Value(self, gameState, depth, agentindex):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return(self.evaluationFunction(gameState))
        
        v = float("Inf")
        actions = gameState.getLegalActions(agentindex)
        if agentindex == gameState.getNumAgents()-1:   
            for a in actions:
                v = min(v, self.Max_Value(gameState.generateSuccessor(agentindex,a), depth-1))
        else:
            for a in actions:
                v = min(v, self.Min_Value(gameState.generateSuccessor(agentindex,a), depth,agentindex+1))
        
        return(v)  

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        actions = gameState.getLegalActions(0)
        score = -float("Inf")
        alpha = -float("Inf")
        beta = float("Inf")
        res_action = actions[0]
        for a in actions:
            min_value = self.Min_Value(gameState.generateSuccessor(0,a),self.depth, alpha,beta,1)
            if score < min_value:
                score = min_value
                res_action = a
            if min_value > beta:
                return(a)
            alpha = max(min_value, alpha)
    
        return(res_action)
        
        util.raiseNotDefined()
        
    def Max_Value(self, gameState,depth,alpha,beta):
        if gameState.isWin() or gameState.isLose() or depth==0:
            return(self.evaluationFunction(gameState))
        
        v = -float("Inf")
        actions = gameState.getLegalActions(0)
        
        for a in actions:
            v = max(v, self.Min_Value(gameState.generateSuccessor(0,a),depth,alpha,beta,1))
            if v > beta:
                return(v)
            alpha = max(alpha,v)
        return(v)
    
    def Min_Value(self, gameState,depth, alpha,beta, agentindex):
        if gameState.isWin() or gameState.isLose() or depth ==0:
            return(self.evaluationFunction(gameState))
        
        actions = gameState.getLegalActions(agentindex)
        v = float("Inf") 
        
        if agentindex == gameState.getNumAgents()-1: 
            for a in actions:
                v = min(v, self.Max_Value(gameState.generateSuccessor(agentindex,a), depth-1, alpha, beta))
                if v < alpha:
                    return(v)
                beta = min(beta,v)
        else:
            for a in actions:
                v = min(v, self.Min_Value(gameState.generateSuccessor(agentindex,a), depth, alpha, beta, agentindex+1))
                if v < alpha:
                    return(v)
                beta = min(beta,v)
        return(v)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        score = -float("Inf")
        res_action = actions[0]
        for a in actions:
            min_value = self.Average_Value(gameState.generateSuccessor(0,a),self.depth,1)
            if score < min_value:
                score = min_value
                res_action = a
    
        return(res_action)
        util.raiseNotDefined()
        
    def Max_Value(self, gameState,depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return(self.evaluationFunction(gameState))
        
        v = -float("Inf")
        actions = gameState.getLegalActions(0)
        
        for a in actions:
            v = max(v, self.Average_Value(gameState.generateSuccessor(0,a),depth,1))
        
        return(v)
    
    def Average_Value(self, gameState, depth, agentindex):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return(self.evaluationFunction(gameState))
        
        values = []
        actions = gameState.getLegalActions(agentindex)
        for a in actions:
            if agentindex == gameState.getNumAgents()-1:   
                values.append(self.Max_Value(gameState.generateSuccessor(agentindex,a), depth-1))
            else:
                values.append(self.Average_Value(gameState.generateSuccessor(agentindex,a), depth,agentindex+1))
        v = sum(values)/float(len(values))
        return(v) 
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The strategy used here is similar to q1. In currentGameState, get the minimized distance of food and all ghosts' position.
                   Here, set weight of ghost as 5 and weight of food as 1 because the amount of food is much greater than ghost. If ghost is
                   in scareTime, the score of ghost is positive; if ghost is not in scareTime, the score of ghost is negative. Use linear
                   combination add all scores.
    """
    "*** YOUR CODE HERE ***"
    

    pacmanPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()        
    ScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    
    #assume weight of food and ghost
    food_weight = 1
    ghost_weight = 5
    
    score = currentGameState.getScore()
    foods_dis = [manhattanDistance(pacmanPos, food) for food in foods.asList()]
    if len(foods_dis) > 0:
        food_dis = min(foods_dis)
    else:
        food_dis = 0

    ghosts_dis = [manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in ghostStates]
    
    for i in range(len(ScaredTimes)):
        if ScaredTimes[i] == 0:
            ghosts_dis[i] = -1*ghosts_dis[i] 

    if food_dis > 0:
        for g in ghosts_dis:
            if g != 0:
                score = score + food_weight*(1.0/food_dis) + ghost_weight*(1.0/g)
    return(score)
    
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction

