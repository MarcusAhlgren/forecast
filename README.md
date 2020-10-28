# Forecasting

## Project Structure
    ├── data      <- Storage for raw, processed data and predictions.     
    ├── notebooks <- Notebooks for exploring data and documenting findings.  
    ├── models    <- Trained models.  
    ├── src       <- Source code for use in this project.  
    ├── Pipfile   <- Environment and library dependencies.  
    └──  api.py   <- Flask app for generating predictions
    
All documentation can be found in the notebooks. Data exploration and model justification is found in **0.1-exploration** and model selection and predictions are generated in **0.2-model_validation**.

## Usage

In this project pipenv is used to handle dependencies and creating a virtual environment. If you don't already have pipenv it can be installed through

    pip install pipenv

To install the libraries and create the virtual environment simply run

    pipenv install
    pipenv shell

Now you are ready to run the project code.

## API Endpoint

There is currently not an API endpoint. The idea was to host a flask app on AWS using Lambda and API Gateway but my attempt was unsuccessful to host it in AWS. The Flask app can only be run locally by typing in the console:

    python api.py
    
Forecasts can be produced either by providing the argument **steps** which produces forecasts for **steps** months where 2020-01-01 is the first month.

**Example:**
    
    curl -X POST "http://127.0.0.1:5000/predict?steps=3"

**returns:**
    
    {
      "2020-01-01": 913407.0, 
      "2020-02-01": 931073.0, 
      "2020-03-01": 946844.0
    }

To forecast a certain interval provide the arguments **start** and **end**

**Example:**

    curl -X POST "http://127.0.0.1:5000/predict?start=2020-02-01&end=2020-06-01"
    
returns: 
    
    {
      "2020-02-01": 931073.0, 
      "2020-03-01": 946844.0, 
      "2020-04-01": 958014.0, 
      "2020-05-01": 941466.0
    }