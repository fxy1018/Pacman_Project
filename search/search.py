# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    
    #create fringe and visited
    fringe = util.Stack()
    visited=[]
    fringe.push((problem.getStartState(),[]))
    
    #loop until fringe is empty
    while not fringe.isEmpty():
        currState, currAct = fringe.pop()
        
        #check whether the current state is goal state
        if problem.isGoalState(currState):
            return currAct
        
        #check whether current state is not visited
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            for successor in successors:
                nextState, action, cost = successor
                fringe.push((nextState,currAct+[action]))
                
    util.raiseNotDefined()
    
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    #create fringe and visited
    fringe = util.Queue()
    visited =[]
    fringe.push((problem.getStartState(),[]))
    
    #loop until fringe is empty
    while not fringe.isEmpty():
        currState, currAct = fringe.pop()
        
        #check whether the current state is goal state
        if problem.isGoalState(currState):
            return currAct
        visited.append(currState)
        successors = problem.getSuccessors(currState)
        for successor in successors:
            nextState, action, cost = successor
            #check whether the nextState is not in the visit queue and not in the fringe
            if (nextState not in visited) and (nextState not in [i[0] for i in fringe.list]):
                fringe.push((nextState,currAct+[action]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"    
    
    #create fringe and visited
    fringe = util.PriorityQueue()
    visited =[]
    fringe.push((problem.getStartState(),[],0),0)
    
    #loop until fringe is empty
    while not fringe.isEmpty():
        currState, currAct, currcost = fringe.pop()

        #check whether the current state is goal state
        if problem.isGoalState(currState):
            return currAct
        visited.append(currState)
        successors = problem.getSuccessors(currState)
        for successor in successors:
            nextState, action, cost = successor
            
            #calculate the cost of next state
            newCost = currcost+cost
            if (nextState not in visited) and (nextState not in [j[0] for j in [i[2] for i in fringe.heap]]):
                fringe.push((nextState,currAct+[action],newCost), newCost)
            elif nextState in [j[0] for j in [i[2] for i in fringe.heap]] and newCost < getCost(nextState, fringe):    
                fringe.push((nextState, currAct+[action],newCost),newCost)

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    print("Start:", problem.getStartState())
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #create fringe and visited
    fringe = util.PriorityQueueWithFunction(lambda x: x[2]+x[3])
    visited =[]
    h = heuristic(problem.getStartState(),problem)
    fringe.push((problem.getStartState(),[],0,h))
    
    #loop until fringe is not empty
    while not fringe.isEmpty():
        currState, currAct, currcost, last_h = fringe.pop()

        #check whether the current state is goal state
        if problem.isGoalState(currState):
            return currAct
        visited.append(currState)
        successors = problem.getSuccessors(currState)
        
        for successor in successors:
            nextState, action, cost = successor
            newCost = currcost+cost
            
            if (nextState not in visited) and (nextState not in [j[0] for j in [i[2] for i in fringe.heap]]):
                next_h = heuristic(nextState, problem) 
                fringe.push((nextState,currAct+[action],newCost,next_h))
                
            elif nextState in [j[0] for j in [i[2] for i in fringe.heap]] and newCost+next_h < getCost(nextState, fringe):
                fringe.push((nextState, currAct+[action],newCost,next_h))
               
    util.raiseNotDefined()

#help function
def getCost(nextState, fringe):
    prio, counts, item = zip(*fringe.heap)
    if len(item[0]) == 3:
        states, path, cost= zip(*item)
    elif len(item[0])==4:
        states,path,cost,heri = zip(*item)

    return(prio[states.index(nextState)])
    
      
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
