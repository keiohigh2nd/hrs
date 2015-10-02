import numpy as np

data = np.loadtxt("../input_data/for_program_bp_cre_basic_data.csv",delimiter=",").astype(np.float32)
pdata = np.random.permutation(data)
T = np.hsplit(pdata, [5])

N = 400
x_train, x_test = np.split(T[0],   [N])
y_train, y_test = np.split(T[1], [N])

print y_train

