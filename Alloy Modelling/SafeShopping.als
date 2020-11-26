//Customers have a number on a certain queue
// and perform an action (entering or waiting)
sig Customer{ 
queue: Queue -> Section,
action: Action
}
abstract sig Action{}
one sig ENTER extends Action{}
one sig WAIT extends Action{}
// Store's sections can be full or not full
sig Section {
state: State
}
abstract sig State{}
one sig FULL extends State{}
one sig NOT_FULL extends State{}
// A Certain queue can provide a turn or not yet
sig Queue{
position: one Position
}
abstract sig Position{}
one sig IS_TURN extends Position{}
one sig IS_NOT_TURN extends Position{}
//SM1. The system will control the amount of people 
// inside the store by means of a queuing system, 
// which will provide permission to enter if and only if 
// all the sections selected by the user have capacity.
fact SM1_GiveTurn{
(all c : Customer | (c.queue.Section).position = IS_TURN iff (Queue.(c.queue)).state = NOT_FULL
)
}
// SM2. The queuing system will not allow customers 
// to enter if it is not their turn.
fact SM2_TurnControl{
(no c : Customer |
 c.action=ENTER and (c.queue.Section).position=IS_NOT_TURN
)
}
// SM4. The system will be able to provide one ticket 
// at a time to each user.
fact SM4_UniqueTicket{
//Customer has only 1 queue
(all c : Customer |
(let q = (c.queue).Section | #q=1)
)
and
//Queue has only 1 Customer
(all q : Queue |
(let c = queue.Section.q | #c=1)
)
}
//G1. The in-person grocery shopping must be carried out 
// guaranteeing the safety of customers and employees. 
//This means that users cannot enter a full section.
assert G1_SafeShopping{
no c: Customer | (Queue.(c.queue)).state=FULL and c.action=ENTER
}
pred show{
#Section=4
#Customer=4
}
run show for 10
// goal is check
check G1_SafeShopping
