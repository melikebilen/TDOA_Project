import csv
import numpy as np
import random
from matplotlib import pyplot as plt
import pyrebase
from statistics import mean

firebaseConfig = {
    "apiKey": "AIzaSyBQjxxJqCcYhjYDH6GFwjSGdQ7VeqVGhCI",
    "authDomain": "tdoa-23cf7.firebaseapp.com",
    "projectId": "tdoa-23cf7",
    "storageBucket": "tdoa-23cf7.appspot.com",
    "messagingSenderId": "611153024504",
    "appId": "1:611153024504:web:0044eeb00f4b4d83af720d",
    "measurementId": "G-XJE676ZHYK",
    "databaseURL": "https://tdoa-23cf7-default-rtdb.firebaseio.com/"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
db = firebase.database()

with open('tdoa.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    x_list = []
    y_list = []
    distance_array = []
    time_of_reception = []
    standard_deviation_list = []
    Standard_Deviation = random.gauss(0, 0.001) ;  # A random number from 0 to 1
    count = 0

    x = ()
    y = ()

    for column in readCSV:
        x_points = column[0]
        y_points = column[1]
        time = column[2]

        x_list.append(x_points)
        y_list.append(y_points)
        time_of_reception.append(time)

#Removing the headings
    time_of_reception.remove('time of reception');
    x_list.remove('receiver x');
    y_list.remove('receiver y');

#Getting float values from the strings
    for i in range(0, len(time_of_reception)):
        time_of_reception[i] = float(time_of_reception[i]) + Standard_Deviation
        x_list[i] = float(x_list[i])
        y_list[i] = float(y_list[i])

#We obtain the distances with the help of the time.
    for i in time_of_reception:
        x = i * 343;
        distance_array.append(x);

#We are going to choose the closest receiver to be the reference and here we decide which receiver is going to be the reference
    closestReceiversDistance = min(distance_array);
    index_of_closest_receiver = distance_array.index(closestReceiversDistance);

#Changing lists to np.arrays
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    distance_array = np.array(distance_array)
    time_of_reception = np.array(time_of_reception)

    receiver1 = [x_list[0], y_list[0], distance_array[0], time_of_reception[0]]
    receiver2 = [x_list[1], y_list[1], distance_array[1], time_of_reception[1]]
    receiver3 = [x_list[2], y_list[2], distance_array[2], time_of_reception[2]]
    receiver4 = [x_list[3], y_list[3], distance_array[3], time_of_reception[3]]

    receivers_list = [receiver1,receiver2,receiver3,receiver4]

    reference_receiver = receivers_list[index_of_closest_receiver]
    receivers_list.remove(receivers_list[index_of_closest_receiver])
    left_receivers = receivers_list
    reference_receiver = np.array(reference_receiver)
    left_receivers = np.array(left_receivers)

    r1 = closestReceiversDistance;

    A = np.array([
        [left_receivers[0][0] - reference_receiver[0], left_receivers[0][1] - reference_receiver[1]], #(left_receivers[0][3] - (reference_receiver[3]) * (343 ** 2))
        [left_receivers[1][0] - reference_receiver[0], left_receivers[1][1] - reference_receiver[1]], # (left_receivers[1][3] - (reference_receiver[3]) * (343 ** 2))
        [left_receivers[2][0] - reference_receiver[0], left_receivers[2][1] - reference_receiver[1]], #(left_receivers[2][3] - (reference_receiver[3]) * (343 ** 2))
    ])

    c = np.array([
        (left_receivers[0][0] - reference_receiver[0])**2 + (left_receivers[0][1] - reference_receiver[1])**2 - (((left_receivers[0][2] - reference_receiver[2])) ** 2),
        (left_receivers[1][0] - reference_receiver[0])**2 + (left_receivers[1][1] - reference_receiver[1])**2 - (((left_receivers[1][2] - reference_receiver[2])) ** 2),
        (left_receivers[2][0] - reference_receiver[0])**2 + (left_receivers[2][1] - reference_receiver[1])**2 - (((left_receivers[2][2] - reference_receiver[2])) ** 2),
    ])

    d=np.array([-1 * (left_receivers[0][2] - reference_receiver[2]), -1 * (left_receivers[1][2] - reference_receiver[2]), -1 * (left_receivers[2][2] - reference_receiver[2])])
    A_Trans = A.transpose();
    AxA_Trans = np.dot(A_Trans, A)

    inverse = np.linalg.inv(AxA_Trans)
    inverseXA_Trans = np.dot(inverse, A_Trans)
    lefthandside = np.dot(0.5, inverseXA_Trans)

    r1x2= r1*2;
    r1x2_d= np.dot(r1x2,d)
    righthandside = np.add(c, r1x2_d)

    t = np.dot(lefthandside, righthandside)

    #t contains x= unknownX - referenceX
    x = t[0] + reference_receiver[0]
    y = t[1] + reference_receiver[1]


    print(x)
    print(y)
    print('Standard deviation')
    print(Standard_Deviation)

    plt.scatter(x , y)
    plt.savefig('xyplot.png', dpi=300, bbox_inches='tight')

    path_on_cloud = "images/xyplot.png"
    path_local = "xyplot.png"
    storage.child(path_on_cloud).put(path_local)

    #The data that we are going to push to the firebase
    data = {
        "x" : x,
        "y" : y
    }
    db.child("Location").update(data)
