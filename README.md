# Artificial_Intelligence_Final_Project
Chess board solver: finds board configurations such that no pieces can attack each other

https://github.com/EthanWebster454/Artificial_Intelligence_Final_Project

Group 11

Coding Authors: Ethan Webster, Steven Kassof


Contained Files:
_pycache_ (folder): Required for backend
images (folder): Contains the images necessary to show the gui
results (folder): Contains pictures of sample results from earlier runs
backend.py: Contains the min-conflict heuristic and other required computations
gui.py: Builds the gui and directs the min-conflict heuristic
guiLayout.ui: Required for gui



RUNNING:
To run the program, use a python compiler to run the gui.py file.

The text boxes on the side indicate the number of chess pieces to try and find a minimal solution that accomodates the inputted pieces.  Console output will show which board dimension the program is currently checking.  There are several different modes available:

If the number of iterations is set to ZERO: Runs the Heuristic Search to find the minimal board size.  At the end of the run a popup window will display how many iterations of the min-conflict heuristic were run along with how many rows/columns the heuristic was off by (compared to the optimal guess).  The board will update to display the configuration of pieces found.

If the number of iterations is higher than ZERO, and the board size is set to ZERO:  Runs the brute force search to find the minimal board size.  It will run the min-conflict heuristic a certain number of times according to the number of iterations that were set.  If the min-conflict heuristic does not find a solution it will increase the board's dimensions until it finds a solution.  Note: If the number of iterations is set too low it might incorrectly register a boardsize as unsolvable (We recommend 1000).  Also for a large set of inputs this will take a long time to complete.  At the end a popup window will display how many iterations of the min-conflict heuristic were run.  The board will update to show the configuration of the pieces.

The number of iterations is higher than ZERO and the board size is higher than ZERO:  Runs the min-conflict heuristic a certain number of times according to the inputted number of iterations attempting to find a configuration of pieces on the inputted board size.  If it finds a solution a popup window will display a success message and the board will show the found solution.  If it hasn't found a solution after the inputted number of iterations it will display a popup window alerting you of its failure.

NOTE: The text boxes do not accomodate blank inputs; a ZERO is required.
