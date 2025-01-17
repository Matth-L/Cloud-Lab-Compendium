#! /bin/bash

echo "Building the docker" 

docker build -t imc_calculator .

echo "Running the docker"

docker run -p 5000:5000 imc_calculator