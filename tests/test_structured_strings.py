"""Test string kernels and utilities associated with them."""
import numpy as np
from sklearn_jax_kernels.structured.string_utils import (
    AsciiBytesTransformer, NGramTransformer)
from sklearn_jax_kernels import RBF
from sklearn_jax_kernels.structured.strings import (
    DistanceSpectrumKernel, SpectrumKernel)


class TestUtils:
    def test_ascii_bytes_transformer(self):
        strings = ['abc', 'def']
        transformer = AsciiBytesTransformer()
        trans = transformer.transform(strings)
        inverse = transformer.inverse_transform(trans)
        assert all([s1 == s2 for s1, s2 in zip(strings, inverse)])


class TestKernels:
    def test_spectrum_kernel_example(self):
        strings = ['aabbcc', 'aaabac']
        strings_transformed = AsciiBytesTransformer().transform(strings)
        kernel = SpectrumKernel(n_gram_length=2)
        K = kernel(strings_transformed)
        assert np.allclose(K, np.array([[5., 3.], [3., 7.]]))

    def test_spectrum_kernel_ngram_transform(self):
        n_gram_length = 2
        strings = ['aabbcc', 'aaabac']
        strings_transformed = AsciiBytesTransformer().transform(strings)
        ngrams = NGramTransformer(n_gram_length).transform(strings_transformed)

        kernel_strings = SpectrumKernel(n_gram_length=n_gram_length)
        kernel_ngrams = SpectrumKernel(n_gram_length=None)
        K_strings = kernel_strings(strings_transformed)
        K_ngrams = kernel_ngrams(ngrams)
        assert np.allclose(K_strings, K_ngrams)

    def test_distance_spectrum_kernel_ngram_transform(self):
        n_gram_length = 2
        distance_kernel = RBF(1.0)
        strings = ['aabbcc', 'aaabac']
        strings_transformed = AsciiBytesTransformer().transform(strings)
        ngrams = NGramTransformer(n_gram_length).transform(strings_transformed)

        kernel_strings = DistanceSpectrumKernel(distance_kernel, n_gram_length)
        kernel_ngrams = DistanceSpectrumKernel(distance_kernel, None)
        K_strings = kernel_strings(strings_transformed)
        K_ngrams = kernel_ngrams(ngrams)
        assert np.allclose(K_strings, K_ngrams)

    def test_distance_spectrum_kernel(self):
        distance_kernel = RBF(1.0)
        strings = ['aabbcc', 'aaabac']
        strings_transformed = AsciiBytesTransformer().transform(strings)
        kernel = DistanceSpectrumKernel(distance_kernel, 2)
        K = kernel(strings_transformed)
        K_gt = np.array([
             [5.,        2.2130613],
             [2.2130613, 6.2130613]
        ])
        assert np.allclose(K, K_gt)