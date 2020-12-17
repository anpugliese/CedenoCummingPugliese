// Assumption D3: Customers have intention of going to shop at
// a certain time. They also have a certain position wrt Stores
// Customers can also have a number on a certain queue
// and perform an action (entering or waiting)
sig Customer{ 
location: Store -> Position,
shopTime: Time,
request: Type -> Queue,
shopSections: Time -> Section
}
// Stores have Sections, which have a certain State
// Assumption D2: Store's Sections can be full or not full
sig Store{
storeSections: State -> Section
}
// Position of Customers wrt Stores
abstract sig Position{}
one sig CLOSE extends Position{}
one sig FAR extends Position{}
// Time in which Customers want to shop
abstract sig Time{}
one sig SOON extends Time{}
one sig LATER extends Time{}
// Sections' State
abstract sig State{}
one sig FULL extends State{}
one sig NOT_FULL extends State{}
// Customers' Requests Type
abstract sig Type{}
one sig LINEUP extends Type{}
one sig BOOK extends Type{}
// Stores' Sections
sig Section{}
// Suggestion of a Store to a Customer
sig Suggestion{
response: Store -> Customer 
}
// Queue to a set of Store's Sections
sig Queue{
queueSection: Store -> Section
}
// FACT Stores have only one position
fact FACT_UniqueStorePosition{
(all p: Position, c : Customer | 
(let s = c.(location.p) | #s=1)
)
}
// FACT Customers are close or far from a certain Store
fact FACT_CloseOrFar{
(all  c : Customer, s : Store | 
(let d = s.(c.location) | #d=1)
)
}
// Assumption D2: Each section can be full or not full
fact D2_SectionState{
(all s : Section, st : Store |
(#st.(storeSections.s)=1)
)
}
// Assumption D3: Customers want to buy soon or later, not both
fact D3_SoonOrLater{
(all  c : Customer | 
(let t = (c.shopSections).Section |#t=1)
)
}
// Assumption D3: customers will shop at the time they want
fact D3_CustomersWill{
(all c : Customer |
((c.shopSections).Section=c.shopTime)
)
}
// Assumption D4: Stores have at least 1 section 
// and sections are associated to at least 1 store
fact D4_SectionStore{
(all  s : Store | 
(let secs = State.(s.storeSections) | #secs>0)
)
and
(all s : Section |
(let stor = storeSections.s.State | #stor>0)
)
}
//Assumptions D5 and D6: if the customers want to buy soon, they line-up
// if the customers want to buy later, they book
fact D5D6_RequestDecission{
(all  c : Customer | 
( c.shopTime=LATER implies (c.request).Queue=BOOK)
and
(c.shopTime=SOON implies (c.request).Queue=LINEUP)
)
}
//Assumption D7: the sections that the customers want to buy in
// are the ones that they request for
fact D7_CustomerWill{
(all  c : Customer | 
(Time.(c.shopSections) = Store.(Type.(c.request).queueSection))
)
}
// Requirement M6: Queues are associated to only 1 customer
fact M6_QueueCustomer{
(all  q : Queue | 
(let c = request.q.Type | #c=1)
)
}
// Requirement M6: The system will be able to provide one ticket 
// at a time to each user.
fact M6_UniqueTicket{
// Customer has only 1 queue
(all c : Customer |
(let q = (c.request).Queue| #q>0 implies #q=1)
)
}
// Requirement M6: Customer can only perform 1 type of request at a time
fact M6_UniqueQueue{
(all  c : Customer | 
(let q = Type.(c.request) |#q>0 implies #q=1)
)
}
// Requirement M6: Request are associated to a single store
fact M6_UniqueStore{
(all  q : Queue | 
(let s=(q.queueSection).Section | #s=1)
)
}
// Requirement M2: if Customers make a request, they must receive a suggestion
fact M2_RequestSuggestion{
(all  c : Customer | 
(#c.request>0 implies #response.c>0)
)
}
// Requirement M2: Suggestions must contain stores with sections in which
//the customer wants to buy in and these sections must be not full
fact M2_SectionSuggestion{
(all  s : Suggestion | 
(s.response.Customer in storeSections.(Time.(Store.(s.response).shopSections)).NOT_FULL)
and
(#s.response.Customer.storeSections.(Time.(Store.(s.response).shopSections))=1)
)
}
// Requirement M3: If the customer wants to shop as soon as possible, the store suggestion
// must be close to him/her
fact M3_RequestSuggestion{
(all c: Customer | 
(c.shopTime=SOON implies Suggestion.(response.c).(c.location)=CLOSE)
)
}
//Requirement M2: for each customer there is one best suggestion
fact M2_Suggestion{
(all s : Suggestion |
(let c = s.response|#c=1)
)
and
(all c : Customer |
(let s = response.c|#s>0 implies #s=1)
)
}
// the model is presented with representative cases
// The following predicate is a simple instance to illustrate Lining-up/Booking UCs 4, 5 & 6
pred UC4UC5UC6_LineUp{
// Only 2 sections, 1 customer, 1 request
#Section=2
#Customer=1
#(Customer.request).Queue=1
#Store.(storeSections.Section)=2 //there are FULL and NOT_FULL sections
(all s : Store | //stores contain all sections 
(let s=s.storeSections | #s=#Section)
)
(some c : Customer |// the customer wants to buy in more than 1 section
(let s=Time.(c.shopSections) | #s>1)
)
}
//G2. The customers must be able to line-up in a store if they want to enter to shop as soon as possible.
//G3. The customers must be able to book a number in order to make a reservation to enter a specific 
//store at a certain date and time.
assert G2G3_Requests{
(all c: Customer | #(c.request).Queue>0)
and
(all c: Customer | c.shopTime=SOON implies (c.request).Queue=LINEUP)
and
(all c: Customer | c.shopTime=LATER implies (c.request).Queue=BOOK)
}
//G4. If customers want to shop as soon as possible, they must receive suggestions on the most convenient
// options in terms of distance and waiting time.
// G5. If customers want to book a number on a specific store, they must receive suggestions on the most
// convenient options in terms of availability.
assert G4G5_Suggestions{
(all c: Customer | 
(c.shopTime=SOON implies Suggestion.(response.c).(c.location)=CLOSE and Suggestion.(response.c).storeSections.(Time.(c.shopSections))=NOT_FULL)
)
and
(all c: Customer | 
(c.shopTime=LATER implies Suggestion.(response.c).storeSections.(Time.(c.shopSections))=NOT_FULL)
)
}
// run demo instances
run UC4UC5UC6_LineUp for 10
// check goals
check G2G3_Requests
check G4G5_Suggestions
