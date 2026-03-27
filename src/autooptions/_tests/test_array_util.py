import numpy as np
from autooptions.array_util import ArrayUtil


def testStripZeroRowsAndColumns():

    testData = np.array([
        [1, 0, 3],
        [0, 0, 0],
        [5, 0, 6]
    ])

    data, columns, rows = ArrayUtil.stripZeroRowsAndColumns(testData)
    assert data.shape == (2,2)
    assert data[0 ,0] == 1
    assert data[0, 1] == 3
    assert data[1, 0] == 5
    assert data[1, 1] == 6
    assert len(columns) == 2
    assert columns[0] == 0
    assert columns[1] == 2
    assert len(rows) == 2
    assert rows[0] == 0
    assert rows[1] == 2