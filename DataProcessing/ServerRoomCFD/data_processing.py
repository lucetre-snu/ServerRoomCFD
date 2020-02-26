modes = [['24C', '27C', '30C'], \
         ['50perc', '75perc', '100perc'], \
         ['rack1', 'rack2']]
racks = [[10, 20, 22, 24, 28, 30, 34, 36], \
         [13, 18, 22, 24, 28, 30]]

def readFile(filename):
    rf = open(filename, mode='r')
    print(filename)
    rf.close()
    return {1:1}

if __name__ == '__main__':
    for i in range(len(modes[0])):
        for j in range(len(modes[1])):
            for k in range(len(modes[2])):
                filename = modes[0][i] + '/' + modes[1][j] + '/' + modes[2][k]
                for l in range(len(racks[k])):
                    filename1 = filename + '/' + str(racks[k][l]) + '_Inlet_0.dat'
                    readFile(filename1)
                    filename2 = filename + '/' + str(racks[k][l]) + '_Outlet_0.dat'
                    readFile(filename2)
                print()
            print()
        
    # T = int(rf.readline())
    # for _ in range(T):
    #     N, L = [int(j) for j in rf.readline().split()]