# Grids Probs

Here are grids in the format *grid1*. We originally thought that we could allow other formats as input, but we finally didn't. 

The grid `example.grid` is the grid from the report, the grid `grid1.grid` is the first grid ever created in the project, and the grid `bigGrid.grid` is a grid used for testing over a grid who's values can have multiple digits.  
The other grids were made by hand and have their solutions (made by hand) in [`../Solutions`](https://github.com/NeoGalaxy/INF432/tree/master/Grids/Solutions).

The format grid1 have been created in order to have a visual representation of the grid. Here is a valid example :
```
grid1
# A comment line
   __ _ ___ _ __ _   # Line covering each column
2 |__|  ___ _ __| |  # A 'normal' line, describing the walls on the tiles of this line and the horizontal val.
 3|   _|___     |_|  # same here...
 4|__|_    | |__ _|  # And so on...
2 |    |___|_|   _|
# A random line that will be ignored
 5|  |  ___   __|_|
  |__|_|___|_|__ _|  # Oh and by the way we don't have to specify a horizontal value
   5      2 4  3 4   # vertical values

# Note that each column can be of any width, but can't change from a line to another, and can't be of width 0.
# The space on the left for the horizontal values can be of any width, but also needs to be of consistent width.
```
THe rules of the grid1 format are the following :  
1. The first line should be `grid1`, and can't have any comment.
2. The second line should be composed of only spaces and underscores `_`. The underscores are here to cover each column of the grid, and should not be over a place where there could be a vertical wall. It allows to the parser to know the width of each column. 
3. On the following lines, there first are the horizontal values (indicating how much tiles of water should be on this line), followed by a combination of spaces, underscores `_` and vertical bars `|`. Underscores on a tile means that there is as wall underneath this tile, and a vertical bar next to a tile means that there is a wall on this side of the tile.  
The width of the tile should be the same as the width of the underscores on the top of the column.
4. The last line should contain the vertical value of each column. 

Every of the lines except the first line can contain a comment (starting by a hash-tag `#`, ending at the end of the line), and empty lines are skipped (except for the first line).
