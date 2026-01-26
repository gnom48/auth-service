import os
import inspect


class BaseConfig:
    def __init__(self):
        self._topic_name = self.__class__.__name__.replace("Config", "")
        self.init()

    def init(self):
        """
        Автоматически присваиваем значения полям класса из переменных окружения,
        учитывая указанный тип атрибута.
        """
        attributes = inspect.getmembers(
            self, lambda a: not inspect.isroutine(a))
        for attr_name, current_value in attributes:
            env_value = os.getenv(attr_name.upper())
            if env_value is not None:
                expected_type = type(current_value)

                if expected_type == int:
                    converted_value = int(env_value)
                elif expected_type == bool:
                    converted_value = env_value.upper() == "TRUE"
                else:
                    converted_value = env_value

                setattr(self, attr_name, converted_value)

    def __repr__(self):
        attrs = ', '.join([f"{k}={v}" for k, v in vars(self).items()])
        return f"<AppConfig({attrs})>"

    def __str__(self):
        return self.__repr__()
