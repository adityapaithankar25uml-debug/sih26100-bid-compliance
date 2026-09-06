from app.core.security import generate_ulid, is_valid_ulid


def test_ulid_generation_and_validation():
    ulid_str = generate_ulid()
    assert len(ulid_str) == 26
    assert is_valid_ulid(ulid_str) is True


def test_ulid_invalid_strings():
    assert is_valid_ulid("") is False
    assert is_valid_ulid("12345") is False
    assert is_valid_ulid("01ARZ3NDEKTSV4RRFFQ69G5FA12") is False  # 27 chars
    assert is_valid_ulid("01ARZ3NDEKTSV4RRFFQ69G5FA!") is False  # Invalid symbol
