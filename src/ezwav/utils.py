from typing import Sequence, List, Tuple, Union
import warnings

Number = Union[int, float]

def normalize(
    values: Sequence[Number], 
    norm_range: Tuple[Number, Number]=[0,1], 
    scale: Number=1
    ) -> List[Number]:
    """
    Normalize a sequence of audio sample values to a specified range and scale.

    Parameters
    ----------
    values : Sequence[Number]
        The input audio samples to normalize.
    norm_range : tuple of two Numbers, optional
        Target range (low, high) to normalize the samples to. Default is (0, 1).
    scale : Number, optional
        A scaling factor applied after normalization. Default is 1.

    Returns
    -------
    List[Number]
        Normalized and scaled audio samples.

    Examples
    --------
    Normalize audio samples between 0 and 1:

    >>> normalize([0, 128, 255])
    [0.0, 0.5019607843137255, 1.0]

    Normalize audio samples to range [0, 100]:

    >>> normalize([0, 128, 255], norm_range=(0, 100))
    [0.0, 50.19607843137255, 100.0]

    Normalize audio samples to range [0, 100] and scale by 2:

    >>> normalize([0, 128, 255], norm_range=(0, 100), scale=2)
    [0.0, 100.3921568627451, 200.0]
    """
    # Sort range in case of backward user input
    low, high = sorted(norm_range)

    maximum = max(values)
    minimum = min(values)

    # Avoid division by zero
    if maximum == minimum:
        warnings.warn("All values are equal; returning constant normalized values.", UserWarning)
        return [low for _ in values]
    
    return [
        low + ((_ - minimum) / (maximum - minimum)) * (high - low) * scale
        for _ in values
    ]