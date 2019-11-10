Requirement

1-Python- Download python for windows- "https://www.python.org/downloads/"  (In installer - Check the box next to Add Python 3.5 to PATH and then click Install Now)
	- After installation, open the command prompt and check that the Python version matches the version you installed by executing:
	  -->   python --version
2-Pip- You’ll also need to install pip. If you downloaded Python from Python’s website, you likely already have pip installed (you can check by running pip in a terminal window). If you don’t have it installed, be sure to install it before moving on!

3-Django-Install django by following command:---> pip install django

Server

1- To start server run the given command in attendence directory--->python manage.py runserver
2- copy the link the provided and paste in browser
3- To create admin run the given command and provide credentials-->python manage.py createsuperuser


Admin

1-Username of student must be its Rollno.
2-To provide department and semester, add student to their group while creating Student user.For example if a student belongs to EE branch and 5 semester then add him to Group "D-EE" and "Sem-5".
3-Add new department by creating group with name as "D-CSE","D-EE"(for example).
4-Defaulter student are highlighted by red.
5-Provide password of the format first_nama@last_name

Faculty

1-Faculty can register course only once. If the the course is already registered then he may join the course with the faculty who register the course.
2-Faculty can take multiple attendance in a day for extra classes with a gap of atleat 1hr.


Student
1-Student can register course once and view attendance.
