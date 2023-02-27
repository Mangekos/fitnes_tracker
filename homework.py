import dataclasses


@dataclasses.dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Подготовить вывод сообщения о тренировках"""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000  # Количество м в км
    M_IN_HR: int = 60  # Количество минут в часе
    LEN_STEP: float = 0.65  # Ширина шага

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(self.__class__.__name__ + '.do_something')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    RUN_MULTIPLIER: int = 18  # Множитель скорости
    RUN_SHIFT: float = 1.79  # Смещение для значения средней скорости

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.RUN_MULTIPLIER
                * self.get_mean_speed()
                + self.RUN_SHIFT)
                * self.weight
                / super().M_IN_KM
                * (self.duration
                   * super().M_IN_HR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALK_WEIGHT_MULTIPLIER: float = 0.035  # Множитель веса человека
    WALK_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    """ WALK_SPEED_HEIGHT_MULTIPLIER -
    Множитель деления квадрата скорости и роста человека"""

    SPEED_IN_M_S: float = 0.278  # Для перeвода скорости в м/с
    SM_IN_M: int = 100  # Для перевода роста в метры

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.WALK_WEIGHT_MULTIPLIER
                 * self.weight
                 + ((self.get_mean_speed()
                     * self.SPEED_IN_M_S) ** 2
                     / (self.height / self.SM_IN_M))
                * self.WALK_SPEED_HEIGHT_MULTIPLIER
                * self.weight)
                * (self.duration
                * super().M_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # Длина гребка спортсмена
    SWM_SHIFT: float = 1.1  # Смещение для значения средней скорости
    SWM_MULTIPLIER: float = 2  # Множитель скорости

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool
                * self.count_pool
                / super().M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed()
                 + self.SWM_SHIFT)
                * self.SWM_MULTIPLIER
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training_class: dict(str, Training) = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}
        return training_class[workout_type](*data)
    except KeyError:
        raise NotImplementedError('Не верный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info: InfoMessage = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        raise NotImplementedError('Ошибка, введены не верные данные')


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
