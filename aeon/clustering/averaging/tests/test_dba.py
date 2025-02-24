"""Tests for DBA."""

import numpy as np
import pytest

from aeon.clustering.averaging import elastic_barycenter_average
from aeon.distances.tests.test_utils import _create_test_distance_numpy
from aeon.testing.test_config import PR_TESTING

expected_dba = np.array(
    [
        [
            0.01351105,
            -0.08112161,
            0.04063662,
            -0.06867308,
            -0.13887883,
            -0.34044035,
            0.22315302,
            -0.16004842,
            0.20959644,
            0.16023767,
        ],
        [
            -0.030493,
            0.16787085,
            -0.01794528,
            -0.15615568,
            0.18888089,
            0.02650418,
            0.03522746,
            -0.02563329,
            0.09055917,
            -0.11046538,
        ],
        [
            0.12595717,
            -0.03616803,
            0.28522336,
            0.1962002,
            -0.05161538,
            0.27548387,
            0.10042834,
            -0.01536394,
            -0.13741457,
            0.07508204,
        ],
        [
            0.23330467,
            0.23283218,
            -0.17851012,
            0.07599822,
            0.0644743,
            -0.22862958,
            -0.05794768,
            -0.16609387,
            -0.1236426,
            -0.10906081,
        ],
        [
            0.16857703,
            -0.24448901,
            0.08663198,
            0.00258875,
            0.01033525,
            -0.29918156,
            -0.05027093,
            0.14333835,
            0.21959808,
            -0.07099129,
        ],
        [
            0.11509088,
            0.12175909,
            -0.15255715,
            0.37132895,
            -0.03063229,
            -0.00922786,
            0.2053414,
            0.10990122,
            -0.10940058,
            -0.11656546,
        ],
        [
            -0.06796261,
            -0.09069732,
            -0.01097365,
            -0.14447324,
            -0.2444549,
            0.32982661,
            0.32280882,
            -0.04148224,
            0.30133403,
            -0.32354776,
        ],
        [
            -0.10985453,
            0.20238667,
            0.47766167,
            -0.0645197,
            0.16300204,
            -0.18033383,
            -0.18312481,
            0.01220449,
            -0.03722065,
            0.11640757,
        ],
        [
            0.07424704,
            -0.2824533,
            0.15604098,
            0.35578053,
            -0.06797368,
            -0.01689053,
            0.29127062,
            0.14293372,
            -0.02831629,
            -0.17414547,
        ],
        [
            -0.09329966,
            -0.0284073,
            0.23789267,
            -0.06377485,
            -0.01545654,
            0.09896634,
            -0.29903917,
            0.0294299,
            -0.13441741,
            0.18484228,
        ],
    ]
)


@pytest.mark.skipif(
    PR_TESTING,
    reason="Only run on overnights because its very slow",
)
def test_dba():
    """Test dba functionality."""
    X_train = _create_test_distance_numpy(10, 10, 10)

    average_ts = elastic_barycenter_average(X_train)

    assert isinstance(average_ts, np.ndarray)
    assert average_ts.shape == X_train[0].shape
    assert np.allclose(average_ts, expected_dba)


@pytest.mark.skipif(
    PR_TESTING,
    reason="Only run on overnights because its very slow",
)
@pytest.mark.parametrize(
    "distance",
    [
        "dtw",
        "ddtw",
        "wdtw",
        "wddtw",
        "erp",
        "edr",
        "twe",
        "msm",
        "shape_dtw",
        "adtw",
    ],
)
def test_elastic_dba_variations(distance):
    """Test dba functionality with different distance measures."""
    X_train = _create_test_distance_numpy(4, 2, 10)

    average_ts = elastic_barycenter_average(
        X_train, distance=distance, window=0.2, independent=False
    )

    assert isinstance(average_ts, np.ndarray)
    assert average_ts.shape == X_train[0].shape
