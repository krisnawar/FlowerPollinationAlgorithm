from numba import jit
import numpy as np
import math as mt
import random
import csv
import time
import datetime

#initiate blank list for sawah (ricefield coordinate)
sawah = list()

#initiate blank list for z value changes
z_movement = list()

#storing ricefield coordinate into a numpy array
with open('sawah.csv', 'r') as infile:
    reader = csv.reader(infile, delimiter=';')

    for row in reader:
        for_col = list()
        for col in row:
            for_col.append(float(col))
        sawah.append(for_col)

sawah = np.asarray(sawah, dtype=np.float64)

#initial device coordinate
uvus1 = [[66, 472], [83, 304], [203, 406], [202, 240], [272, 84]]
uvus2 = [[68, 472], [85, 304], [205, 406], [204, 240], [274, 84]]
uvus3 = [[66, 474], [83, 306], [203, 408], [202, 242], [272, 86]]
uvus4 = [[64, 474], [81, 306], [201, 408], [200, 242], [270, 86]]

#radius 100 coordinate
rad = 100

#necessary variable
population = list()
tempPopulation = list()
bestSolution = list()
bestPopulation = list()
foriter = list()

#count z value for current coordinate
@jit
def count_z(sawah, populasi):
    zvalue = list()
    for i in populasi:
        floorvalue = list()
        for j in sawah:
            mindist = list()
            for k in i:
                d = mt.sqrt((j[0] - k[0])**2 + (j[1] - k[1])**2)
                mindist.append(d)
            floorvalue.append(mt.floor(min(mindist)/rad))

        x = 0
        for j in floorvalue:
            x = x+j

        zvalue.append(x+len(i))
    
    return zvalue

#count the best z value
@jit
def count_z_best(sawah, bestpop):
    floorvalue = list()
    for j in sawah:
        mindist = list()
        for k in bestpop:
            d = mt.sqrt((j[0] - k[0])**2 + (j[1] - k[1])**2)
            mindist.append(d)
        floorvalue.append(mt.floor(min(mindist)/rad))
    x = 0
    for j in floorvalue:
        x = x+j
    zvalue = x+len(bestpop)
    
    return zvalue

#append initial device coordinati and assign to numpy array
def appendBTS(uvus1, uvus2, uvus3, uvus4):
    a = list()
    a.append(uvus1)
    a.append(uvus2)
    a.append(uvus3)
    a.append(uvus4)

    global population
    population = np.asarray(a, dtype=np.float64)

#set best solution before iteration begin
def setBestSolutionFirst():
    index = findIndexMin()
    bestSolution.clear()
    for i in population[index]:
        bestSolution.append(i)

#find Index of minimum z value
def findIndexMin():
    zvalue = count_z(sawah, population)

    return zvalue.index(min(zvalue))

#do local pollination
def localPollination(x, xj, xk, y, yj, yk, rand):
    x_temp = round(x + rand * (xj - xk), 2)
    y_temp = round(y + rand * (yj - yk), 2)

    value = [x_temp, y_temp]

    return value

#do global pollination
def globalPollination(x, y, rand, best):
    x_temp = round(x + rand*(x - best[0]), 2)
    y_temp = round(y + rand*(y - best[1]), 2)

    value = [x_temp, y_temp]

    return value

#check solution by comparing current solution with the previous one
def checkSolution(value):
    new_pop = np.asarray(value)
    bestsol = np.asarray(bestSolution)
    new_z = count_z(sawah, new_pop)
    for_best_z = count_z_best(sawah, bestsol)

    if(min(new_z) <= for_best_z):
        bestSolution.clear()
        for_best = value[new_z.index(min(new_z))]
        for i in for_best:
            bestSolution.append(i)

        z_movement.append(min(new_z))
        print('updated best solution')

        if(min(new_z) == len(value)):
            return True
        else:
            return False
    
    else:
        z_movement.append(for_best_z)
        print('best solution not updated!')

        return False

#write z value changes into csv file
def write_z_movement():
    with open('z_movement.csv', mode='w', newline='') as zmov:
        z_write = csv.writer(zmov, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        zlen = 1
        for z in z_movement:
            z_write.writerow([zlen, z])
            zlen += 1

#iteration of FPA
def FPA(maxiter, switchprob):
    t = 1
    populasi = population.tolist()
    while t <= maxiter:
        print('Iterasi ke-' + str(t))
        value = list()
        for i in populasi:
            xytemp = list()
            for j in i:
                rand = random.uniform(0, 1)
                if rand <= switchprob:
                    ind_j = i.index(j)
                    r1 = random.randint(0, len(i)-1)
                    while r1 == ind_j:
                        r1 = random.randint(0, len(i)-1)

                    r2 = random.randint(0, len(i)-1)
                    while r2 == r1 or r2 == ind_j:
                        r2 = random.randint(0, len(i)-1)
                    
                    xytemp.append(localPollination(j[0], populasi[populasi.index(i)][i.index(i[r1])][0], populasi[populasi.index(i)][i.index(i[r2])][0], j[1], populasi[populasi.index(i)][i.index(i[r1])][1], populasi[populasi.index(i)][i.index(i[r1])][1], rand))
                    # xytemp.append(localPollination(j[0], populasi[np.where(populasi == i), np.where(i == i[r1]), 0], populasi[np.where(populasi == i), np.where(i == i[r2]), 0], j[1], populasi[np.where(populasi == i), np.where(i == i[r1]), 1], populasi[np.where(populasi == i), np.where(i == i[r2]), 1], rand))

                else:
                    xytemp.append(globalPollination(j[0], j[1], rand, bestSolution[i.index(j)]))
                    # xytemp.append(globalPollination(j[0], j[1], rand, bestSolution[np.where(i == j)]))
                
            value.append(xytemp)

        if(checkSolution(value)):
            break

        t += 1

#main function
def main():
    start = time.time()
    print('start at : ' + str(datetime.datetime.now()))
    appendBTS(uvus1, uvus2, uvus3, uvus4)
    setBestSolutionFirst()
    FPA(5000, 0.7)
    print('BEST SOLUTION = ' + str(bestSolution))
    besto = np.asarray(bestSolution)
    print('Z value = ' + str(count_z_best(sawah, besto)))
    write_z_movement()
    end = time.time()
    print('Execution time = ' + str(end-start) + ' seconds')


if __name__ == '__main__':
    main()
