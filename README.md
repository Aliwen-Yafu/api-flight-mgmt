# api-flight-mgmt
Un entorno de desarrollo usando Docker Compose

# Flight Management API

A REST API for managing flight information and passengers, built with FastAPI and MongoDB.

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Running the Application

1. Clone this repository:
```bash
git clone <your-repo-url>
cd api-flight-mgmt
```

2. Start the application:
```bash
docker-compose up --build
```

3. The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠 API Endpoints

### Health Check
- `GET /` - API status
- `GET /health` - Health check

### Flights CRUD
- `POST /flights` - Create a new flight
- `GET /flights` - Get all flights
- `GET /flights/{flight_id}` - Get a specific flight
- `PUT /flights/{flight_id}` - Update a flight
- `DELETE /flights/{flight_id}` - Delete a flight

## 📋 Data Structure

### Flight Object
```json
{
  "flightCode": "string",
  "passengers": [
    {
      "id": "number",
      "name": "string",
      "hasConnections": "boolean",
      "age": "number",
      "flightCategory": "Black | Platinum | Gold | Normal",
      "reservationId": "string",
      "hasCheckedBaggage": "boolean"
    }
  ]
}
```

## 🧪 Testing the API

### Create a Flight
```bash
curl -X POST "http://localhost:8000/flights" \
-H "Content-Type: application/json" \
-d '{
  "flightCode": "AA123",
  "passengers": [
    {
      "id": 1,
      "name": "John Doe",
      "hasConnections": true,
      "age": 35,
      "flightCategory": "Gold",
      "reservationId": "RES001",
      "hasCheckedBaggage": true
    }
  ]
}'
```

### Get All Flights
```bash
curl http://localhost:8000/flights
```

### Get Specific Flight
```bash
curl http://localhost:8000/flights/{flight_id}
```

### Update a Flight
```bash
curl -X PUT "http://localhost:8000/flights/{flight_id}" \
-H "Content-Type: application/json" \
-d '{
  "flightCode": "BB456",
  "passengers": [...]
}'
```

### Delete a Flight
```bash
curl -X DELETE "http://localhost:8000/flights/{flight_id}"
```

## 🏗 Architecture

### Technology Stack
- **API Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Containerization**: Docker & Docker Compose
- **Documentation**: Auto-generated with FastAPI

### Project Structure
```
api-flight-mgmt/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   └── database.py      # MongoDB connection
├── docker-compose.yml   # Multi-container configuration
├── Dockerfile          # API container configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🐳 Docker Services

### API Service
- **Port**: 8000
- **Framework**: FastAPI with Uvicorn
- **Environment**: Python 3.11

### Database Service
- **Type**: MongoDB 7.0
- **Port**: 27017
- **Database**: flight_management
- **Collection**: flights

## 🔧 Development

### Local Development (without Docker)
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MongoDB locally or update connection string in `database.py`

3. Run the application:
```bash
cd app
uvicorn main:app --reload
```

## 📝 Notes

- The API automatically validates request data using Pydantic models
- MongoDB ObjectId is automatically converted to string in responses
- All endpoints include proper error handling and HTTP status codes
- The application uses environment variables for configuration flexibility