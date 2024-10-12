# FastAPI CRUD Application

This is a FastAPI-based application performing CRUD (Create, Read, Update, Delete) operations on two entities: **Items** and **User Clock-In Records**. The application is built with FastAPI, uses MongoDB as the database, and implements robust input validation using Pydantic models.

## Setup Instructions

### Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.8+**
- **MongoDB** (either locally installed or use MongoDB Atlas)
- **Pip** (Python package manager)
- **Git** (for cloning the repository)

### Steps to Set Up and Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chantya127/python_project.git
   cd python_project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**:
   If using MongoDB Atlas, add the connection string to a .env file:
   ```
   MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/mydatabase?retryWrites=true&w=majority
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API documentation**: Open your browser and navigate to http://127.0.0.1:8000/docs to view and test the APIs using the Swagger UI.

## API Endpoints

### Items Endpoints

#### POST /items - Create a new item.

Request body:
```json
{
  "email": "string",
  "item_name": "string",
  "quantity": 10,
  "expiry_date": "YYYY-MM-DD"
}
```

Response body:
```json
{
  "id": "item_id",
  "email": "string",
  "item_name": "string",
  "quantity": 10,
  "expiry_date": "2024-10-11T00:00:00",
  "insert_date": "2024-10-11T12:10:44.216466"
}
```

#### GET /items/{id} - Retrieve an item by ID.

Response body:
```json
{
  "id": "item_id",
  "email": "string",
  "item_name": "string",
  "quantity": 10,
  "expiry_date": "2024-10-11T00:00:00",
  "insert_date": "2024-10-11T12:10:44.216466"
}
```

#### GET /items/filter - Filter items based on certain criteria.

Query parameters: email, expiry_date, insert_date, quantity.
Example response:
```json
[
  {
    "id": "item_id",
    "email": "string",
    "item_name": "string",
    "quantity": 10,
    "expiry_date": "2024-10-11T00:00:00",
    "insert_date": "2024-10-11T12:10:44.216466"
  }
]
```

#### GET /items/aggregation - Aggregate items by email.

Response:
```json
[
  {
    "email": "user@example.com",
    "item_count": 3
  }
]
```

#### PUT /items/{id} - Update an item by ID.

Request body:
```json
{
  "email": "updated_email",
  "item_name": "updated_name",
  "quantity": 20,
  "expiry_date": "2024-10-12"
}
```

Response body:
```json
{
  "id": "item_id",
  "email": "updated_email",
  "item_name": "updated_name",
  "quantity": 20,
  "expiry_date": "2024-10-12T00:00:00",
  "insert_date": "2024-10-11T12:10:44.216466"
}
```

#### DELETE /items/{id} - Delete an item by ID.

Response:
```json
{ "message": "Item deleted successfully" }
```

### Clock-In Records Endpoints

#### POST /clock-in - Create a new clock-in record.

Request body:
```json
{
  "email": "string",
  "location": "string"
}
```

Response body:
```json
{
  "id": "clock_in_id",
  "email": "string",
  "location": "string",
  "insert_date": "2024-10-11T12:10:44.216466"
}
```

#### GET /clock-in/{id} - Retrieve a clock-in record by ID.

Response body:
```json
{
  "id": "clock_in_id",
  "email": "string",
  "location": "string",
  "insert_date": "2024-10-11T12:10:44.216466"
}
```

#### PUT /clock-in/{id} - Update a clock-in record by ID.

Request body:
```json
{
  "email": "updated_email",
  "location": "updated_location"
}
```

Response body:
```json
{
  "id": "clock_in_id",
  "email": "updated_email",
  "location": "updated_location",
  "insert_date": "2024-10-11T12:10:44.216466"
}
```

#### DELETE /clock-in/{id} - Delete a clock-in record by ID.

Response:
```json
{ "message": "Clock-in record deleted successfully" }
```
