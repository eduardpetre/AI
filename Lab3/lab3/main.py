import numpy as np
from matplotlib import pyplot as plt

train_images = np.loadtxt('./data/train_images.txt')
train_labels = np.int32(np.loadtxt('./data/train_labels.txt'))

test_images = np.loadtxt('./data/test_images.txt')
test_labels = np.int32(np.loadtxt('./data/test_labels.txt'))

class KnnClasifier:
    # 1.

    # constructor
    def __init__(self, train_images, train_labels):
        self.train_images = train_images
        self.train_labels = train_labels

    # 2.
    def classify_image(self, test_image, num_neighbors = 3, metric = "l2"):
        # distanta
        if metric.lower () == 'l2':
            dist = np.sqrt(np.sum(((self.train_images - test_image) ** 2), axis = 1))
        elif metric.lower() == 'l1':
            dist = np.sum(np.abs(self.train_images - test_image), axis = 1)

        # sortam dupa dist si pastram doar index ul
        sorted_idx = dist.argsort()

        # pastram doar primii k vecini
        sorted_idx = sorted_idx[:num_neighbors]

        # etichetele primilor k vecini
        labels = self.train_labels[sorted_idx]

        # afisam clasa cea mai apropiata
        return np.bincount(labels).argmax()

    # 3.

    # aplicarea clasificarii imaginilor
    def classify_images(self, test_images, num_neighbors = 3, metric = 'l2'):
        predicted_labels = [self.classify_image(test_img, num_neighbors, metric) for test_img in test_images]
        return np.array(predicted_labels)

def accuracy_score(labels, predicted_labels):
    return np.mean(labels == predicted_labels)

obj = KnnClasifier(train_images, train_labels)
predictions = obj.classify_images(test_images)

accuracy = accuracy_score(test_labels, predictions)
print(f"Accuracy: {accuracy}")

# 4.

# a)
accuracyL2 = []
for i in range(1, 10, 2):
    predicted_labels = obj.classify_images(test_images, num_neighbors = i, metric = 'l2')
    accuracyL2.append(accuracy_score(test_labels, predicted_labels))
accuracyL2

# b)
accuracyL1 = []
for i in range(1, 10, 2):
    predicted_labels = obj.classify_images(test_images, num_neighbors = i, metric = 'l1')
    accuracyL1.append(accuracy_score(test_labels, predicted_labels))
accuracyL1

plt.plot([1,3,5,7,9], accuracyL1)
plt.show()

plt.plot([1,3,5,7,9], accuracyL2)
plt.show()

plt.plot([1,3,5,7,9], accuracyL1)
plt.plot([1,3,5,7,9], accuracyL2)
plt.show()