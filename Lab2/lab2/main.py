# 1.
data = [(160, "F"), (165, "F"), (155, "F"), (172, "F"), (175, "B"), (180, "B"), (177, "B"), (190, "B")];
intervals = [(150, 160), (161, 170), (171, 180), (181, 190)];

date_modificate = []
for d in data:
    for i,interval in enumerate(intervals):
        if interval[0] <= d[0] <= interval[1]:
            date_modificate.append((i, d[1]))
            break
print(date_modificate)
# ...

# 2.

import numpy as np
import matplotlib.pyplot as plt

train_images = np.loadtxt('data/train_images.txt') # incarcam imaginile
train_labels = np.loadtxt('data/train_labels.txt').astype(np.uint8) # incarcam etichetele avand tipul de date int
image = train_images[0, :] # prima imagine
image = np.reshape(image, (28, 28))
plt.imshow(image.astype(np.uint8), cmap='gray')
plt.show()

test_images = np.loadtxt('data/test_images.txt') # incarcam imaginile
test_labels = np.loadtxt('data/test_labels.txt').astype(np.uint8)# incarcam etichetele avand tipul de date int
image = test_images[0, :] # prima imagine
image = np.reshape(image, (28, 28))

def values_to_bins(x, bins):
    x = np.digitize(x, bins)
    return x-1

bins = np.linspace(0, 255 + 1, 4 + 1) # start, stop, num
x_train = values_to_bins(train_images, bins)
x_test = values_to_bins(test_images, bins)

# 3.
from sklearn.naive_bayes import MultinomialNB

naive_bayes_model = MultinomialNB()
naive_bayes_model.fit(x_train, train_labels)
naive_bayes_model.predict(x_test)
print(naive_bayes_model.score(x_test, test_labels))

# 4.
num_bins = [3,5,7,9,11]
for bin in num_bins:
    bins = np.linspace(0,256, bin)
    x_train = values_to_bins(train_images, bins)
    x_test = values_to_bins(test_images, bins)
    naive_bayes_model = MultinomialNB()
    naive_bayes_model.fit(x_train, train_labels)
    naive_bayes_model.predict(x_test)
    print(naive_bayes_model.score(x_test, test_labels))

# 5.
bins = np.linspace(0, 256, 7)
x_train = values_to_bins(train_images, bins)
x_test = values_to_bins(test_images, bins)
naive_bayes_model = MultinomialNB()
naive_bayes_model.fit(x_train, train_labels)
pred = naive_bayes_model.predict(x_test)

wrong_samples = x_test [pred != test_labels]
wrong_pred = pred [pred != test_labels]

for i in range(10):
    image = wrong_samples[i, :]
    image = np.reshape(image, (28, 28))
    plt.imshow(image.astype(np.uint8), cmap = 'gray')
    plt.show()
    print(f"predicted {wrong_pred[i]}")