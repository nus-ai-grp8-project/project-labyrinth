(define (problem labyrinth-size-7-rotations-4-seed-51)
(:domain labyrinth)
(:objects
	pos0 pos1 pos2 pos3 pos4 pos5 pos6  - gridpos
	card0 card1 card2 card3 card4 card5 card6 card7 card8 card9 card10 card11 card12 card13 card14 card15 card16 card17 card18 card19 card20 card21 card22 card23 card24 card25 card26 card27 card28 card29 card30 card31 card32 card33 card34 card35 card36 card37 card38 card39 card40 card41 card42 card43 card44 card45 card46 card47 card48  - card
)
(:init
	(MAX-POS pos6)
	(MIN-POS pos0)

	(NEXT pos1 pos0)
	(NEXT pos2 pos1)
	(NEXT pos3 pos2)
	(NEXT pos4 pos3)
	(NEXT pos5 pos4)
	(NEXT pos6 pos5)

	(card-at card0 pos0 pos0)
	(card-at card1 pos1 pos0)
	(card-at card2 pos2 pos0)
	(card-at card3 pos3 pos0)
	(card-at card4 pos4 pos0)
	(card-at card12 pos5 pos0)
	(card-at card6 pos6 pos0)
	(card-at card7 pos0 pos1)
	(card-at card8 pos1 pos1)
	(card-at card9 pos2 pos1)
	(card-at card10 pos3 pos1)
	(card-at card11 pos4 pos1)
	(card-at card20 pos5 pos1)
	(card-at card13 pos6 pos1)
	(card-at card15 pos0 pos2)
	(card-at card16 pos1 pos2)
	(card-at card17 pos2 pos2)
	(card-at card18 pos3 pos2)
	(card-at card19 pos4 pos2)
	(card-at card26 pos5 pos2)
	(card-at card14 pos6 pos2)
	(card-at card21 pos0 pos3)
	(card-at card22 pos1 pos3)
	(card-at card23 pos2 pos3)
	(card-at card24 pos3 pos3)
	(card-at card25 pos4 pos3)
	(card-at card31 pos5 pos3)
	(card-at card27 pos6 pos3)
	(card-at card33 pos0 pos4)
	(card-at card34 pos1 pos4)
	(card-at card28 pos2 pos4)
	(card-at card29 pos3 pos4)
	(card-at card30 pos4 pos4)
	(card-at card40 pos5 pos4)
	(card-at card32 pos6 pos4)
	(card-at card35 pos0 pos5)
	(card-at card36 pos1 pos5)
	(card-at card37 pos2 pos5)
	(card-at card38 pos3 pos5)
	(card-at card39 pos4 pos5)
	(card-at card47 pos5 pos5)
	(card-at card41 pos6 pos5)
	(card-at card42 pos0 pos6)
	(card-at card43 pos1 pos6)
	(card-at card44 pos2 pos6)
	(card-at card45 pos3 pos6)
	(card-at card46 pos4 pos6)
	(card-at card5 pos5 pos6)
	(card-at card48 pos6 pos6)

	(BLOCKED card0 N)
	(BLOCKED card0 S)


	(BLOCKED card2 E)
	(BLOCKED card2 S)


	(BLOCKED card4 N)
	(BLOCKED card4 W)

	(BLOCKED card12 N)
	(BLOCKED card12 W)

	(BLOCKED card6 E)
	(BLOCKED card6 W)

	(BLOCKED card7 S)
	(BLOCKED card7 W)

	(BLOCKED card8 W)

	(BLOCKED card9 N)
	(BLOCKED card9 E)

	(BLOCKED card10 N)
	(BLOCKED card10 S)

	(BLOCKED card11 E)
	(BLOCKED card11 S)

	(BLOCKED card20 S)
	(BLOCKED card20 W)

	(BLOCKED card13 E)
	(BLOCKED card13 W)

	(BLOCKED card15 N)
	(BLOCKED card15 S)

	(BLOCKED card16 S)
	(BLOCKED card16 W)

	(BLOCKED card17 N)
	(BLOCKED card17 E)

	(BLOCKED card18 N)
	(BLOCKED card18 E)

	(BLOCKED card19 E)
	(BLOCKED card19 W)

	(BLOCKED card26 E)
	(BLOCKED card26 W)

	(BLOCKED card14 N)
	(BLOCKED card14 E)

	(BLOCKED card21 N)
	(BLOCKED card21 W)

	(BLOCKED card22 S)

	(BLOCKED card23 N)
	(BLOCKED card23 E)

	(BLOCKED card24 W)

	(BLOCKED card25 S)
	(BLOCKED card25 W)

	(BLOCKED card31 S)
	(BLOCKED card31 W)

	(BLOCKED card27 N)
	(BLOCKED card27 W)

	(BLOCKED card33 E)
	(BLOCKED card33 S)

	(BLOCKED card34 E)
	(BLOCKED card34 W)

	(BLOCKED card28 N)

	(BLOCKED card29 N)
	(BLOCKED card29 W)

	(BLOCKED card30 N)
	(BLOCKED card30 W)

	(BLOCKED card40 S)
	(BLOCKED card40 W)

	(BLOCKED card32 N)
	(BLOCKED card32 E)

	(BLOCKED card35 N)
	(BLOCKED card35 S)

	(BLOCKED card36 S)

	(BLOCKED card37 S)

	(BLOCKED card38 N)
	(BLOCKED card38 S)


	(BLOCKED card47 N)
	(BLOCKED card47 S)

	(BLOCKED card41 W)

	(BLOCKED card42 S)
	(BLOCKED card42 W)

	(BLOCKED card43 E)
	(BLOCKED card43 S)

	(BLOCKED card44 N)
	(BLOCKED card44 E)

	(BLOCKED card45 N)
	(BLOCKED card45 E)

	(BLOCKED card46 W)

	(BLOCKED card5 E)
	(BLOCKED card5 W)

	(BLOCKED card48 E)


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
