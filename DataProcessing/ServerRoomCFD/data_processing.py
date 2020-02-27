import numpy as np

modes = [['24C', '27C', '30C'], \
         ['50perc', '75perc', '100perc'], \
         ['rack1', 'rack2']]
racks = [[10, 20, 22, 24, 28, 30, 34, 36], \
         [13, 18, 22, 24, 28, 30]]

wf = None
nonzeros = 0
dimensions = [0, 0, 0, 0]
entries = {}

def readAirCon(i, j, k, filename):
    global wf, nonzeros, dimensions, entries
    with open(filename, mode='r') as rf:
        for _, line in enumerate(rf):
            if line[0] == '#':
                continue
            time, T = [float(t) for t in line.split(' ')]
            time = int(time + 0.5)
            idx = (i+1, j+1, k+1, time)
            entry = '{0[0]}\t{0[1]}\t{0[2]}\t{0[3]}\t{1}\n'.format(idx, T)
            # wf.write(entry)
            entries[idx] = entry
            nonzeros = nonzeros + 1
            dimensions = np.maximum(dimensions, idx)
    print(filename, '...done!')
    rf.close()

def readProbe(i, j, filename):
    global wf, nonzeros, dimensions, entries
    with open(filename, mode='r') as rf:
        for _, line in enumerate(rf):
            if line[0] == '#':
                continue
            T = [float(t) for t in line.split()]
            time = int(T[0] + 0.5)
            for k in range(4):
                idx = (i+1, j+1, k+3, time)
                entry = '{0[0]}\t{0[1]}\t{0[2]}\t{0[3]}\t{1}\n'.format(idx, T[k+1])
                # wf.write(entry)
                entries[idx] = entry
                nonzeros = nonzeros + 1
                dimensions = np.maximum(dimensions, idx)
    print(filename, '...done!')
    rf.close()

def readRack(i, j, k, filename):
    global wf, nonzeros, dimensions, entries
    with open(filename, mode='r') as rf:
        for _, line in enumerate(rf):
            if line[0] == '#':
                continue
            time, T = [float(t) for t in line.split('\t')]
            time = int(time + 0.5)
            idx = (i+1, j+1, k+1, time)
            entry = '{0[0]}\t{0[1]}\t{0[2]}\t{0[3]}\t{1}\n'.format(idx, T)
            # wf.write(entry)
            entries[idx] = entry
            nonzeros = nonzeros + 1
            dimensions = np.maximum(dimensions, idx)
    print(filename, '...done!')
    rf.close()

if __name__ == '__main__':
    wf = open('ServerRoomCFD.tensor', mode='w')
    for i in range(len(modes[0])):
        for j in range(len(modes[1])):
            filename = modes[0][i] + '/' + modes[1][j] + '/aircon_Inlet.dat'
            readAirCon(i, j, 0, filename)
            filename = modes[0][i] + '/' + modes[1][j] + '/aircon_Outlet.dat'
            readAirCon(i, j, 1, filename)
            filename = modes[0][i] + '/' + modes[1][j] + '/probes.dat'
            readProbe(i, j, filename)
            for k in range(len(modes[2])):
                filename = modes[0][i] + '/' + modes[1][j] + '/' + modes[2][k]
                for l in range(len(racks[k])):
                    filename1 = filename + '/' + str(racks[k][l]) + '_Inlet_0.dat'
                    readRack(i, j, 6+(k*len(racks[0])+l)*2, filename1)
                    filename2 = filename + '/' + str(racks[k][l]) + '_Outlet_0.dat'
                    readRack(i, j, 6+(k*len(racks[0])+l)*2 + 1, filename2)
                print()
            print()
    print('dimensions', dimensions)
    print('nonzeros', nonzeros, end='\n')
    for entry in entries:
        # wf.write(entry)
        print(entry)
        input()
    wf.close()