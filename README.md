# BitBid
CSCE 606 - BitBid - Team 3GB

[Notes](https://drive.google.com/drive/folders/1pU8iHhiHwo8pn0ndJedjYgVnxPt8D0Wy)

# Developer setup
* You need to have python3 installed on your machine
* Installation
* pip install virtualenv 
* Create a virtual enviornment using `python3 -m venv \path\to\virtual\env`
* Activate virtual environment using\
    * linux `source \path\to\virtual\env\bin\activate`
    * windows `\path\to\virtual\env\bin\activate.bat`
* Install the necessary modules using `pip install -r requirements.txt`
* Change directory `cd bitbid_project/`
* Migrate and sync DB\
    * `python3 manage.py makemigrations`
    * `python manage.py migrate`
    * `python manage.py migrate --run-syncdb`
* Run the server `python3 manage.py runserver`. The default port it uses is `8000`. If you want to change it use `python3 manage.py runserver 8080`
* Django also supports hot reload, so you don't have to stop and re-run the server for every change you make.
* When you're done, deactivate environment using `deactivate`

# Test environment setup
## BDD tests
* Tests make use of the following python packages: pytest-bdd, pytest, and selenium (they are all enumerated in the requirements.txt for easy installation of python packages). 
* Additionally, since our tests make use of selenium webdriver, you'll need to install gecko driver on your system. Check [Gecko download links](https://github.com/mozilla/geckodriver/releases). Once you've downloaded it, unzip it and give execute permissions (eg: chmod +x geckodriver) and move it to a location `/tmp` (or a location of your choice that you can reference in your test file).
    * Note: If you're using macOS and apple flags geckodriver as malicious then you might have to manually allow it as below:
    ![malicious](/readme_assets/malicous.png)
    * If you're on windows and you encounter a similar block, then you may have to just allow it in windows smart sceen.
* Gecko uses firefox as its browser engine, so you need to install firefox on your machine. It is recommended to use the default installation. You may choose to do a custom installation, in which case you have to set the path to the firefox binary in your test file.
* Start your server with `python3 manage.py runserver` in one terminal window. 
* Open another terminal window and you can run all the BDD tests with a simple command: `pytest bitbid_project/bdd/`. 

## Unit tests and coverage statistics
* Change directory `cd bitbid_project/`
* Run `coverage run --branch --source='.' manage.py test` to run all test cases
* Run `coverage html` to generate HTML report or `coverage report` to generate command line report
* If you generate HTML report, navigate to `bitbid_project\htmlcov` and open `index.html` with your favourite browser.



# [Deployment / Production guide](https://testdriven.io/blog/deploying-django-to-heroku-with-docker/)
* DEPRECATED
    <strike>
    * At this moment, our target is Heroku. However, building image (steps 1-3) remains same regardless of the target platform.
        1. Install [Docker desktop](https://www.docker.com/products/docker-desktop/) (or perhaps docker engine would suffice? idk) on your local machine.
        2. Go to the project root directory (i.e, wherever the Dockerfile is located)
        3. Build image using `docker buildx build --platform linux/amd64 -t bit-bid .` The reason to build for a sepcific platform is because if you're using applice silicon (M1 or M2) to build docker image, there's a problem with architecture mismatch. Heroku containers are primarily linux (amd64), but apple silicon chipset is an enhanced mobile chipset (arm64). It is noticed that the container crashes right away due to this configuration mismatch. Therefore it is a good practice to build docker images for a specific platform.
        4. Optional: Verify the container runs on a linux VM `docker run -d --name bit-bid-container -p 8000:8000 bit-bid`. Stop `docker stop bit-bid-container` and remove `docker rm bit-bid-container` the container.
        5. Push the image to heroku's container registery:\
        `docker tag bit-bid registry.heroku.com/bit-bid/web`
        `docker push registry.heroku.com/bit-bid/web`
        6. Once pushed, image can be released using (you need heroku CLI for this step):\
        `heroku container:release web --app bit-bid`
    </strike>

*   UPDATE:
    *   Github workflows has been setup for this repository to deploy to heroku using `HEROKU_API_KEY` secret
    * If you want a new build out, push your code to `/release/**` branch and a new build will be triggered :)
    * You can check the status of the build under the `Actions` tab
