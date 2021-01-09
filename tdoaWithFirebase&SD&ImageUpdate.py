import csv
import numpy as np
import random
from matplotlib import pyplot as plt
import pyrebase
import math

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
    average_x_list = []
    average_y_list = []
    x_list = []
    y_list = []
    distance_array = []
    time_of_reception = []
    error_List = []
    x = ()
    y = ()
    knownX = 3
    knownY = 4

    for column in readCSV:
        x_points = column[0]
        y_points = column[1]
        time = column[2]

        x_list.append(x_points)
        y_list.append(y_points)
        time_of_reception.append(time)

    # Removing the headings
    time_of_reception.remove('time of reception');
    x_list.remove('receiver x');
    y_list.remove('receiver y');

    T = time_of_reception
    X = x_list
    Y = y_list

    count = 0
    while count < 10:
        x_list = X
        y_list = Y
        distance_array = []
        time_of_reception = T

        #Standard_Deviation = random.gauss(0, 0.001);  # A random number from 0 to 1

        # Getting float values from the strings
        for i in range(0, len(time_of_reception)):
            time_of_reception[i] = float(time_of_reception[i]) + random.gauss(0, 0.0001)
            x_list[i] = float(x_list[i])
            y_list[i] = float(y_list[i])

        # We obtain the distances with the help of the time.
        for i in time_of_reception:
            x = i * 343;
            distance_array.append(x);

        # We are going to choose the closest receiver to be the reference and here we decide which receiver is going to be the reference
        closestReceiversDistance = min(distance_array);
        index_of_closest_receiver = distance_array.index(closestReceiversDistance);

        # Changing lists to np.arrays
        x_list = np.array(x_list)
        y_list = np.array(y_list)
        distance_array = np.array(distance_array)
        time_of_reception = np.array(time_of_reception)

        receiver1 = [x_list[0], y_list[0], distance_array[0], time_of_reception[0]]
        receiver2 = [x_list[1], y_list[1], distance_array[1], time_of_reception[1]]
        receiver3 = [x_list[2], y_list[2], distance_array[2], time_of_reception[2]]
        receiver4 = [x_list[3], y_list[3], distance_array[3], time_of_reception[3]]

        receivers_list = [receiver1, receiver2, receiver3, receiver4]
        receivers_list_copy = receivers_list
        reference_receiver = receivers_list[index_of_closest_receiver]
        receivers_list.remove(receivers_list[index_of_closest_receiver])
        left_receivers = receivers_list
        reference_receiver = np.array(reference_receiver)
        left_receivers = np.array(left_receivers)

        r1 = closestReceiversDistance;

        A = np.array([
            [left_receivers[0][0] - reference_receiver[0], left_receivers[0][1] - reference_receiver[1]],
            # (left_receivers[0][3] - (reference_receiver[3]) * (343 ** 2))
            [left_receivers[1][0] - reference_receiver[0], left_receivers[1][1] - reference_receiver[1]],
            # (left_receivers[1][3] - (reference_receiver[3]) * (343 ** 2))
            [left_receivers[2][0] - reference_receiver[0], left_receivers[2][1] - reference_receiver[1]],
            # (left_receivers[2][3] - (reference_receiver[3]) * (343 ** 2))
        ])

        c = np.array([
            (left_receivers[0][0] - reference_receiver[0]) ** 2 + (
                        left_receivers[0][1] - reference_receiver[1]) ** 2 - (
                        ((left_receivers[0][2] - reference_receiver[2])) ** 2),
            (left_receivers[1][0] - reference_receiver[0]) ** 2 + (
                        left_receivers[1][1] - reference_receiver[1]) ** 2 - (
                        ((left_receivers[1][2] - reference_receiver[2])) ** 2),
            (left_receivers[2][0] - reference_receiver[0]) ** 2 + (
                        left_receivers[2][1] - reference_receiver[1]) ** 2 - (
                        ((left_receivers[2][2] - reference_receiver[2])) ** 2),
        ])

        d = np.array(
            [-1 * (left_receivers[0][2] - reference_receiver[2]), -1 * (left_receivers[1][2] - reference_receiver[2]),
             -1 * (left_receivers[2][2] - reference_receiver[2])])
        A_Trans = A.transpose();
        AxA_Trans = np.dot(A_Trans, A)

        inverse = np.linalg.inv(AxA_Trans)
        inverseXA_Trans = np.dot(inverse, A_Trans)
        lefthandside = np.dot(0.5, inverseXA_Trans)

        r1x2 = r1 * 2;
        r1x2_d = np.dot(r1x2, d)
        righthandside = np.add(c, r1x2_d)

        t = np.dot(lefthandside, righthandside)

        # t contains x= unknownX - referenceX
        x = t[0] + reference_receiver[0]
        y = t[1] + reference_receiver[1]

        errCount = math.sqrt((knownX - x) ** 2 + (knownY - y) ** 2)
        error_List.append(errCount)

        #plt.scatter(x, y, color='red')
        #plt.savefig('xyplot.png', dpi=300, bbox_inches='tight')

        #print('************************')
        #print(x)
        #print(y)
        #print('************************')
        average_x_list.append(x)
        average_y_list.append(y)
        count = count + 1

    errorSum = 0
    for i in error_List:
        errorSum = (i ** 2) + errorSum;
    error = math.sqrt((errorSum / len(error_List)))

    print('Error')
    print(error)
    final_x = sum(average_x_list) / len(average_x_list)
    final_y = sum(average_y_list) / len(average_y_list)
    #print(average_x_list)
    #print(average_y_list)

    print('Final X and Y Points ')
    print(final_x)
    print(final_y)


    counts = db.child("Count").get()
    oldCount = ();
    newCount = ();
    if counts.val():
        oldCount = counts.val().get('count')
        newCount = oldCount + 1
        print(oldCount)
        print(newCount)
    else:
        oldCount = 0
        newCount = oldCount + 1


    countString = newCount.__str__()
    # The data that we are going to push to the firebase
    data = {
        "x": final_x, #x  x and y are the last ones from the while loop
        "y": final_y #y
    }
    count = {
        "count": newCount
    }
    #db.child("Location").update(data)
    db.child("Count").update(count)
    db.child("Location".__add__(countString)).update(data)

    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.grid()

    plt.xlim(0, 10)
    plt.ylim(0, 5)

    plt.scatter(final_x , final_y, color='blue') #The average point
    plt.scatter(knownX, knownY, color='green') #True Point

    plt.savefig('xyplot.png', dpi=300, bbox_inches='tight')
    path_on_cloud = "images/xyplot.png"
    path_local = "xyplot.png"

    storage.child(path_on_cloud.__add__(countString)).put(path_local)