# confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

classes = ['Fault 1', 'Fault 2', 'Fault 3', 'Fault 4', 'Fault 5', 'Fault 6']
confusion_matrix = np.array(
    [(0.883, 0.017, 0.1, 0, 0, 0), (0, 0.966, 0.017, 0, 0.017, 0), (0.017, 0, 0.966, 0.017, 0, 0),
     (0, 0, 0.067, 0.933, 0, 0), (0, 0, 0, 0.017, 0.983, 0), (0, 0, 0, 0, 0, 1)], dtype=np.float64)

plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
# plt.title('confusion_matrix')
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=-25)
plt.yticks(tick_marks, classes)

thresh = confusion_matrix.max() / 2.
# iters = [[i,j] for i in range(len(classes)) for j in range((classes))]
# ij配对，遍历矩阵迭代器
iters = np.reshape([[[i, j] for j in range(6)] for i in range(6)], (confusion_matrix.size, 2))
for i, j in iters:
    plt.text(j, i, format(confusion_matrix[i, j]), horizontalalignment="center",
             color='white' if confusion_matrix[i, j] > thresh else 'black')  # 显示对应的数字

plt.ylabel('Real label')
plt.xlabel('Prediction label')
plt.tight_layout()
plt.show()
