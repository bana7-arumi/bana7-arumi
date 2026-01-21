from scripts.main import ReadmeMd, Resident, read_resident_json, update_readme


def test_read_resident_json() -> None:
    # Arrange
    expected_residents: list[Resident] = [
        Resident(name="aya", image_path="assets/th/aya.png"),
        Resident(name="daiyousei", image_path="assets/th/daiyousei.png"),
        Resident(name="hina", image_path="assets/th/hina.png"),
        Resident(name="nitori", image_path="assets/th/nitori.png"),
        Resident(name="rin", image_path="assets/th/rin.png"),
        Resident(name="suwako", image_path="assets/th/suwako.png"),
        Resident(name="yuyuko", image_path="assets/th/yuyuko.png"),
    ]

    # Act
    residents: list[Resident] = read_resident_json()

    # Assert
    assert residents == expected_residents


def test_update_todays_resident() -> None:
    # Arrange
    resident = Resident(image_path="test/path.png", name="test")
    content = (
        "hoge\n"
        f"{ReadmeMd.TODAYS_RESIDENT_START_TAG}\n"
        "fuga\n"
        f"{ReadmeMd.TODAYS_RESIDENT_END_TAG}\n"
        "piyo"
    )

    expected_content = (
        "hoge\n"
        f"{ReadmeMd.TODAYS_RESIDENT_START_TAG}\n"
        f"{
            ReadmeMd.TODAYS_RESIDENT_TEMPLATE.format(
                resident_image_path='test/path.png', resident_name='test'
            )
        }\n"
        f"{ReadmeMd.TODAYS_RESIDENT_END_TAG}\n"
        "piyo"
    )

    # Act
    readme = ReadmeMd(content=content)
    readme = readme.update_todays_resident(
        resident_image_path=resident.image_path, resident_name=resident.name
    )
    # Assert
    assert readme.content == expected_content


# --- Update Readme Test ---


def test_update_readme() -> None:
    # Act
    update_readme()
    # Assert
    # 目視で確認
