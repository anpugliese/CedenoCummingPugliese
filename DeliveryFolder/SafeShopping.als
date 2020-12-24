//Customers have a number on a certain queue
// and perform an action (entering or waiting)
sig Customer{ 
queue: Queue -> Section,
action: Action
}
// Assumption D3: Customers that want to buy groceries, 
// will line-up in order to wait for their turn to enter the store.
abstract sig Action{}
one sig ENTER extends Action{}
one sig WAIT extends Action{}
// Assumption D2: Store's sections can be full or not full
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
//Requirement M1: The system will control the amount of people 
// inside the store by means of a queuing system, 
// which will provide permission to enter if and only if 
// all the sections selected by the user have capacity.
fact M1_GiveTurn{
(all c : Customer | (c.queue.Section).position = IS_TURN iff (Queue.(c.queue)).state = NOT_FULL
)
}
// Requirement M1: The queuing system will not allow customers 
// to enter if it is not their turn.
fact M1_TurnControl{
(no c : Customer |
 c.action=ENTER and (c.queue.Section).position=IS_NOT_TURN
)
}
// Requirement M6: The system will be able to provide one ticket 
// at a time to each user.
fact M6_UniqueTicket{
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
//D1. The in-person shopping will be safe as long as 
// customers do not enter a full section.
assert G1D1_SafeShopping{
no c: Customer | (Queue.(c.queue)).state=FULL and c.action=ENTER
}
// the model is presented with a representative instance
pred show{
#Section=4
#Customer=3
some c : Customer | #Queue.(c.queue)=#Section
some c : Customer | #Queue.(c.queue)<#Section and c.action=ENTER
some c : Customer | #Queue.(c.queue)<#Section and c.action=WAIT
}
run show for 10
// goal is checked
check G1D1_SafeShopping
