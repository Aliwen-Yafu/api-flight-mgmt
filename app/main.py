from fastapi import FastAPI, HTTPException
from typing import List
from models import Flight, FlightResponse, Passenger
from database import get_flights_collection
from bson import ObjectId
import json

app = FastAPI(title="Flight Management API", version="1.0.1")

def convert_objectid(obj):
    """Convierte ObjectId a string para JSON serialization"""
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError

@app.get("/")
def read_root():
    return {"message": "Flight Management API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/flights", response_model=dict)
def create_flight(flight: Flight):
    """Crear un nuevo vuelo"""
    try:
        collection = get_flights_collection()
        flight_dict = flight.dict()
        result = collection.insert_one(flight_dict)
        
        # Obtener el vuelo creado
        created_flight = collection.find_one({"_id": result.inserted_id})
        created_flight["id"] = str(created_flight["_id"])
        del created_flight["_id"]
        
        return created_flight
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/flights", response_model=List[dict])
def get_all_flights():
    """Obtener todos los vuelos"""
    try:
        collection = get_flights_collection()
        flights = []
        for flight in collection.find():
            flight["id"] = str(flight["_id"])
            del flight["_id"]
            flights.append(flight)
        return flights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/flights/{flight_id}", response_model=dict)
def get_flight(flight_id: str):
    """Obtener un vuelo específico"""
    try:
        collection = get_flights_collection()
        flight = collection.find_one({"_id": ObjectId(flight_id)})
        if flight is None:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        flight["id"] = str(flight["_id"])
        del flight["_id"]
        return flight
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/flights/{flight_id}", response_model=dict)
def update_flight(flight_id: str, flight: Flight):
    """Actualizar un vuelo"""
    try:
        collection = get_flights_collection()
        flight_dict = flight.dict()
        
        result = collection.update_one(
            {"_id": ObjectId(flight_id)}, 
            {"$set": flight_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        # Obtener el vuelo actualizado
        updated_flight = collection.find_one({"_id": ObjectId(flight_id)})
        updated_flight["id"] = str(updated_flight["_id"])
        del updated_flight["_id"]
        
        return updated_flight
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/flights/{flight_id}")
def delete_flight(flight_id: str):
    """Eliminar un vuelo"""
    try:
        collection = get_flights_collection()
        result = collection.delete_one({"_id": ObjectId(flight_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        return {"message": "Flight deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/flights/{flight_id}/stats")
def get_flight_stats(flight_id: str):
    """Obtener estadísticas de un vuelo"""
    try:
        collection = get_flights_collection()
        flight = collection.find_one({"_id": ObjectId(flight_id)})

        if flight is None:
            raise HTTPException(status_code=404, detail="Flight not found")

        passengers = flight["passengers"]
        total_passengers = len(passengers)

        # Estadísticas básica etaria
        ages = [p["age"] for p in passengers]
        avg_age = sum(ages) / len(ages) if ages else 0

        # Distribución por categoría
        category_stats = {}
        for category in ["Black", "Platinum", "Gold", "Normal"]:
            count = len([p for p in passengers if p["flightCategory"] == category])
            category_stats[category] = count

        return {
            "flightCode": flight["flightCode"],
            "totalPassengers": total_passengers,
            "ageStats": {
                "average": round(avg_age, 1),
            },
            "categoryDistribution": category_stats            
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))