//Customers have a number on a certain queue
// and perform an action (entering or waiting)
sig Customer{ 
location: Store -> Position,
shopTime: Time,
request: Type -> Queue,
shopSections: Time -> Section
}
sig Store{
storeSections: State -> Section
}
abstract sig Position{}
one sig CLOSE extends Position{}
one sig FAR extends Position{}

abstract sig Time{}
one sig SOON extends Time{}
one sig LATER extends Time{}

abstract sig State{}
one sig FULL extends State{}
one sig NOT_FULL extends State{}

abstract sig Type{}
one sig LINEUP extends Type{}
one sig BOOK extends Type{}

sig Section{}

sig Suggestion{
response: Customer 
}
sig Queue{
queueSection: Section,
queueStore: Store
}

// SM4. The system will be able to provide one ticket 
// at a time to each user.
fact SM4_UniqueTicket{
//Customer has only 1 queue
(all c : Customer |
(let q = (c.request).Queue| #q=1)
)
}


//M2. The system will receive the position and section preferences of the customers with respect to the different
// stores as well as the number of people inside them. Based on this information, it will always find a hierarchy
// regarding the convenience of going to the different stores.
fact M2_Suggestion{
(all s : Suggestion |
(let c = s.response| #c=1)
)
and
(all c : Customer |
(let s = response.c| #s=1)
)
}
// Stores have only one position
fact UniqueStorePosition{
(all p: Position, c : Customer | 
(let s = c.(location.p) | #s=1)
)

}



pred show{
}
run show for 10
