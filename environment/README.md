# LABYRINTH ENVIRONMENT

This contains the code for a general labyrinth game relevant to CS4246

## Notations  
- 0 -> Blocked
- 1 -> Clear Path
- 2 -> Robot
- 5 -> Goal Position

## Terminologies  
- Card index  
    In a say 7 x 7 matrix, the standard way of laying out the card is 
    > 0 1 2 3 4 5 6
    > 7 8 9 10 11 12
    > ....
    These are basically your card indices.


## Some useful functions  
- move  
    - Inputs : axis (Axis type), direction (Direction Type), card_row_or_col (index of the card - not the board)  
- shift  
    - Inputs : src_card_number (index of the card), dest_card_number (index of the card)  
    - Note : Does not check if the move is valid or not  
- print_board_prettier  
    - improves mental health and also your eye health when eyeballing game states  

## LMK if u need more - WE SHOULD use the same environment just in case we are pitting algorithms tgt in a game