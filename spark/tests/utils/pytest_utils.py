import uuid

from _pytest.python_api import ApproxMapping
import pytest

prefix_id = str(uuid.uuid4())


def my_approx(expected, rel=None, abs=None, nan_ok=True):
    """Source: https://stackoverflow.com/questions/56046524/check-if-python-dictionaries-are-equal-allowing-small-difference-for-floats"""

    # TODO Implement a way to be used with list of nested dict
    from collections.abc import Mapping

    if isinstance(expected, Mapping):
        return ApproxNestedMapping(expected, rel, abs, nan_ok)
    return pytest.approx(expected, rel, abs, nan_ok)


class ApproxNestedMapping(ApproxMapping):
    """Source: https://stackoverflow.com/questions/56046524/check-if-python-dictionaries-are-equal-allowing-small-difference-for-floats"""

    # TODO Implement a way to be used with list of nested dict
    def _yield_comparisons(self, actual):
        for k in self.expected:
            if isinstance(actual[k], type(self.expected)):
                gen = ApproxNestedMapping(
                    self.expected[k], rel=self.rel, abs=self.abs, nan_ok=self.nan_ok
                )._yield_comparisons(actual[k])
                yield from gen
                for el in gen:
                    y = el
                    yield y
            else:
                yield actual[k], self.expected[k]

    def _check_type(self):
        for value in self.expected.values():
            if not isinstance(value, type(self.expected)):
                super()._check_type()
