from src.my_project_test.task import add_nums


def test_add_nums():
    assert add_nums(1, 2) == 3


if __name__ == "__main__":
    test_add_nums()
