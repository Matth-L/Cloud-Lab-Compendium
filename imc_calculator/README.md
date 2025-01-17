# 🏋️‍♂️ IMC Calculator

In this question, we were asked to build an IMC (BMI) calculator using any technology of our choice.  

We chose to build this application with **Python** and **Flask**. The application is in the `app.py` file.  

🗄️ Data entered during the session will be stored in a **SQLite** database.  

🐳 We created a Docker container to run the application, and the **Dockerfile** is located in the root of the project.  

To run the application, use the following commands in the terminal:

```bash
docker build -t imc_calculator .
docker run -p 5000:5000 imc_calculator
```