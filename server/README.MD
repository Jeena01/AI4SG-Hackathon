# FastAPI Recommender System API

## Overview

This is a FastAPI-based recommender system API that connects clients with providers based on their needs, preferences, and geographical locations. The system uses an SQLite database for storage and supports CRUD operations.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Running the Application](#running-the-application)

## Features

- Add and manage providers and clients.
- Map clients to providers with ratings.
- Generate recommendations based on content and collaborative filtering.
- Populate the database with dummy data for testing.

## Technologies

- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```
  
### 2. Create and Activate the Virtual Enviroment

For creating a virtual environment, use the following command:
```
  python -m venv .venv
```
To activate the enviroment:
  
On Windows:
  ```
.\.venv\Scripts\activate
  ```
On macOS/Linux:
  
```

source .venv/bin/activate

  ```
### 3. Install Dependencies
```

pip install fastapi uvicorn sqlalchemy pydantic
  
## Running the Application

  To start the FastAPI server, run:

bash```
uvicorn main:app --reload
```

  Your API will be available at http://127.0.0.1:8000


## Endpoints

### Root Endpoint

- **GET** `/`
  - **Description:** Returns a welcome message.
  - **Response:**
    ```json
    {
      "message": "Welcome to the SQLite-based recommender system API!"
    }
    ```

### Providers

#### Add a Provider

- **POST** `/providers/`
  - **Description:** Add a new provider.
  - **Request Body:**
    ```json
    {
      "name": "Provider Name",
      "specialization": "Specialization",
      "location": "Location",
      "gender": "Gender",
      "language": "Language",
      "cultural_background": "Cultural Background"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "name": "Provider Name",
      "specialization": "Specialization",
      "location": "Location",
      "gender": "Gender",
      "language": "Language",
      "cultural_background": "Cultural Background"
    }
    ```

#### Populate Dummy Data

- **GET** `/populate-dummy-data/`
  - **Description:** Populate the database with dummy providers and clients for testing.
  - **Response:**
    ```json
    {
      "message": "Dummy data added successfully."
    }
    ```

### Clients

#### Add a Client

- **POST** `/clients/`
  - **Description:** Add a new client.
  - **Request Body:**
    ```json
    {
      "name": "Client Name",
      "need": "Client Need",
      "location": "Client Location",
      "gender": "Gender",
      "language": "Language",
      "cultural_background": "Cultural Background",
      "preferred_gender": "Preferred Gender",
      "preferred_cultural_background": "Preferred Cultural Background"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "name": "Client Name",
      "need": "Client Need",
      "location": "Client Location",
      "gender": "Gender",
      "language": "Language",
      "cultural_background": "Cultural Background",
      "preferred_gender": "Preferred Gender",
      "preferred_cultural_background": "Preferred Cultural Background"
    }
    ```

### Client-Provider Mapping

#### Add Client-Provider Mapping

- **POST** `/client-provider-mapping/`
  - **Description:** Map a client to a provider with an optional rating.
  - **Request Body:**
    ```json
    {
      "client_id": 1,
      "provider_id": 1,
      "rating": 5
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "client_id": 1,
      "provider_id": 1,
      "rating": 5
    }
    ```

### Recommendations

#### Get Recommendations

- **GET** `/recommend/{client_id}`
  - **Description:** Get provider recommendations for a specific client based on their preferences.
  - **Parameters:**
    - `client_id`: The ID of the client.
  - **Response:**
    ```json
    {
      "recommendations": [
        {
          "id": 1,
          "name": "Provider Name",
          "specialization": "Specialization",
          "location": "Location",
          "gender": "Gender",
          "language": "Language",
          "cultural_background": "Cultural Background",
          "score": 85.5
        }
      ]
    }
    ```

## Error Responses

- **404 Not Found**
  - Returned when a requested resource (e.g., client or provider) does not exist.
  - **Response:**
    ```json
    {
      "detail": "Client or Provider not found."
    }
    ```

## Additional Information

- Ensure the database is set up correctly before making requests.
- Use tools like Postman or cURL for testing the API endpoints.
