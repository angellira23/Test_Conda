import numpy as np
# A = [np.array([[1, 2, 3],[1, 2, 3],[1, 2, 3]]),np.array([[50,6,7],[5,6,7],[5,6,7]]),np.array([[7,8,9],[7,8,9],[7,8,9]])]

def stddeviation(lst):
    stddev = [i.std(axis=0) for i in lst]
    stddevmean = [i.mean(axis=0) for i in lst]
    return stddev
#
# stdds = stddeviation(A)
# print(stdds)
#
# stval = []
# for i in stdds:
#     stval.append(i[0])
#     val = np.mean(stval)
#     if i[0] > val:
#         stval.remove(i[0])
# print(stval)
# print(val)

B = [-0.00018522639543541676, -0.00018563119950627593, -0.00018824308033263615, -0.00018713327914705885, -0.00020031759770798335,1]

def stddeviation(lst):
    ref = np.mean(lst)
    for i in lst:
        if i > ref:
            lst.remove(i)
    return lst
bef = stddeviation(B)
print(bef)
