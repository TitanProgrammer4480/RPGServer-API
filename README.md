# RPG Minecraft Server API

This is a Flask-based REST API that interacts with Google Firebase Firestore to manage users and characters of a RPG Minecraft server. It provides CRUD operations for both users and characters while ensuring authentication via an API key. This project was a collaboration with an friend of me. Thanks to [Kerzinator](https://github.com/Kerzinator24) for working with me.

## 🚀 Features
- User authentication via API key
- CRUD operations for Users and Characters
- Firestore database integration
- Flask-based RESTful architecture

## 📌 Requirements
- Python 3.x
- Flask
- Firebase Admin SDK

## 🛠 Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TitanProgrammer4480/RPGServer-API
   cd RPGServer-API
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Firebase credentials:
   - Obtain Firebase Admin SDK credentials (JSON file) from the Firebase Console.
   - Set the environment variables:
     ```bash
     export AUTH_TOKEN="your_secret_token"
     export FIREBASE_CRED="path/to/firebase_credentials.json"
     ```

4. Run the API:
   ```bash
   python app.py
   ```

## 🔑 Authentication
The API uses an API key for authentication, passed in the request headers:
```http
API-Key: your_secret_token
```

## 📡 API Endpoints

### Home Route
- `GET /` – Returns the home page.

### User Management
- `GET /api/users` – Retrieves all users.
- `GET /api/user` – Retrieves a specific user by `uuid`.
- `POST /api/user` – Creates a new user.
- `PUT /api/user` – Updates an existing user.
- `DELETE /api/user` – Deletes a user.

### Character Management
- `GET /api/character` – Retrieves a character by `id`.
- `POST /api/character` – Creates a new character.
- `PUT /api/character` – Updates an existing character.
- `DELETE /api/character` – Deletes a character.

## 📜 License
This project is licensed under the MIT License.
