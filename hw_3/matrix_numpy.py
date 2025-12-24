import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

class FileWriteMixin:
    def save(self, filepath):
        with open(filepath, 'w') as f:
            f.write(str(self))

class StringReprMixin:
    def __str__(self):
        return str(self.value)

class AccessorMixin:
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val

class Matrix(NDArrayOperatorsMixin, FileWriteMixin, StringReprMixin, AccessorMixin):
    def __init__(self, value):
        self._value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, int, float, list)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, Matrix) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.value if isinstance(x, Matrix) else x for x in out)

        result = getattr(ufunc, method)(*inputs, **kwargs)

        if method == 'at':
            return None

        return Matrix(result)

