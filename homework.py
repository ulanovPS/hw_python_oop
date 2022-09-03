from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    """Можно записать одну строку в одну переменную"""
    LINE_OUTPUT = ("Тип тренировки: {}; "
                   "Длительность: {:.3f} ч.; "
                   "Дистанция: {:.3f} км; "
                   "Ср. скорость: {:.3f} км/ч; "
                   "Потрачено ккал: {:.3f}.")
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить дистанцию в км."""
        return (self.LINE_OUTPUT.format(self.training_type,
                                        self.duration,
                                        self.distance,
                                        self.speed,
                                        self.calories))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # stride length in meters
    M_IN_KM: float = 1000  # coefficient for converting meters to kilometers
    MIN_IN_HOUR: float = 60  # coefficient for converting minutes to hours
    VAL_CALORIE_CALC_18: float = 18  # coefficient for calculating calorie
    VAL_CALORIE_CALC_20: float = 20  # coefficient for calculating calorie

    def __init__(self,
                 action: int,  # action in training
                 duration: float,  # workout duration in minutes
                 weight: float,  # trainee weight in kilograms
                 ) -> None:
        self.action = action
        self.duration_m = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_m

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_m,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.VAL_CALORIE_CALC_18 * self.get_mean_speed()
                - self.VAL_CALORIE_CALC_20) * self.weight_kg
                / self.M_IN_KM * self.duration_m
                * self.MIN_IN_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_0_035: float = 0.035
    coeff_calorie_0_029: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,  # trainer's height in centimeters
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        """Сначала я думал заменить 2 - на pow() для этого и подключал Math"""
        return ((self.coeff_calorie_0_035 * self.weight_kg
                + (self.get_mean_speed()**2
                 // self.height_cm)
                * self.coeff_calorie_0_029
                * self.weight_kg) * self.duration_m
                * self.MIN_IN_HOUR
                )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_1_1: float = 1.1
    coeff_calorie_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration_m)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.coeff_calorie_1_1)
                * self.coeff_calorie_2 * self.weight_kg)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM


TRANING_TYPE: list = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRANING_TYPE:
        raise ValueError('Не верный тип тренировки: {}. '
                         'Допустимые значения: {} '
                         .format(workout_type, ", ".join(TRANING_TYPE)))
    try:
        TRANING_TYPE[workout_type](*data)
    except TypeError:
        print('Число параметров класса задано не верно ')
    return TRANING_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
