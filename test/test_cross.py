import pytest
from rt import Vec3

def test_cross_one():
    v = Vec3( 3, 0, 2)
    w = Vec3(-1, 4, 2)

    expected = Vec3(-8, -8, 12)
    actual = v.cross(w)

    assert expected == actual

def test_cross_two():
    v = Vec3(1,  3, -5)
    w = Vec3(4, -2, -1)

    expected = Vec3(-13, -19, -14)
    actual = v.cross(w)

    assert expected == actual

def test_cross_three():
    v = Vec3(0, 3, -7)
    w = Vec3(2, 3,  1)

    expected = Vec3(24, -14, -6)
    actual = v.cross(w)

    assert expected == actual
