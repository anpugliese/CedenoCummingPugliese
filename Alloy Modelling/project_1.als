abstract sig StoreState{}
one sig NotFull extends StoreState{}
one sig Full extends StoreState{}

abstract sig CustomerState{}
one sig Waiting extends CustomerState{}
one sig Shopping extends CustomerState{}

abstract sig Request{}
one sig LineUp extends Request{}
one sig Book extends Request{}
one sig ScanQR extends Request{}

abstract sig Response{}
one sig OpenDoor extends Response{}
one sig WaitingTime extends Response{}
one sig KeepDoorClosed extends Response{}

sig Customer{//MAPS Request to Store
request: Request -> Store,
customer_state: one CustomerState
}{
#request >0
}

sig Store {//MAPS Response to Customer
response: Response -> Customer,
store_state: one StoreState
}

//Retrieves all the Stores requested from a customer
fun getCStore[c :Customer]: set Store {
Request.(c.request)
}
//Retrieves all the Customers responded from a store
fun getSCustomer[s : Store]: set Customer {
Response.(s.response)
}
//Retrieve the Store associated to one Request
fun getRStore[r :Request]: set Store {
r.(Customer.request)
}
//Retrieve the Customer associated to one Response
fun getRCustomer[r :Response]: set Customer {
r.(Store.response)
}
//Retrieves all the Requests made by a Customer
fun getRequest[c :Customer]: set Request {
(c.request).Store
}

//Retrieves all the Responses made by a Store
fun getResponse[s :Store]: set Response {
(s.response).Customer
}


fact facts{
// All Requests have a Response
(all req: Request, res: Response |
let s = getRStore[req], c = getRCustomer[res]|(req=getRequest[c] and  c=getSCustomer[s]) iff (res = getResponse[s] and s=getCStore[c])
)
and
(#request=#response)
}

pred show{
#Customer > 4
#Store>2
}

run show for 10
