### Setup

Install all required packages in a virtual environment
If you are using a windows venv, run $env:FLASK_APP = "**init**.py" within wound_analysis

run npm start within frontend
run flask run within wound_analysis

The app will be running on localhost:3000
The api will be running on localhost:5000

### Example images of interface and analysis

<img src="https://github.com/ZovcIfzm/Wound-Analysis-Backend/blob/master/readme-imgs/readme1.png" width="720">  
<img src="https://github.com/ZovcIfzm/Wound-Analysis-Backend/blob/master/readme-imgs/readme2.png" width="720">  
<img src="https://github.com/ZovcIfzm/Wound-Analysis-Backend/blob/master/readme-imgs/readme3.png" width="720">

### Special implementation steps

Due to bugs with libgl1, an Aptfile needs to be added.
To add it, run
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt

### To set up venv FLASK_APP:

This commmand, $env:FLASK_APP = "**init**.py", is needed in order for the api to be run.
