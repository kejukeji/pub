# coding: utf-8

import jsonpickle

pickler = jsonpickle.pickler.Pickler(unpicklable=False, max_depth=2)