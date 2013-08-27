Software-Engineering
====================

Software Engineering project. 

The purpose of this project was to create a mobile application for marching band memebers to learn their steps faster.
The band instructor would visit the website and upload the pdf from the band routine generating sofware called Pyware.
The server would take that pdf and extract the relitive location for students and save them to the database. See views.py line 144ish.
The student on their mobile application would make gps calls via the devices gps locator and send that location to the server. See views.py line 124ish.
The server would then find the difference between actual location(sent from student) and desired location
(extrapolated from relative location from database). See views.py line 65ish.

The above description is very basic, there was also a custom api being built for the students to perform a pseudo-login that way we could give them ids. 
We also interfaced with the html5 locaion api (the instructor would set the location of the home and away side 50 yard line).
There is also some neat javascript to place dots on an image of a football field for the instructor to browse. The previous 2 features can be found on drill.html. 


