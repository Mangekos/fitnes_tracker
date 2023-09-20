from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str = ' '
    duration: float = 0
    distance: float = 0
    speed: float = 0
    calories: float = 0

    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Подготовить вывод сообщения о тренировках"""

        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM: ClassVar[int] = 1000  # Количество м в км
    M_IN_HR: ClassVar[int] = 60  # Количество минут в часе
    LEN_STEP: ClassVar[float] = 0.65  # Ширина шага

    action: int
    duration: float
    weight: float

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

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    RUN_MULTIPLIER: ClassVar[int] = 18  # Множитель скорости
    RUN_SHIFT: ClassVar[float] = 1.79  # Смещение для значения средней скорости

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.RUN_MULTIPLIER
                * self.get_mean_speed()
                + self.RUN_SHIFT)
                * self.weight
                / self.M_IN_KM
                * (self.duration
                   * self.M_IN_HR))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALK_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035  # Множитель веса человека
    WALK_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    """ WALK_SPEED_HEIGHT_MULTIPLIER -
    Множитель деления квадрата скорости и роста человека"""

    SPEED_IN_M_S: ClassVar[float] = 0.278  # Для перeвода скорости в м/с
    SM_IN_M: ClassVar[int] = 100  # Для перевода роста в метры

    height: int

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
                * self.M_IN_HR))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38  # Длина гребка спортсмена
    SWM_SHIFT: ClassVar[float] = 1.1  # Смещение для значения средней скорости
    SWM_MULTIPLIER: ClassVar[float] = 2  # Множитель скорости

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
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
    except (KeyError, TypeError) as e:
        print('Не верный тип тренировки', e)


def main(training: Training) -> 0:
    """Главная функция."""
    try:
        info: InfoMessage = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        raise NotImplementedError('Ошибка, введены не верные данные')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
        training = read_package(workout_type, data)
        main(training)
