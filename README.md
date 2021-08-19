# Agreement Game Design

The goal of both game 1 and game 2 is to make as much money as possible.
In a single round:
1. Display both information partitions.
2. At each turn based on existing reports 
    * Tell agents 
      * What their posterior is/which worlds are still plausible
      * What the expected payoff of their previous reports are
      * What they expect to make on a new report
    * If game 1
      * Give them options to report or to leave the game.
    * If game 2
      * Give them options to renege, report, or to leave the game    
3. The game ends if
    * One of the two players chooses to leave at any point
    * Agreement is reached
