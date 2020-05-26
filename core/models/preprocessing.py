import numpy as np
from sklearn import preprocessing
from sklearn.impute import SimpleImputer


class DataStrategy:
    def fit(self, data_to_fit) -> 'DataStrategy':
        raise NotImplementedError()

    def apply(self, data):
        raise NotImplementedError()


class Scaling(DataStrategy):
    def __init__(self):
        self.default = DefaultStrategy()
        self.scaler = preprocessing.StandardScaler()

    def fit(self, data_to_fit):
        self.default.fit(data_to_fit)
        data_to_fit = self.default.apply(data_to_fit)
        self.scaler.fit(data_to_fit)
        return self

    def apply(self, data):
        data = self.default.apply(data)
        resulted = self.scaler.transform(data)
        return resulted


class Normalization(DataStrategy):
    def __init__(self):
        self.default = DefaultStrategy()

    def fit(self, data_to_fit):
        self.default.fit(data_to_fit)
        return self

    def apply(self, data):
        modified = self.default.apply(data)
        resulted = preprocessing.normalize(modified)

        return resulted


class DefaultStrategy(DataStrategy):
    def __init__(self):
        self.imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

    def fit(self, data_to_fit):
        self.imputer.fit(data_to_fit)
        return self

    def apply(self, data):
        modified = self.imputer.transform(data)
        return modified

class TsScalingStrategy(DataStrategy):
    def __init__(self):
        self.scaling = Scaling()
    
    def fit(self, data_to_fit):
        # Make from (n, timestamps, features) input the (n, features)
        self.scaling.fit(data_to_fit[:, 0])
        return self

    def apply(self, data):
        # Make (n * timestamps, features) from (n, timestamps, features)
        # So each feature scaled separatedly
        temp = data.reshape(-1, data.shape[-1])
        scaled = self.scaling.apply(temp)
        resulted = scaled.reshape(data.shape)
        return resulted
