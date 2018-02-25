# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import math

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
        scaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if not newFood.asList(): 
            minFoodDistScore = 0
            foodLeftScore = 100
        else: 
            minFoodDistScore = float(100)/min([util.manhattanDistance(newPos, food) for food in newFood.asList()])
            foodLeftScore = 100*(float(len(currentGameState.getFood().asList())) - float(len(newFood.asList())))
        
        if not newGhostStates: minGhostDistScore = 0
        else:
            minGhostDist = min([util.manhattanDistance(newPos, ghost.getPosition()) if ghost.scaredTimer != 1 else 10000 for ghost in newGhostStates])
            minGhostDistScore = - math.exp(-minGhostDist + 7)



        finalScore = minFoodDistScore + minGhostDistScore + foodLeftScore

        # For debugging
        # print "Pos: ", currentGameState.getPacmanPosition(), "Action: ", action
        # print "Food Score: ", minFoodDistScore
        # print "Ghost Score: ", minGhostDistScore
        # print "Food Left Score: ", foodLeftScore
        # print "Total Score: ", finalScore, '\n'

        return finalScore

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        
        availableActions = gameState.getLegalActions(self.index)
        numAgents = gameState.getNumAgents()

        # get successor states from current actions
        successorStates = [[gameState.generateSuccessor(self.index, action), action] for action in availableActions]

        # score each resulting states
        scores = [[self.value(stateAction[0], numAgents, self.index+1), stateAction[1]] for stateAction in successorStates]

        return max(scores)[1]

    def value(self, gameState, numAgents, index):

        if gameState.isWin() or gameState.isLose() or (1 + index/numAgents > self.depth):
            return self.evaluationFunction(gameState)
        if index%numAgents == 0:
            return self.maxValue(gameState, numAgents, index)
        else:
            return self.minValue(gameState, numAgents, index)

    def maxValue(self, gameState, numAgents, index):
        v = float('-inf')

        for action in gameState.getLegalActions(index%numAgents):
            v = max(v, self.value(gameState.generateSuccessor(index%numAgents, action), numAgents, index+1))
        return v

    def minValue(self, gameState, numAgents, index):
        v = float('inf')

        for action in gameState.getLegalActions(index%numAgents):
            v = min(v, self.value(gameState.generateSuccessor(index%numAgents, action), numAgents, index+1))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        numAgents = gameState.getNumAgents()

        # store score action pairs
        scores = [] 

        # initialize
        v = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for action in gameState.getLegalActions(self.index%numAgents):
            successorScore = self.value(gameState.generateSuccessor(self.index%numAgents, action), numAgents, self.index+1, alpha, beta)
            v = max(v, successorScore)
            scores.append([successorScore, action])
            if v > beta: pass
            alpha = max(alpha, v)

        return max(scores)[1]

    # Dispatch function that recursively determines the value of a node
    def value(self, gameState, numAgents, index, alpha, beta):

        if gameState.isWin() or gameState.isLose() or (1 + index/numAgents > self.depth):
            return self.evaluationFunction(gameState)
        if index%numAgents == 0:
            return self.maxValue(gameState, numAgents, index, alpha, beta)
        else:
            return self.minValue(gameState, numAgents, index, alpha, beta)

    # Recursively determines the maximum value of a node
    def maxValue(self, gameState, numAgents, index, alpha, beta):
        v = float('-inf')

        for action in gameState.getLegalActions(index%numAgents):
            v = max(v, self.value(gameState.generateSuccessor(index%numAgents, action), numAgents, index+1, alpha, beta))
            if v > beta: return v
            alpha = max(alpha, v)
        return v

    # Recursively determines the minimum value of a node
    def minValue(self, gameState, numAgents, index, alpha, beta):
        v = float('inf')

        for action in gameState.getLegalActions(index%numAgents):
            v = min(v, self.value(gameState.generateSuccessor(index%numAgents, action), numAgents, index+1, alpha, beta))
            if v < alpha: return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action from the current gameState using self.depth
          and self.evaluationFunction.
        """
        
        availableActions = gameState.getLegalActions(self.index)
        numAgents = gameState.getNumAgents()

        # get successor states from current actions
        successorStates = [[gameState.generateSuccessor(self.index, action), action] for action in availableActions]

        # score each resulting states
        scores = [[self.value(stateAction[0], numAgents, self.index+1), stateAction[1]] for stateAction in successorStates]

        return max(scores)[1]

    def value(self, gameState, numAgents, index):

        if gameState.isWin() or gameState.isLose() or (1 + index/numAgents > self.depth):
            return self.evaluationFunction(gameState)
        if index%numAgents == 0:
            return self.maxValue(gameState, numAgents, index)
        else:
            return self.expValue(gameState, numAgents, index)

    def maxValue(self, gameState, numAgents, index):
        v = float('-inf')

        for action in gameState.getLegalActions(index%numAgents):
            v = max(v, self.value(gameState.generateSuccessor(index%numAgents, action), numAgents, index+1))
        return v

    def expValue(self, gameState, numAgents, index):
        v = 0

        legalActions = gameState.getLegalActions(index%numAgents)

        for action in legalActions:
            p = 1.0/len(legalActions)
            v = v + p*float(self.value(gameState.generateSuccessor(index%numAgents, action), numAgents, index+1))
        return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Evaluation function for evaluating pacman state.
      
      The evaluation function is a linear combination of the following 
      features that are extracted from the pacman game state:
            - Inverse distance to closest food
            - Exponential distance to closest ghost (so pacman is only scared of nearby ghosts)
            - Current game score
    """
    
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    # food scoring
    if not food.asList(): minFoodDistScore = 0
    else: 
        minFoodDistScore = float(500)/min([util.manhattanDistance(pos, foodLoc) for foodLoc in food.asList()])
    
    # ghost scoring
    if not ghostStates: minGhostDistScore = 0
    else:
        minGhostDist = min([util.manhattanDistance(pos, ghost.getPosition()) if ghost.scaredTimer != 1 else 1000 for ghost in ghostStates])
        minGhostDistScore = -math.exp(-1.2*(minGhostDist - 5))


    gameScore = 100*currentGameState.getScore()

    finalScore = minFoodDistScore + minGhostDistScore + gameScore
    return finalScore

# Abbreviation
better = betterEvaluationFunction

