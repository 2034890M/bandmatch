# bandmatch

Assuming that you have cloned the code from GitHub to your machine. If not, you will need to type "git clone https://<USERNAME>:<PASSWORD>@github.com/<OWNER>/<REPO_NAME>.git <workspace>" on your command line. If you do not know how to open a command line, look at step 1.

1) Open command line. (http://lmgtfy.com/?q=How+to+open+command+line%3F%3F%3F)

2) Make a virtual environment. (http://lmgtfy.com/?q=How+to+make+a+virtual+environment%3F)

3) Go to the your local repository.

4) Type in: pip install -r requirements.txt. Pip will install all the required packages.

5) Go to the folder bandmatch_project

6) Type in: python manage.py makemigrations bandmatch

7) Type in: python manage.py migrate

8) Type in: python populate_bandmatch.py

9) Type in: python manage.py runserver

10) The site is now running locally on your computer at 127.0.0.1:8000/bandmatch