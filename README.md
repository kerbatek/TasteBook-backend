# TasteBook Backend

**TasteBook** is a recipe-sharing platform where users can upload, browse, and save recipes. This repository contains the backend code for the platform, built using **Flask** and **MongoDB**.

## Features

- User authentication (signup, login)
- Recipe creation, editing, and deletion
- User profiles with recipe collections and favorites
- Search and filter recipes by tags, cuisine, and more
- Ratings and comments on recipes
- RESTful API for frontend interaction

## Tech Stack

- **Backend Framework**: Flask
- **Database**: MongoDB (with PyMongo)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI (optional)

## Project Setup

### Prerequisites

- Python 3.8+
- MongoDB

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/TasteBook-backend.git
2. Navigate to the project directory:

   ```bash
   cd TasteBook-backend
3. Create a virtual environment:
   
   ```bash 
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
5. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   
   ```makefile
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   MONGO_URI=mongodb://localhost:27017/tastebook
6. Start the Flask development server:

   ```bash
   flask run
7. Access the API at `http://localhost:5000`.

## API Endpoints

- **`POST /auth/register`**: Register a new user
- **`POST /auth/login`**: Login a user and generate a JWT token
- **`GET /recipes`**: Retrieve all recipes
- **`GET /recipes/<id>`**: Retrieve a single recipe by ID
- **`POST /recipes`**: Create a new recipe (requires authentication)
- **`PUT /recipes/<id>`**: Update an existing recipe by ID (requires authentication)
- **`DELETE /recipes/<id>`**: Delete a recipe by ID (requires authentication)
- **`GET /recipes/search?q=<query>`**: Search for recipes by keyword, tags, or cuisine
- **`POST /recipes/<id>/comment`**: Add a comment to a recipe (requires authentication)
- **`GET /users/<username>`**: Retrieve user profile and their uploaded recipes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


