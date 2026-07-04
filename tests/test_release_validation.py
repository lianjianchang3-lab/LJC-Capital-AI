from core.validation import DataIntegrityValidator, ReleaseValidationCenter


def test_data_integrity_validator():
    result = DataIntegrityValidator().validate()
    assert "pass" in result
    assert "checks" in result


def test_release_validation_center():
    result = ReleaseValidationCenter().validate()
    assert "overall" in result
    assert "checks" in result
