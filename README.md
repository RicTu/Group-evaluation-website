# Group evaluation website application
This repository contains a website that easy for students to evaluate the performance of themself and their team members.
The webpage is designed for [Nordlinglab Profskills](https://www.nordlinglab.org/profskills/).

## Why we need this webpage
During the Profskill course, students need to give their presentations each week. And the group member will be changed every three weeks.
For each week, students need to evaluate the contributions of every team member including themself.
The translation of team members brings a lot of trouble to the course assistant and teacher (e.g. recording scores for each group).
Therefore, we want to design a system that is easy for students to do the evaluation and also easy for the assistant to compute the semester grades.

## Backbone of the webpage
This webpage is built with the flask.
Using the JS for the user interface and the python code for the statistic.

## Lunch the webpage
* install the required package
```
pip install -r requirements.txt
```

* Put student list at
```
website/student_list.csv
```

* Activate app
```
python main.py
```

## How to use it
* First time access the webpage, sign up an account
<img src="figures/home.png" height="300">

* Log in with student account
<img src="Figure/student.png" height="300">

* Log in with admin account
<img src="Figure/admin.png" height="300">
(The group number with 9999 will redirect to the admin page)

* The score will be stored at student_com.csv


## Reference
https://youtu.be/dam0GPOAvVI



