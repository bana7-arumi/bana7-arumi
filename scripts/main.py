import json
import re
import secrets
from typing import Any, ClassVar, Final

from pydantic import BaseModel


class Resident(BaseModel):
    name: Final[str]
    image_path: Final[str]


class ReadmeMd(BaseModel):
    TODAYS_RESIDENT_START_TAG: ClassVar[str] = "<!-- todays-resident-start -->"
    TODAYS_RESIDENT_END_TAG: ClassVar[str] = "<!-- todays-resident-end -->"
    TODAYS_RESIDENT_TEMPLATE: ClassVar[str] = (
        "<img src='{resident_image_path}' width='100px'>\n<p>{resident_name}</p>"
    )

    content: Final[str]

    def update_todays_resident(
        self, *, resident_image_path: str, resident_name: str
    ) -> "ReadmeMd":
        new_today_resident: str = self.TODAYS_RESIDENT_TEMPLATE.format(
            resident_image_path=resident_image_path,
            resident_name=resident_name,
        )
        pattern = re.compile(
            rf"({self.TODAYS_RESIDENT_START_TAG}).*?({self.TODAYS_RESIDENT_END_TAG})",
            re.DOTALL,
        )
        print(pattern)
        print(new_today_resident)
        print()
        new_content: str = pattern.sub(
            f"\\1\n{new_today_resident}\n\\2",
            self.content,
        )
        print(new_content)
        return ReadmeMd(content=new_content)


def read_resident_json() -> list[Resident]:
    with open("scripts/resident.json", encoding="utf-8") as f:
        residents: Any = json.load(f)
    return [Resident.model_validate(c) for c in residents]


def read_readme_md() -> ReadmeMd:
    with open("README.md", encoding="utf-8") as f:
        content: str = f.read()
    return ReadmeMd(content=content)


def write_readme_md(*, readme_md: ReadmeMd) -> None:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_md.content)


def update_readme() -> None:
    residents: list[Resident] = read_resident_json()
    readme_md: ReadmeMd = read_readme_md()

    choiced_resident: Resident = secrets.choice(residents)
    new_readme_md = readme_md.update_todays_resident(
        resident_image_path=choiced_resident.image_path,
        resident_name=choiced_resident.name,
    )

    write_readme_md(readme_md=new_readme_md)


if __name__ == "__main__":
    update_readme()
