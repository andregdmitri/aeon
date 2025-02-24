"""Matrix Profile classifier.

Pipeline classifier using the Matrix Profile transformer and an estimator.
"""

__maintainer__ = []
__all__ = ["MatrixProfileClassifier"]

import numpy as np
from deprecated.sphinx import deprecated
from sklearn.neighbors import KNeighborsClassifier

from aeon.base._base import _clone_estimator
from aeon.classification.base import BaseClassifier
from aeon.transformations.collection.matrix_profile import MatrixProfile


# TODO: remove in v0.8.0
@deprecated(
    version="0.7.0",
    reason="MatrixProfileClassifier will be removed in v0.8.0.",
    category=FutureWarning,
)
class MatrixProfileClassifier(BaseClassifier):
    """
    Matrix Profile (MP) classifier.

    This classifier simply transforms the input data using the MatrixProfile [1]_
    transformer and builds a provided estimator using the transformed data.

    Parameters
    ----------
    subsequence_length : int, default=10
        The subsequence length for the MatrixProfile transformer.
    estimator : sklearn classifier, default=None
        An sklearn estimator to be built using the transformed data. Defaults to a
        1-nearest neighbour classifier.
    n_jobs : int, default=1
        The number of jobs to run in parallel for both `fit` and `predict`.
        ``-1`` means using all processors. Currently available for the classifier
        portion only.
    random_state : int or None, default=None
        Seed for random, integer.

    Attributes
    ----------
    n_classes_ : int
        Number of classes. Extracted from the data.
    classes_ : ndarray of shape (n_classes_)
        Holds the label for each class.

    See Also
    --------
    MatrixProfile
        MatrixProfile transformer.

    References
    ----------
    .. [1] Yeh, Chin-Chia Michael, et al. "Time series joins, motifs, discords and
        shapelets: a unifying view that exploits the matrix profile." Data Mining and
        Knowledge Discovery 32.1 (2018): 83-123.
        https://link.springer.com/article/10.1007/s10618-017-0519-9

    Examples
    --------
    >>> from aeon.classification.feature_based import MatrixProfileClassifier
    >>> from aeon.datasets import load_unit_test
    >>> X_train, y_train = load_unit_test(split="train", return_X_y=True)
    >>> X_test, y_test = load_unit_test(split="test", return_X_y=True)
    >>> clf = MatrixProfileClassifier()
    >>> clf.fit(X_train, y_train)
    MatrixProfileClassifier(...)
    >>> y_pred = clf.predict(X_test)
    """

    _tags = {
        "capability:multithreading": True,
        "algorithm_type": "distance",
    }

    def __init__(
        self,
        subsequence_length=10,
        estimator=None,
        n_jobs=1,
        random_state=None,
    ):
        self.subsequence_length = subsequence_length
        self.estimator = estimator

        self.n_jobs = n_jobs
        self.random_state = random_state

        self._transformer = None
        self._estimator = None

        super().__init__()

    def _fit(self, X, y):
        """Fit a pipeline on cases (X,y), where y is the target variable.

        Parameters
        ----------
        X : 3D np.ndarray
            The training data shape = (n_instances, n_channels, n_timepoints).
        y : 1D np.ndarray
            The training labels, shape = (n_instances).

        Returns
        -------
        self :
            Reference to self.

        Notes
        -----
        Changes state by creating a fitted model that updates attributes
        ending in "_" and sets is_fitted flag to True.
        """
        self._transformer = MatrixProfile(m=self.subsequence_length)
        self._estimator = _clone_estimator(
            (
                KNeighborsClassifier(n_neighbors=1)
                if self.estimator is None
                else self.estimator
            ),
            self.random_state,
        )

        m = getattr(self._estimator, "n_jobs", None)
        if m is not None:
            self._estimator.n_jobs = self._n_jobs

        X_t = self._transformer.fit_transform(X, y)
        self._estimator.fit(X_t, y)

        return self

    def _predict(self, X) -> np.ndarray:
        """Predict class values of n instances in X.

        Parameters
        ----------
        X : 3D np.ndarray
            The data to make predictions for, shape = (n_instances, n_channels,
            n_timepoints).

        Returns
        -------
        y : 1D np.ndarray
            The predicted class labels, shape = (n_instances).
        """
        return self._estimator.predict(self._transformer.transform(X))

    def _predict_proba(self, X) -> np.ndarray:
        """Predict class probabilities for n instances in X.

        Parameters
        ----------
        X : 3D np.ndarray
            The data to make predictions for, shape = (n_instances, n_channels,
            n_timepoints).

        Returns
        -------
        y : 2D np.ndarray
            Predicted probabilities using the ordering in classes_ shape = (
            n_instances, n_classes_).
        """
        m = getattr(self._estimator, "predict_proba", None)
        if callable(m):
            return self._estimator.predict_proba(self._transformer.transform(X))
        else:
            dists = np.zeros((X.shape[0], self.n_classes_))
            preds = self._estimator.predict(self._transformer.transform(X))
            for i in range(0, X.shape[0]):
                dists[i, self._class_dictionary[preds[i]]] = 1
            return dists

    @classmethod
    def get_test_params(cls, parameter_set="default"):
        """Return testing parameter settings for the estimator.

        Parameters
        ----------
        parameter_set : str, default="default"
            Name of the set of test parameters to return, for use in tests. If no
            special parameters are defined for a value, will return `"default"` set.

        Returns
        -------
        params : dict or list of dict, default={}
            Parameters to create testing instances of the class.
            Each dict are parameters to construct an "interesting" test instance, i.e.,
            `MyClass(**params)` or `MyClass(**params[i])` creates a valid test instance.
            `create_test_instance` uses the first (or only) dictionary in `params`.
        """
        return {"subsequence_length": 4}
