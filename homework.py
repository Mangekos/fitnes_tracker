class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_training_info(Training):
        pass

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    M_IN_HR = 60
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        return InfoMessage(training_type=self, duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.
                    get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) * self.
                    weight / super().M_IN_KM * (self.
                                                duration * super().M_IN_HR))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    SPEED_IN_M_S = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.
                 CALORIES_MEAN_SPEED_MULTIPLIER * self.
                 weight + ((self.SPEED_IN_M_S * self.
                           get_mean_speed()
                            ) ** 2 / (self.height / self.SM_IN_M)
                           ) * self.CALORIES_MEAN_SPEED_SHIFT * self.
                weight) * (self.duration * super().M_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.
                count_pool / super().M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.
                 CALORIES_MEAN_SPEED_MULTIPLIER) * self.
                CALORIES_MEAN_SPEED_SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_class = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    while True:
        train_cod: Training = training_class[workout_type](*data)
        return train_cod


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
