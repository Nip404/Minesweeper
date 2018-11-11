# Minesweeper
A clone of the popular game Minesweeper by Atari in Python 3.7.x using the Pygame library.

# Gameplay mechanics
- The board is generated after the first tile is clicked. Mines are not allowed within 1 tile of the starting tile.
- A recursive method is used to detect neighbours when the tile pressed has 0 mines nearby:
  1) Reveal the current tile
  2) Loop through all neighbours
  3) If the current neighbour also has 0 neighbours, goto that neighbour and start from i.
  4) Otherwise, reveal that neighbour and continue.
