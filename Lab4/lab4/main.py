import numpy as np

def normalize_data(train_data, test_data, type = None):
    if type == 'standard':
        mean_train = np.mean(train_data, axis = 0)
        std_train = np.std(train_data, axis = 0)

        scaled_train_data = (train_data - mean_train) / std_train
        scaled_test_data = (test_data - mean_train) / std_train

    elif type == 'l1':
        norm_train = np.linalg.norm(train_data, ord = 1)
        scaled_train_data = train_data / norm_train
        norm_test = np.linalg.norm(test_data, ord = 1)
        scaled_test_data = test_data / norm_test
    elif type == 'l2':
        norm_train = np.linalg.norm(train_data, ord=2)
        scaled_train_data = train_data / norm_train
        norm_test = np.linalg.norm(test_data, ord=2)
        scaled_test_data = test_data / norm_test
    else:
        raise Exception("type not found")
    return train_data, test_data


class BagOfWords:
    def __init__(self):
        self.vocabulary = {}  # word: id
        self.voc_len = 0
        self.words = []

    def build_vocabulary(self, data):
        for sentence in data:
            for word in sentence:
                if word not in self.vocabulary:
                    self.vocabulary[word] = len(self.vocabulary)
                    self.words.append(word)
            self.voc_len = len(self.vocabulary)

    def get_features(self, data):
        features = np.zeros((len(data), self.voc_len))

        for id_sen, sentence in enumerate(data):
            for word in sentence:
                if word in self.vocabulary:
                    features[id_sen, self.vocabulary[word]] += 1
        return features

train_sentences = np.load("data/training_sentences.npy", allow_pickle=True)
train_labels = np.load("data/training_labels.npy", allow_pickle=True)

test_sentences = np.load("data/test_sentences.npy", allow_pickle=True)
test_labels = np.load("data/test_labels.npy", allow_pickle=True)

bagOfWords = BagOfWords()
bagOfWords.build_vocabulary(train_sentences)
print(bagOfWords.voc_len)

train_features = bagOfWords.get_features(train_sentences)
test_features = bagOfWords.get_features(train_sentences)

train_features_norm, test_features_norm = normalize_data(train_features, test_features, type='l2')

from sklearn import svm

svm_model = svm.SVC(C=1, kernel='linear')
svm_model.fit(train_features_norm, train_labels)