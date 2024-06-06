import copy

# See https://stackoverflow.com/a/70277752/4258693
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class UpdatableBaseModel(BaseModel):
    """BaseModel which can be updated partially.

    See https://stackoverflow.com/a/75451357/4258693

    """

    model_config = ConfigDict(validate_assignment=True)

    def update(self, **kwargs: Dict[str, Any]) -> None:
        """Update the model with multiple assignments."""
        self.__class__.validate(self.__dict__ | kwargs)
        self.__dict__.update(kwargs)

    @contextmanager
    def delay_validation(self) -> Iterator[None]:
        """Context manager which enables to direct reassign individual values.

        And have field- and model- validators to run as expected.

        Example:
        -------
        with myModel.delay_validation():
            myModel.a = 2
            myModel.b = 3

        """
        original_dict = copy.deepcopy(self.__dict__)

        self.__config__.validate_assignment = False  # type: ignore[attr-defined]
        try:
            yield
        finally:
            self.__config__.validate_assignment = True  # type: ignore[attr-defined]

        try:
            self.__class__.validate(self.__dict__)
        except:
            self.__dict__.update(original_dict)
            raise
