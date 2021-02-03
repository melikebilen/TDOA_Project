import csv
import numpy as np
from scipy import linalg
import math

with open('new.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    distancelist = []
    x_list = []
    y_list = []

    distance_array = []
    calculated_time_of_reception = []

    x = ()
    y = ()


    for column in readCSV:
        distance = column[2]
        x_points = column[0]
        y_points = column[1]


        distancelist.append(distance)
        x_list.append(x_points)
        y_list.append(y_points)


#Removing the headings
    distancelist.remove('distance');
    x_list.remove('receiver x');
    y_list.remove('receiver y');


#Getting float values from the strings
    for i in range(0, len(distancelist)):
        distancelist[i] = float(distancelist[i])
        x_list[i] = float(x_list[i])
        y_list[i] = float(y_list[i])


#Distance array'i kendi hesapladığımı daha düzgün şekilde kullanabilmek için aldım.
    for i in distancelist:
        x= math.sqrt(i);
        distance_array.append(x);

#Zamanı kendim hesaplıyorum;
    for i in distance_array:
        x = i/343;
        calculated_time_of_reception.append(x);

#DECIDING WHICH RECEIVER IS GOING TO BE THE REFERENCE.
    closestReceiversDistance = min(distance_array);
    index_of_closest_receiver = distance_array.index(closestReceiversDistance);
    t0= closestReceiversDistance
    #print(index_of_closest_receiver)

#Changing lists to np.arrays
    distancelist = np.array(distancelist)
    x_list = np.array(x_list)
    y_list = np.array(y_list)

    distance_array = np.array(distance_array)
    calculated_time_of_reception = np.array(calculated_time_of_reception)

    receiver1 = [x_list[0], y_list[0], distance_array[0], calculated_time_of_reception[0]]
    receiver2 = [x_list[1], y_list[1], distance_array[1], calculated_time_of_reception[1]]
    receiver3 = [x_list[2], y_list[2], distance_array[2], calculated_time_of_reception[2]]
    receiver4 = [x_list[3], y_list[3], distance_array[3], calculated_time_of_reception[3]]

    receivers_list = [receiver1,receiver2,receiver3,receiver4]
    reference_receiver = receivers_list[index_of_closest_receiver]
    receivers_list.remove(receivers_list[index_of_closest_receiver])
    left_receivers = receivers_list

    reference_receiver = np.array(reference_receiver)
    print('The left receivers')
    left_receivers = np.array(left_receivers)
    print(left_receivers)
    print('************************')
    print('The reference receiver that I obtained')
    print(reference_receiver)


    r1 = closestReceiversDistance;
    #print(closestReceiversDistance)

    A = np.array([
        [left_receivers[0][0] - reference_receiver[0], left_receivers[0][1] - reference_receiver[1]],
        [left_receivers[1][0] - reference_receiver[0], left_receivers[1][1] - reference_receiver[1]],
        [left_receivers[2][0] - reference_receiver[0], left_receivers[2][1] - reference_receiver[1]],
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

    #(t)
    print('************************')
    print('X point:')
    print(x)
    print('Y point:')
    print(y)


#working on yayan article
