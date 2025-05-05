from enum import Enum

from metrics.chi2 import Chi2Test
from metrics.hellinger_distance import HellingerDistance
from metrics.jensen_shannon_distance import JensenShannonDistance
from metrics.ks import KolmogorovSmirnovTest
from metrics.kullback_leibler_divergence import KullbackLeiblerDivergence
from metrics.psi import PSI
from metrics.wasserstein_distance import WassersteinDistance


class MapDriftEnumToClass(Enum):
    HELLINGER = HellingerDistance
    WASSERSTEIN = WassersteinDistance
    KS = KolmogorovSmirnovTest
    JS = JensenShannonDistance
    PSI = PSI
    CHI2 = Chi2Test
    KULLBACK = KullbackLeiblerDivergence

    @classmethod
    def get_calculator_class(cls, algo_type: str):
        try:
            return cls[algo_type].value
        except KeyError as exc:
            raise ValueError(
                f'No calculator class mapped for algorithm type: {algo_type}'
            ) from exc
