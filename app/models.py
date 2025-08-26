from pydantic import BaseModel
from typing import List, Literal

class Passenger(BaseModel):
    id: int
    name: str
    hasConnections: bool
    age: int
    flightCategory: Literal["Black", "Platinum", "Gold", "Normal"]
    reservationId: str
    hasCheckedBaggage: bool

class Flight(BaseModel):
    flightCode: str
    passengers: List[Passenger]

class FlightResponse(Flight):
    id: str = None