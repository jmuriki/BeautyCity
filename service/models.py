from django.db import models
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField
from datetime import time, timedelta, datetime


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
        default='+70000000000'
    )

    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class WorkDay(models.Model):
    date = models.DateField()
    specialists = models.ManyToManyField('Specialist', related_name='workdays', blank=True)

    def __str__(self):
        return f'{self.date}'

    class Meta:
        verbose_name = 'Рабочий день'
        verbose_name_plural = 'Рабочие дни'


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
    role = models.CharField(
        'Должность',
        max_length=255,
        db_index=True,
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
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
    )
    order_hour = models.ForeignKey(
        'TimeSlot',
        verbose_name='Время приема',
        related_name='orders',
        on_delete=models.SET_NULL,
        default=None,
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


class TimeSlot(models.Model):
    DAYTIME_CHOICES = (
        ('M', 'Утро'),
        ('L', 'Обед'),
        ('E', 'Вечер')
    )
    START_TIME = time(10, 0)
    END_TIME = time(19, 30)
    INTERVAL = timedelta(minutes=30)

    START_TIME_CHOICES = []

    current_time = datetime.combine(datetime.today(), START_TIME)
    end_time = datetime.combine(datetime.today(), END_TIME)
    while current_time.time() <= end_time.time():
        START_TIME_CHOICES.append((current_time.time(), current_time.time().strftime('%H:%M')))
        current_time += INTERVAL

    start_time = models.TimeField('Начало', choices=START_TIME_CHOICES)
    end_time = models.TimeField('Конец', editable=False, null=True, blank=True)  # New field
    date = models.ForeignKey(WorkDay, on_delete=models.CASCADE, related_name='appointments')
    specialist = models.ForeignKey(
        Specialist,
        verbose_name='Специалист',
        on_delete=models.CASCADE,
        null=True
    )
    is_available = models.BooleanField(default=True)
    daytime = models.CharField(
        max_length=1,
        verbose_name='Время суток',
        choices=DAYTIME_CHOICES,
        db_index=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Временной период'
        verbose_name_plural = 'Временные периоды'

    def __str__(self):
        return f'{self.start_time}:{self.end_time} - {self.date.date}'

    def clean(self, ):
        super().clean()
        if self.start_time < time(10, 0) or self.start_time > time(19, 30):
            raise ValidationError("Время должно быть между 10:00 и 19:30")
        if time(10, 0) <= self.start_time < time(11, 30):
            self.daytime = 'M'
        elif self.start_time <= time(16, 30):
            self.daytime = 'L'
        else:
            self.daytime = 'E'

        start_datetime = datetime.combine(self.date.date, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=30)
        self.end_time = end_datetime.time().strftime('%H:%M')

        self.is_available = self.specialist in self.date.specialists.all()

