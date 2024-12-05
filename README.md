# Tradingview-recommendations
Check out the App:- http://103.241.65.47:8501/

## This app is auto deployed through GitHub actions CICD pipeline whenever the code is merged to the PROD branch and it runs on a remote server 


# To run this project inside a Docker Container run the commands:

###  **docker build -t streamlit-app .**

###  **docker run --env-file .env -p 8501:8501 streamlit-app**

