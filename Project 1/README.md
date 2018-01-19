# cs151-search
## Project 1: Search in Pacman

Version 1.003\. Last Updated: 09/04/2017\.

* * *

### Table of Contents

*   [Introduction](#Introduction)
*   [Welcome](#Welcome)
*   [Q1: Depth First Search](#Q1)
*   [Q2: Breadth First Search](#Q2)
*   [Q3: Uniform Cost Search](#Q3)
*   [Q4: A* Search](#Q4)
*   [Q5: Corners Problem: Representation](#Q5)
*   [Q6: Corners Problem: Heuristic](#Q6)
*   [Q7: Eating All The Dots: Heuristic](#Q7)
*   [Q8: Suboptimal Search](#Q8)
*   [Glossary](#Glossary)
*   [Submission](#Submission)

* * *


![](https://github.com/HEATlab/cs151-search/blob/master/maze.png)
> 
> <center>All those colored walls,  
> Mazes give Pacman the blues,  
> So teach him to search.</center>

### <a name="Introduction"></a>Introduction

In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios.

**NOTE:** The projects for this class assume you use Python 2.7. Python 2.7 is already installed on CS lab machines, but you are also free to use your own machine.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

<pre>python autograder.py</pre>

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore. You can download all the code and supporting files as a [zip archive](https://github.com/HEATlab/cs151-search/archive/master.zip).

<table class="intro" border="0" cellpadding="10">

<tbody>

<tr>

<td colspan="2">**Files you'll edit:**</td>

</tr>

<tr>

<td>search.py</td>

<td><text>Where all of your search algorithms will reside.</text></td>

</tr>

<tr>

<td>searchAgents.py</td>

<td>Where all of your search-based agents will reside.</td>

</tr>

<tr>

<td colspan="2">**Files you should read but NOT edit:**</td>

</tr>

<tr>

<td>pacman.py</td>

<td>The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project.</td>

</tr>

<tr>

<td>game.py</td>

<td>The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.</td>

</tr>

<tr>

<td>util.py</td>

<td>Useful data structures for implementing search algorithms.</td>

</tr>

<tr>

<td colspan="2">**Supporting files you can ignore:**</td>

</tr>

<tr>

<td>graphicsDisplay.py</td>

<td>Graphics for Pacman</td>

</tr>

<tr>

<td>graphicsUtils.py</td>

<td>Support for Pacman graphics</td>

</tr>

<tr>

<td>textDisplay.py</td>

<td>ASCII graphics for Pacman</td>

</tr>

<tr>

<td>ghostAgents.py</td>

<td>Agents to control ghosts</td>

</tr>

<tr>

<td>keyboardAgents.py</td>

<td>Keyboard interfaces to control Pacman</td>

</tr>

<tr>

<td>layout.py</td>

<td>Code for reading layout files and storing their contents</td>

</tr>

<tr>

<td>autograder.py</td>

<td>Project autograder</td>

</tr>

<tr>

<td>testParser.py</td>

<td>Parses autograder test and solution files</td>

</tr>

<tr>

<td>testClasses.py</td>

<td>General autograding test classes</td>

</tr>

<tr>

<td>`test_cases/`</td>

<td>Directory containing the test cases for each question</td>

</tr>

<tr>

<td>searchTestClasses.py</td>

<td>Project 1 specific autograding test classes</td>

</tr>

</tbody>

</table>

**Files to Edit and Submit:** You will fill in portions of [search.py](https://github.com/HEATlab/cs151-search/blob/master/search.py) and [searchAgents.py](https://github.com/HEATlab/cs151-search/blob/master/searchAgents.py) during the assignment. You should submit these files with your code and comments. Please _do not_ change the other files in this distribution or submit any of our original files other than these files.

**Evaluation:** Your code will be autograded for technical correctness. Please _do not_ change the names of any provided functions or classes within the code, or you will wreak havoc on the autograder. However, the correctness of your implementation -- not the autograder's judgements -- will be the final judge of your score. If necessary, we will review and grade assignments individually to ensure that you receive due credit for your work.

**Academic Dishonesty:** We will be checking your code against other submissions in the class for logical redundancy. If you copy someone else's code and submit it with minor changes, we will know. These cheat detectors are quite hard to fool, so please don't try. We trust you all to submit your own work only; _please_ don't let us down. If you do, we will pursue the strongest consequences available to us.

**Getting Help:** You are not alone! If you find yourself stuck on something, contact the course staff for help. Office hours, grutoring hours, and the Piazza forum are there for your support; please use them. If you can't make our office hours, let us know and we will schedule more. We want these projects to be rewarding and instructional, not frustrating and demoralizing. But, we don't know when or how to help unless you ask.

**Discussion:** Please be careful not to post spoilers.


### <a name="Welcome"></a>Welcome to Pacman

After downloading the code (https://github.com/HEATlab/cs151-search/archive/master.zip), unzipping it, and changing to the directory, you should be able to play a game of Pacman by typing the following at the command line:

<pre>python pacman.py</pre>

Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pacman's first step in mastering his domain.

The simplest agent in `searchAgents.py` is called the `GoWestAgent`, which always goes West (a trivial reflex agent). This agent can occasionally win:

<pre>python pacman.py --layout testMaze --pacman GoWestAgent</pre>

But, things get ugly for this agent when turning is required:

<pre>python pacman.py --layout tinyMaze --pacman GoWestAgent</pre>

If Pacman gets stuck, you can exit the game by typing CTRL-c into your terminal.

Soon, your agent will solve not only `tinyMaze`, but any maze you want.

Note that `pacman.py` supports a number of options that can each be expressed in a long way (e.g., `--layout`) or a short way (e.g., `-l`). You can see the list of all options and their default values via:

<pre>python pacman.py -h</pre>

Also, all of the commands that appear in this project also appear in `commands.txt`, for easy copying and pasting. In UNIX/Mac OS X, you can even run all these commands in order with `bash commands.txt`.

Note: if you get error messages regarding Tkinter, see [this page](http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter).

* * *

### <a name="Q1"></a>Question 1 (3 points): Finding a Fixed Food Dot using Depth First Search

In `searchAgents.py`, you'll find a fully implemented `SearchAgent`, which plans out a path through Pacman's world and then executes that path step-by-step. **The search algorithms for formulating a plan are not implemented -- that's your job.** As you work through the following questions, you might find it useful to refer to the object glossary (Glossary section below).

**First, test that the `SearchAgent` is working correctly by running:**

<pre>python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch</pre>

The command above tells the `SearchAgent` to use `tinyMazeSearch` as its search algorithm, which is implemented in `search.py`. Pacman should navigate the maze successfully.

Now it's time to write full-fledged generic search functions to help Pacman plan routes! For your reference, the general search algorithm from lecture is as follows:

![](https://github.com/HEATlab/cs151-search/blob/master/hw1_graph-search.png)

**Implement the depth-first search (DFS) algorithm in the `depthFirstSearch` function in `search.py`.** To make your algorithm _complete_, write the graph search version of DFS, which avoids expanding any already visited states.

Your code should quickly find a solution for:

<pre>python pacman.py -l tinyMaze -p SearchAgent</pre>

<pre>python pacman.py -l mediumMaze -p SearchAgent</pre>

<pre>python pacman.py -l bigMaze -z .5 -p SearchAgent</pre>

The Pacman board will show an overlay of the states explored, and the order in which they were explored (brighter red means earlier exploration). Is the exploration order what you would have expected? Does Pacman actually go to all the explored squares on his way to the goal?

**_Important notes:_** 

* Remember that a search node must contain not only a state but also the information necessary to reconstruct the path (plan) which gets to that state.

* All of your search functions need to return a list of _actions_ that will lead the agent from the start to the goal. These actions all have to be legal moves (valid directions, no moving through walls).

* Make sure to **use** the `Stack`, `Queue` and `PriorityQueue` data structures provided to you in `util.py`! These data structure implementations have particular properties which are required for compatibility with the autograder.

_Hints:_ 

* Algorithms for DFS, BFS, UCS, and A* are very similar and derive from the general search algorithm pseudocode above. They differ only in the details of how the fringe is managed. So, concentrate on getting DFS right and the rest should be relatively straightforward. Indeed, one possible implementation requires only a single generic search method which is configured with an algorithm-specific queuing strategy. (Your implementation need _not_ be of this form to receive full credit).

* If you use a `Stack` as your data structure, the solution found by your DFS algorithm for `mediumMaze` should have a length of 130 (provided you push successors onto the fringe in the order provided by getSuccessors; you might get 246 if you push them in the reverse order). Is this a least cost solution? If not, think about what depth-first search is doing that leads to it finding a suboptimal solution.

* * *

### <a name="Q2"></a>Question 2 (3 points): Breadth First Search
**Implement the breadth-first search (BFS) algorithm in the `breadthFirstSearch` function in `search.py`.** Again, write a graph search algorithm that avoids expanding any already visited states. Test your code the same way you did for depth-first search.

`python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs`
`python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5`

Does BFS find a least cost solution? If not, check your implementation.
**Hint:** If Pacman moves too slowly for you, try the option `--frameTime 0`.
**Note:** If you've written your search code generically, your code should work equally well for the eight-puzzle search problem without any changes.
`python eightpuzzle.py`

* * *

### <a name="Q3"></a>Question 3 (3 points): Varying the Cost Function

While BFS will find a fewest-actions path to the goal, we might want to find paths that are "best" in other senses. Consider `mediumDottedMaze` and `mediumScaryMaze`.

By changing the cost function, we can encourage Pacman to find different paths. For example, we can charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas, and a rational Pacman agent should adjust its behavior in response.

Implement the uniform-cost graph search algorithm in the `uniformCostSearch` function in `search.py`. We encourage you to look through `util.py` for some data structures that may be useful in your implementation. You should now observe successful behavior in all three of the following layouts, where the agents below are all UCS agents that differ only in the cost function they use (the agents and cost functions are written for you):

<pre>python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs</pre>

<pre>python pacman.py -l mediumDottedMaze -p StayEastSearchAgent</pre>

<pre>python pacman.py -l mediumScaryMaze -p StayWestSearchAgent</pre>

_Note:_ You should get very low and very high path costs for the `StayEastSearchAgent` and `StayWestSearchAgent` respectively, due to their exponential cost functions (see `searchAgents.py` for details).

* * *

### <a name="Q4"></a>Question 4 (3 points): A* search

Implement A* graph search in the empty function `aStarSearch` in `search.py`. A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The `nullHeuristic` heuristic function in `search.py` is a trivial example.

You can test your A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as `manhattanHeuristic` in `searchAgents.py`).

<pre>python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic</pre>

You should see that A* finds the optimal solution slightly faster than uniform cost search (about 549 vs. 620 search nodes expanded in our implementation, but ties in priority may make your numbers differ slightly). What happens on `openMaze` for the various search strategies?

* * *


### <a name="Q5"></a>Question 5 (3 points): Finding All the Corners

_Note: Make sure to complete Question 2 before working on Question 5, because Question 5 builds upon your answer for Question 2._

The real power of A* will only be apparent with a more challenging search problem. Now, it's time to formulate a new problem and design a heuristic for it. In this part, we will create the search space for our new problem.

In _corner mazes_, there are four dots, one in each corner. Our new search problem is to find the shortest path through the maze that touches all four corners (whether the maze actually has food there or not). Note that for some mazes like `tinyCorners`, the shortest path does not always go to the closest food first! _Hint_: the shortest path through `tinyCorners` takes 28 steps.

Implement the `CornersProblem` search problem in `searchAgents.py`. You will need to choose a state representation that encodes all the information necessary to detect whether all four corners have been reached. Now, your search agent should solve tinyCorners and mediumCorners. You can check by running:

<pre>python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem</pre>

<pre>python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem</pre>

To receive full credit, you need to define an abstract state representation that _does not_ encode irrelevant information (like the position of ghosts, where extra food is, etc.). In particular, do not use a Pacman `GameState` as a search state. Your code will be very, very slow if you do (and also wrong).

_Hint:_ The only parts of the game state you need to reference in your implementation are the starting Pacman position and the location of the four corners.

Our implementation of `breadthFirstSearch` expands just under 2000 search nodes on `mediumCorners`. However, heuristics (used with A* search) can reduce the amount of searching required. We will do this in the next section.

* * *

### <a name="Q6"></a>Question 6 (3 points): Corners Problem: Heuristic

_Note: Make sure to complete Question 4 before working on Question 6, because Question 6 builds upon your answer for Question 4._

Implement a non-trivial, consistent heuristic for the `CornersProblem` in `cornersHeuristic`.

`python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5`

_Note:_ `AStarCornersAgent` is a shortcut for

`-p SearchAgent -a fn=aStarSearch,prob=CornersProblem,heuristic=cornersHeuristic`.

_**Admissibility vs. Consistency:**_ Remember, heuristics are just functions that take search states and return numbers that estimate the cost to a nearest goal. More effective heuristics will return values closer to the actual goal costs. To be _admissible_, the heuristic values must be lower bounded by the actual shortest path cost to the nearest goal (and be strictly non-negative). To be _consistent_, it must additionally hold that if an action has cost _c_, then taking that action can only cause a drop in heuristic of at most _c_.

Remember that admissibility isn't enough to guarantee correctness in graph search -- you need the stronger condition of consistency. However, admissible heuristics are usually also consistent, especially if they are derived from problem relaxations. Therefore, it is usually easiest to start out by brainstorming admissible heuristics. Once you have an admissible heuristic that works well, you can check whether it is indeed consistent, too. The only way to guarantee consistency is with a proof. However, inconsistency can often be detected by verifying that for each node you expand, its successor nodes are equal or higher in in f-value. Moreover, if UCS and A* ever return paths of different lengths, your heuristic is inconsistent. This stuff is tricky!

_**Non-Trivial Heuristics:**_ The trivial heuristics are the ones that return zero everywhere (UCS) and the heuristic which computes the true completion cost. The former won't save you any time, while the latter will timeout the autograder. You want a heuristic which reduces total compute time, though for this assignment the autograder will only check node counts (aside from enforcing a reasonable time limit).

_**Grading:**_ Your heuristic must be a non-trivial non-negative consistent heuristic to receive any points. Make sure that your heuristic returns 0 at every goal state and never returns a negative value. The fewer nodes your heuristic expands, the more points you receive! We’ll be using the following scale:

| Number of nodes expanded | Grade |
| --- | --- |
| more than 2000 | 0/3 |
| at most 2000 | 1/3 |
| at most 1600 | 2/3 |
| at most 1200 | 3/3 |

_Remember:_ If your heuristic is inconsistent, you will receive _no_ credit, so be careful!

* * *
### <a name="Q7"></a>Question 7 (4 points): Eating All The Dots

Now we'll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we'll need a new search problem definition which formalizes the food-clearing problem: `FoodSearchProblem` in `searchAgents.py` (implemented for you). A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and Pacman. (Of course ghosts can ruin the execution of a solution! We'll get to that in the next project.) If you have written your general search methods correctly, `A*` with a null heuristic (equivalent to uniform-cost search) should quickly find an optimal solution to `testSearch` with no code change on your part (total cost of 7).

<pre>python pacman.py -l testSearch -p AStarFoodSearchAgent</pre>

_Note:_ `AStarFoodSearchAgent` is a shortcut for `-p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic`.

You should find that UCS starts to slow down even for the seemingly simple `tinySearch`. As a reference, our implementation takes 2.5 seconds to find a path of length 27 after expanding 5057 search nodes.

_Note: Make sure to complete Question 4 before working on Question 7, because Question 7 builds upon your answer for Question 4._

Fill in `foodHeuristic` in `searchAgents.py` with a <emph>consistent</emph> heuristic for the `FoodSearchProblem`. Try your agent on the `trickySearch` board:

<pre>python pacman.py -l trickySearch -p AStarFoodSearchAgent</pre>

Our UCS agent finds the optimal solution in about 13 seconds, exploring over 16,000 nodes.

Any non-trivial non-negative consistent heuristic will receive 1 point. Make sure that your heuristic returns 0 at every goal state and never returns a negative value. Depending on how few nodes your heuristic expands, you'll get additional points:

<table align="center" border="1" cellspacing="1" cellpadding="5">

<tbody>

<tr>

<th>Number of nodes expanded</th>

<th>Grade</th>

</tr>

<tr>

<td>more than 15000</td>

<td>1/4</td>

</tr>

<tr>

<td>at most 15000</td>

<td>2/4</td>

</tr>

<tr>

<td>at most 12000</td>

<td>3/4</td>

</tr>

<tr>

<td>at most 9000</td>

<td>4/4 (full credit; medium)</td>

</tr>

<tr>

<td>at most 7000</td>

<td>5/4 (optional extra credit; hard)</td>

</tr>

</tbody>

</table>

_Remember:_ If your heuristic is inconsistent, you will receive _no_ credit, so be careful! Can you solve `mediumSearch` in a short time? If so, we're either very, very impressed, or your heuristic is inconsistent.

* * *

### <a name="Q8"></a>Question 8 (3 points): Suboptimal Search

Sometimes, even with A* and a good heuristic, finding the optimal path through all the dots is hard. In these cases, we'd still like to find a reasonably good path, quickly. In this section, you'll write an agent that always greedily eats the closest dot. `ClosestDotSearchAgent` is implemented for you in `searchAgents.py`, but it's missing a key function that finds a path to the closest dot.

Implement the function `findPathToClosestDot` in `searchAgents.py`. Our agent solves this maze (suboptimally!) in under a second with a path cost of 350:

<pre>python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5 </pre>

_Hint:_ The quickest way to complete `findPathToClosestDot` is to fill in the `AnyFoodSearchProblem`, which is missing its goal test. Then, solve that problem with an appropriate search function. The solution should be very short!

Your `ClosestDotSearchAgent` won't always find the shortest possible path through the maze. Make sure you understand why and try to come up with a small example where repeatedly going to the closest dot does not result in finding the shortest path for eating all the dots.

* * *
### <a name="Glossary"></a>Object Glossary

Here's a glossary of the key objects in the code base related to search problems, for your reference:

`SearchProblem (search.py)`  
A SearchProblem is an abstract object that represents the state space, successor function, costs, and goal state of a problem. You will interact with any SearchProblem only through the methods defined at the top of `search.py`

`PositionSearchProblem (searchAgents.py)`  
A specific type of SearchProblem that you will be working with --- it corresponds to searching for a single pellet in a maze.

`CornersProblem (searchAgents.py)`  
A specific type of SearchProblem that you will define --- it corresponds to searching for a path through all four corners of a maze.

`FoodSearchProblem (searchAgents.py)`  
A specific type of SearchProblem that you will be working with --- it corresponds to searching for a way to eat all the pellets in a maze.

`Search Function`  
A search function is a function which takes an instance of SearchProblem as a parameter, runs some algorithm, and returns a sequence of actions that lead to a goal. Example of search functions are `depthFirstSearch` and `breadthFirstSearch`, which you have to write. You are provided `tinyMazeSearch` which is a very bad search function that only works correctly on `tinyMaze.`

`SearchAgent`  
`SearchAgent` is a class which implements an Agent (an object that interacts with the world) and does its planning through a search function. The `SearchAgent` first uses the search function provided to make a plan of actions to take to reach the goal state, and then executes the actions one at a time.

### <a name="Submission"></a> Submission

You're not done yet! 

Having completed Questions 1 through 8 as specified in the project instructions, you must now upload `search.py` and `searchAgents.py`. 

Prior to submitting, be sure you run the autograder on your own machine. Running the autograder locally will help you to debug and expediate your development process. The autograder can be invoked on your own machine using the command:

<pre>python autograder.py</pre>

Note that running the autograder locally will **not** register your grades with us.

Note that you should select and upload akk files simultaneously. On Windows and Linux, this can be accomplished by holding down Ctrl and clicking. On OS X, hold down Cmd instead.


To submit your P1 code, please the Gradescope submission site (the URL for your courses Gradescope site is available in Piazza under Resources).  There you will submit both `search.py` and `searchAgents.py` to the Project 1 assignment.  You and your partner may submit as a group.  Once you've submitted your code, you should be able to verify that it was uploaded properly by logging back into Gradescope and visiting the Project 1 submission.

