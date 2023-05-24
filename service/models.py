from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Salon(models.Model):
    name = models.CharField(
        'Название салона',
        max_length=255,
        db_index=True,
    )
    image = models.ImageField(
        'Изображение',
        db_index=True,
        blank=True,
    )
    address = models.CharField(
        'адрес',
        max_length=255,
        db_index=True
    )
    work_time = models.CharField(
        'Время работы',
        max_length=100,
        default='с 10:00 до 20:00 без выходных'
    )

    def __str__(self):
        return f'{self.name} {self.address}'

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'


class Client(models.Model):
    name = models.CharField(
        'Имя',
        max_length=255,
        db_index=True
    )
    phone = PhoneNumberField(
        'телефон',
        unique=True,
        default='+7 111 222 33 44'
    )

    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Specialist(models.Model):
    name = models.CharField(
        'Имя',
        max_length=255,
        db_index=True
    )
    specialization = models.ForeignKey(
        'Category',
        related_name='workers',
        verbose_name='Специализация',
        on_delete=models.CASCADE,
        db_index=True
    )
    salon = models.ForeignKey(
        Salon,
        related_name='workers',
        verbose_name='Салон',
        on_delete=models.CASCADE,
        db_index=True
    )
    foto = models.ImageField(
        'Фотография',
        null=True,
        blank=True
    )

    experience = models.CharField(
        'Стаж работы',
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.name} {self.specialization} {self.salon}'

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'


class Category(models.Model):
    name = models.CharField(
        'Категория услуг',
        max_length=255,
        db_index=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Service(models.Model):
    name = models.CharField(
        'Название услуги',
        max_length=255,
        db_index=True
    )
    category = models.ForeignKey(
        'Category',
        related_name='services',
        verbose_name='Категория',
        on_delete=models.CASCADE,
        db_index=True
    )
    descriptions = models.TextField(
        'Описание',
        null=True,
        blank=True,
        db_index=True
    )
    image = models.ImageField(
        'Изображение',
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True
    )

    def __str__(self):
        return f'{self.name} {self.price}'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class PaymentMethod(models.TextChoices):
    CASHLESS = 'cashless', 'Безналичный'
    CASH = 'cash', 'Наличные'


class PaymentStatus(models.TextChoices):
    PAID = 'paid', 'Оплачен'
    NOT_PAID = 'not_paid', 'Не оплачен'


class Order(models.Model):
    MORNING_1 = '10:00'
    MORNING_2 = '10:30'
    DAY_1 = '12:00'
    DAY_2 = '12:30'
    DAY_3 = '15:00'
    DAY_4 = '16:30'
    EVENING_1 = '17:00'
    EVENING_2 = '18:30'
    EVENING_3 = '19:00'

    WORK_HOURS = [
        (MORNING_1, MORNING_1),
        (MORNING_2, MORNING_2),
        (DAY_1, DAY_1),
        (DAY_2, DAY_2),
        (DAY_3, DAY_3),
        (DAY_4, DAY_4),
        (EVENING_1, EVENING_1),
        (EVENING_2, EVENING_2),
        (EVENING_3, EVENING_3),
    ]
    client = models.ForeignKey(
        Client,
        related_name='orders',
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        db_index=True
    )
    procedure = models.ForeignKey(
        'Service',
        related_name='orders',
        verbose_name='Услуга',
        on_delete=models.CASCADE,
        db_index=True
    )
    salon = models.ForeignKey(
        Salon,
        related_name='orders',
        verbose_name='Салон',
        on_delete=models.CASCADE,
        db_index=True
    )
    specialist = models.ForeignKey(
        Specialist,
        related_name='orders',
        verbose_name='Специалист',
        on_delete=models.CASCADE,
        db_index=True
    )
    order_hour = models.CharField(
        'Время записи',
        max_length=20,
        choices=WORK_HOURS,
        blank=True,

    )
    order_day = models.DateField(
        'Дата',
        null=True
    )
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=12,
        blank=True,
        choices=PaymentMethod.choices,
        db_index=True,
    )
    payment_status = models.CharField(
        'Статус оплаты',
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_PAID,
        db_index=True
    )

    def __str__(self):
        return f'{self.specialist.name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

