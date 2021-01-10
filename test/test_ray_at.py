import pytest
from rt import Vec3, Ray

def test_at_one():
    origin = Vec3(0, 0, 0)
    direction = Vec3(1, 2, 3)
    ray = Ray(origin, direction)

    expected = Vec3(10, 20, 30)
    actual = ray.at(10)

    assert expected == actual
