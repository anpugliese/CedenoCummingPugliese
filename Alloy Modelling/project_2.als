abstract sig StoreState{}
one sig NotFull extends StoreState{}
one sig Full extends StoreState{}

abstract sig CustomerState{}
one sig Waiting extends CustomerState{}
one sig Shopping extends CustomerState{}

//abstract sig Request{}
//one sig LineUp extends Request{}
//one sig Book extends Request{}
//one sig ScanQR extends Request{}

//abstract sig Response{}
//one sig OpenDoor extends Response{}
//one sig WaitingTime extends Response{}
//one sig KeepDoorClosed extends Response{}

sig Customer{
lineUp: Store,
book: Store,
scanQR: Store,
customer_state: one CustomerState
}

sig Store {
openDoor:  Customer,
waitTime:  Customer,
keepDoorClosed:  Customer,
store_state: one StoreState
}

fact facts{
// All Line-up requests have a Response
(all c: Customer, s: Store | c.lineUp =s or c.book=s or c.scanQR=s iff s.openDoor = c or s.waitTime = c or s.keepDoorClosed = c
)
}

pred show{
//#Customer > 5
//#Store>5
}

run show for 10
