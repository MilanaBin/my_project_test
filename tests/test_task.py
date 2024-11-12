from src.my_project_test.task import add_nums, mult_nums


def test_add_nums():
    assert add_nums(1, 2) == 3


def test_mult_nums():
    assert mult_nums(1, 20) == 20
    assert mult_nums(2, 2) == 4


if __name__ == "__main__":
    test_add_nums()
    test_mult_nums()
