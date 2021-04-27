import os
import numpy as np


def duplicate_check(lb_file):
    # verify labels
    assert os.path.isfile(lb_file), "label file not found!!!"

    with open(lb_file, 'r') as f:
        l = [x.split() for x in f.read().strip().splitlines()]
        l = np.array(l, dtype=np.float32)
    if len(l):
        assert l.shape[1] == 5, 'labels require 5 columns each'
        assert (l >= 0).all(), 'negative labels'
        assert (l[:, 1:] <= 1).all(), 'non-normalized or out of bounds coordinate labels'
        if np.unique(l, axis=0).shape[0] == l.shape[0]:
            return True
    return False