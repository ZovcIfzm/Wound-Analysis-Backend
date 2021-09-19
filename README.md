### Project intro
This project allows you to upload images of mice with wounds, and find the area of their wounds. This project consists of three components. Frontend interface, backend api, and ml models. Each component has it's own repository. For basic wound area measurement, just frontend and backend is required.

### Backend Setup
* Clone the project
* (Optional) Create a virtual environment. This is generally recommended for any python project. 
* Install all packages with pip install -r requirements.txt
* Run ```python3 wsgi.py``` if using Linux/MacOS, or ```py wsgi.py``` if using Windows. All wsgi.py does, is basically the same exact thing as running ```flask run``` inside the wound_analysis subfolder, but without the need for environmental variables to be set.
* Test if it's running by going to localhost:5000 on your web browser, it should say "This is the wound analysis api"

### Frontend setup
* Follow the frontend repo's instructions. Basically just ```npm install``` in the root directory then ```npm run```.

The website interface (frontend) will be running on localhost:3000
The api will be running on localhost:5000

### Special implementation steps
Due to bugs with libgl1, an Aptfile needs to be added.
To add it, run
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
