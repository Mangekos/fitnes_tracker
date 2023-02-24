class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    M_IN_HR: int = 60
    LEN_STEP: float = 0.65

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CONSTANT_RUN_1: int = 18
    CONSTANT_RUN_2: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        cal_1: float = self.CONSTANT_RUN_1 * self.get_mean_speed()
        cal_2: float = self.weight / super().M_IN_KM
        cal_3: float = self.duration * super().M_IN_HR
        run_cal: float = (cal_1 + self.CONSTANT_RUN_2) * cal_2 * cal_3
        return run_cal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CONSTANT_WALK_1: float = 0.035
    CONSTANT_WALK_2: float = 0.029
    SPEED_IN_M_S: float = 0.278
    SM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        height_m: float = self.height / self.SM_IN_M
        avg_speed: float = self.get_mean_speed() * self.SPEED_IN_M_S
        walk_cal_1: float = self.CONSTANT_WALK_1 * self.weight
        walk_cal_2: float = avg_speed ** 2 / height_m
        walk_cal_3: float = walk_cal_2 * self.CONSTANT_WALK_2 * self.weight
        walk_cal: float = (walk_cal_1 + walk_cal_3) * (self.duration * super().
                                                       M_IN_HR)
        return walk_cal


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CONSTANT_SWIM_1: float = 1.1
    CONSTANT_SWIM_2 = 2
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        speed_1: float = self.length_pool * self.count_pool
        swim_speed: float = speed_1 / super().M_IN_KM / self.duration
        return swim_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        cal_1: float = self.get_mean_speed() + self.CONSTANT_SWIM_1
        cal_2: float = self.weight * self.duration
        swim_cal: float = cal_1 * self.CONSTANT_SWIM_2 * cal_2
        return swim_cal


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_class = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return training_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
