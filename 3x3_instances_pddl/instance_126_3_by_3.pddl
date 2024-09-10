(define (problem labyrinth-size-3-rotations-1-seed-126)
(:domain labyrinth)
(:objects
	pos0 pos1 pos2  - gridpos
	card0 card1 card2 card3 card4 card5 card6 card7 card8  - card
)
(:init
	(MAX-POS pos2)
	(MIN-POS pos0)

	(NEXT pos1 pos0)
	(NEXT pos2 pos1)

	(card-at card0 pos0 pos0)
	(card-at card4 pos1 pos0)
	(card-at card2 pos2 pos0)
	(card-at card3 pos0 pos1)
	(card-at card7 pos1 pos1)
	(card-at card5 pos2 pos1)
	(card-at card6 pos0 pos2)
	(card-at card1 pos1 pos2)
	(card-at card8 pos2 pos2)

	(BLOCKED card0 N)
	(BLOCKED card0 S)


	(BLOCKED card2 N)
	(BLOCKED card2 W)

	(BLOCKED card3 S)
	(BLOCKED card3 W)

	(BLOCKED card7 N)
	(BLOCKED card7 E)

	(BLOCKED card5 E)

	(BLOCKED card6 E)
	(BLOCKED card6 W)

	(BLOCKED card1 E)

	(BLOCKED card8 E)
	(BLOCKED card8 W)


	(robot-at card0)

	(= (total-cost) 0)
	(= (move-robot-cost) 1)
	(= (move-card) 1)
)
(:goal
	(and
		(left)
	)
)
	(:metric minimize (total-cost))
)
