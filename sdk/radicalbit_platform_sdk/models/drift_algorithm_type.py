from enum import Enum


class DriftAlgorithmType(str, Enum):
    HELLINGER = 'HELLINGER'
    WASSERSTEIN = 'WASSERSTEIN'
    KS = 'KS'
    JS = 'JS'
    PSI = 'PSI'
    CHI2 = 'CHI2'
    KL = 'KULLBACK'
