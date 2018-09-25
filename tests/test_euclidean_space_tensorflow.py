"""
Unit tests for Euclidean Space for tensorflow backend.
"""

import importlib
import numpy as np
import os
import tensorflow as tf

import geomstats.backend as gs
import tests.helper as helper

from geomstats.euclidean_space import EuclideanSpace


class TestEuclideanSpaceMethodsTensorFlow(tf.test.TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        gs.random.seed(1234)

        self.dimension = 2
        self.space = EuclideanSpace(self.dimension)
        self.metric = self.space.metric

        self.n_samples = 3

    @classmethod
    def setUpClass(cls):
        os.environ['GEOMSTATS_BACKEND'] = 'tensorflow'
        importlib.reload(gs)

    @classmethod
    def tearDownClass(cls):
        os.environ['GEOMSTATS_BACKEND'] = 'numpy'
        importlib.reload(gs)

    def test_belongs(self):
        point = self.space.random_uniform()
        belongs = self.space.belongs(point)
        expected = tf.convert_to_tensor([[True]])

        with self.test_session():
            self.assertAllClose(gs.eval(belongs), gs.eval(expected))

    def test_random_uniform(self):
        point = self.space.random_uniform()
        point_numpy = np.random.uniform(size=(1, self.dimension))

        with self.test_session():
            self.assertShapeEqual(point_numpy, point)

    def test_inner_product_matrix(self):
        result = self.metric.inner_product_matrix()

        expected = gs.eye(self.dimension)
        expected = helper.to_matrix(expected)

        with self.test_session():
            self.assertAllClose(gs.eval(result), gs.eval(expected))

    def test_inner_product(self):
        point_a = tf.convert_to_tensor([0., 1.])
        point_b = tf.convert_to_tensor([2., 10.])

        result = self.metric.inner_product(point_a, point_b)
        expected = gs.dot(point_a, point_b)
        expected = helper.to_scalar(expected)

        with self.test_session():
            self.assertAllClose(gs.eval(result), gs.eval(expected))

    def test_inner_product_vectorization(self):
        n_samples = 3

        one_point_a = tf.convert_to_tensor([0., 1.])
        one_point_b = tf.convert_to_tensor([2., 10.])

        n_points_a = tf.convert_to_tensor([
            [2., 1.],
            [-2., -4.],
            [-5., 1.]])
        n_points_b = tf.convert_to_tensor([
            [2., 10.],
            [8., -1.],
            [-3., 6.]])

        result = self.metric.inner_product(one_point_a, one_point_b)
        expected = gs.dot(one_point_a, gs.transpose(one_point_b))
        expected = helper.to_scalar(expected)
        with self.test_session():
            self.assertAllClose(gs.eval(result), gs.eval(expected))

        result = self.metric.inner_product(n_points_a, one_point_b)
        point_numpy = np.random.uniform(size=(n_samples, 1))
        with self.test_session():
            self.assertShapeEqual(point_numpy, result)

        result = self.metric.inner_product(one_point_a, n_points_b)
        point_numpy = np.random.uniform(size=(n_samples, 1))
        with self.test_session():
            self.assertShapeEqual(point_numpy, result)

        result = self.metric.inner_product(n_points_a, n_points_b)
        point_numpy = np.random.uniform(size=(n_samples, 1))
        with self.test_session():
            self.assertShapeEqual(point_numpy, result)


if __name__ == '__main__':
        tf.test.main()
