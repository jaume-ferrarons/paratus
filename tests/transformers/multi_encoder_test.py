import timeit
import numpy as np
import pandas as pd

from paratus.transformers import MultiEncoder

data = pd.DataFrame(
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9]],
    columns=['a', 'b', 'c'])

data2 = pd.DataFrame(
    [["1", np.nan, 3], ["4", 5, 6], ["7", 8, 9], ["1", 5, 9]],
    columns=['a', 'b', 'c'])


def test_encode_one_column():
    model = MultiEncoder(['b'])

    transformed = model.fit_transform(data)

    assert (transformed.columns.values == [
        'a', 'c', 'b'
    ]).all()

    assert (transformed.values == np.array([
        [1, 3, 1],
        [4, 6, 2],
        [7, 9, 3],
        [1, 9, 2]
    ])).all()


def test_encode_two_columns():
    model = MultiEncoder(['b', 'a'])

    transformed = model.fit_transform(data)

    assert (transformed.columns.values == [
        'c', 'b', 'a'
    ]).all()

    assert (transformed.values == np.array([
        [3, 1, 1],
        [6, 2, 2],
        [9, 3, 3],
        [9, 2, 1]
    ])).all()


def test_encode_string():
    model = MultiEncoder(['a'])

    transformed = model.fit_transform(data2)

    assert (transformed.columns.values == [
        'b', 'c', 'a'
    ]).all()

    assert transformed.equals(
        pd.DataFrame(
            [
                [np.nan, 3, 1],
                [5, 6, 2],
                [8, 9, 3],
                [5, 9, 1]
            ],
            columns=['b', 'c', 'a']).astype(transformed.dtypes)
    )


def test_encode_missing_number():
    model = MultiEncoder(['b'])

    transformed = model.fit_transform(data2)

    assert (transformed.columns.values == [
        'a', 'c', 'b'
    ]).all()

    assert (transformed.equals(pd.DataFrame([
        ["1", 3, 0],
        ["4", 6, 1],
        ["7", 9, 2],
        ["1", 9, 1]
    ], columns=['a', 'c', 'b']).astype(transformed.dtypes)))


def test_transform_new_values():
    model = MultiEncoder(['b'])

    model.fit(data)
    transformed = model.transform(data2)

    assert (transformed.columns.values == [
        'a', 'c', 'b'
    ]).all()

    assert (transformed.equals(pd.DataFrame([
        ["1", 3, 0],
        ["4", 6, 2],
        ["7", 9, 3],
        ["1", 9, 2]
    ], columns=['a', 'c', 'b']).astype(transformed.dtypes)))


def test_encode_low_freq():
    model = MultiEncoder(['c'], min_frequency=2)

    transformed = model.fit_transform(data)

    assert (transformed.columns.values == [
        'a', 'b', 'c'
    ]).all()

    assert (transformed.values == np.array([
        [1, 2, -1],
        [4, 5, -1],
        [7, 8, 1],
        [1, 5, 1]
    ])).all()


def test_encode_to_int():
    model = MultiEncoder(['b'], as_category=False)

    transformed = model.fit_transform(data2)

    assert (transformed.columns.values == [
        'a', 'c', 'b'
    ]).all()

    assert (transformed.equals(pd.DataFrame([
        ["1", 3, 0],
        ["4", 6, 1],
        ["7", 9, 2],
        ["1", 9, 1]
    ], columns=['a', 'c', 'b'])))


def test_speed():
    dataset = np.random.randint(0, 1000, 100000)
    model = MultiEncoder(['c'], min_frequency=2)
    df = pd.DataFrame(np.transpose(dataset), columns=['c'])
    res = timeit.timeit(lambda: model.fit_transform(df), number=10)
    assert(res < 10)
