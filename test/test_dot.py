import pytest
from rt import Vec3

def test_dot_one():
    v = Vec3(3,  0, 2)
    w = Vec3(-1, 4, 2)
    assert 1 == v.dot(w)

def test_dot_two():
    v = Vec3(1,  3, -5)
    w = Vec3(4, -2, -1)
    assert 3 == v.dot(w)

def test_dot_three():
    v = Vec3(0, 3, -7)
    w = Vec3(2, 3,  1)
    assert 2 == v.dot(w)
