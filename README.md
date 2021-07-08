# TDOA Project
    
TDOA Project is a project to calculate the location of a robot. Within this project, a csv file is needed to prepare the calculations, 
the CSV file contains the stabil locations of the sensors, and for each point, the time is recorded. By using the CVS file provided,
The time difference of arrival algorithm is used, and X and Y values are obtained. By using Firebase Realtime Database, we use the X and
Y values calculated everytime the code is run.

## Installation for Python
    You must have the version Python 3.7.4 to be able to continue the steps.

  
 ## Firebase
    To be able to use all the features of the application, you must use Firebase. Please check out the link below and make sure you follow the steps.
  
    https://firebase.google.com/docs/flutter/setup
  
  ## Versions
   Python version: 1.0.0+1
  ## Environment
    sdk: ">=2.1.0 <3.0.0"
    
  ## Dependencies  
    Pyrebase: 3.0.27

    matplotlib: 3.3.3
    
    numpy: 1.19.3
    
    
   ## Steps to use the code
   
    1) Make sure you have the IDE that you prefer, I have used PyCharm Community Edition. Make sure you have Android 
   
    2) After setting up the environment, you can download the zip file. You should unzip the file that you have downloaded. 
    
      Then open the file at the IDE you prefer.
    
    3) Make sure the Python interpreter is configured. You can follow the steps in the,
    
      following link: https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html
    
    4) There are multiple branches in the repository, and multiple .py files. It is because, 
    
        more features have been added step by step. The most updated one, and the one I advice 
        
        to use is the tdoaFirebaseSDErrorImageRead.py file.
    
    5) Before you run the tdoaFirebaseSDErrorImageRead.py, you are going to need to make some changes.

       After you create a Realtime Database in Firebase, obtain the firebaseConfig for the database you 
       
       created. And you need to replace it with the one present in the code (10th to 19th lines)
       
    6) For the code to work properly and use the values of your own, you need to change the CSV files. 
    
        If you would like you can create a whole new csv file and change the name in 25th line. 
        
        Currently, it is tdoa1. If you are going to create a new file, please make sure you have exactly 
        
        the same format as the tdoa1. You should have the same structure and exact same names for the columns. 
        
        In the CSV file each row represents a sensor that is placed around the room. Receiver x means the
      
        x position of the sensor, and Receiver y columns the y position of the sensor, and the time of 
        
        reception is the value that the specific time when this sensor receives the signal.
      
    7) After making all these changes, run the code, you are going to receive X and Y values. 
    
       The values are not going to be exactly the same because, the code contains the standard deviation, 
       
       because in real world, there might be errors while working with signals. So even if you run 
       
       the same CSV code multiple times, you are going to obtain different values each time.
      
    8) I hope you can make a good use of this repository! If you need to use it, you are free to do so, 
    
        if you have questions please reach me via e-mail: bilenmelike@gmail.com
      
     
    
