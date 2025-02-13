# 🏦 Banking Application with Docker

This project implements a very simple banking application using Docker. The application allows users to create accounts, deposit and withdraw money, and check account balances. It is built using Python with Flask for the backend and SQLite for the database.

## 🚀 Getting Started

### 📋 Prerequisites

- Docker installed on your machine

### 🛠️ Building and Running the Application

1. **Build the Docker Image:**

    ```sh
    docker build -t banque_app .
    ```

2. **Run the Docker Container:**

    ```sh
    docker run -p 5000:5000 banque_app
    ```

3. **Access the Application:**

Open your web browser and navigate to `http://localhost:5000` to interact with the banking application.

### 🐳 Docker Hub

The Docker image for this application is available on Docker Hub. You can pull and run the image using the following commands:

1. **Pull the Image from Docker Hub:**

    ```sh
    docker pull matthl2002/banking_app:v1
    ```

2. **Run the Image:**

    ```sh
    docker run -p 5000:5000 matthl2002/banking_app:v1
    ```

## 📂 Project Structure

- **`app.py`**: Contains the main application logic, including routes and database operations.
- **`templates/`**: Contains HTML templates for the web interface.
- **`Dockerfile`**: Defines the Docker image configuration.