# How to run

## Prerequisite
- pipenv must be installed to manage the dependencies. See here [link](https://pypi.org/project/pipenv/#:~:text=Usage%20Examples%3A%20Create%20a%20new,%2D%2Dpre%20Show%20a%20graph)
- Assuming you have a shell in the root directory of the project 

```shell
$ cd backend
```

Assuming this is the first time you have to install the dependencies and pipenv creates a virtual environment for you with them installed.

```shell
$ pipenv install
```
Then you can activate the environment with the shell command. NOTE: You need to activate the environment every time you want to run the system.
```shell
$ pipenv shell
```

After that move to the banksystem project
```shell
 $ cd banksystem
```

Then run the server with the command
```shell
$ python manage.py runserver
```

This sums up the start up process of the backend server. You can either interact with it in two ways.

## 1- Postman
You can find the very helpful postman documenter here [link](https://documenter.getpostman.com/view/3995062/Tzz7PJAM). It provides ready made request

## 2- UI
You can also use the UI by going over to the Frontend/ directory and opening Login.html in your favorite browser and it'll provide most of the main interactions.
