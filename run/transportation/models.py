import threading
from typing import NoReturn

from django.db import models


class ContragentMixin(models.Model):
    name = models.CharField(verbose_name="Имя (наименование)", max_length=225, null=True)
    contact_info = models.CharField(verbose_name="Контактные данные", max_length=225, null=True)
    in_black_list = models.BooleanField(verbose_name="В черном списке", default=False)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Client(ContragentMixin, models.Model):
    pass


class Carrier(ContragentMixin, models.Model):
    pass


class Auction(models.Model):
    """данные перевозки"""
    time_transportation = models.DateTimeField(verbose_name="дата, время перевозки")
    start_address = models.CharField(verbose_name="Адрес погрузки", max_length=225)
    finish_address = models.CharField(verbose_name="Адрес разгрузки", max_length=225, null=True)
    length = models.IntegerField(verbose_name="Расстояние", )
    """данные аукциона"""
    time_start = models.DateTimeField(verbose_name="Начало аукциона", auto_now_add=True)

    min_price = models.IntegerField(verbose_name="Начальная цена", default=0)
    max_price = models.IntegerField(verbose_name="Максимальная цена", default=0)
    interval = models.IntegerField(verbose_name="Продолжительность шага", default=1)
    step = models.IntegerField(verbose_name='Шаг аукциона')
    is_step_taken = models.BooleanField(verbose_name="Шаг сделан", default=False)
    total_price = models.IntegerField(verbose_name="Итоговая цена", blank=True, null=True)
    is_auto_price_increase = models.BooleanField(verbose_name="Произошло автоувеличение цены", default=False)

    """другие данные"""
    name = models.CharField(verbose_name="Наименование перевозки", max_length=225, blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    more_info = models.TextField(verbose_name="Дополнительная информация", max_length=1000, blank=True, null=True)
    is_underway = models.BooleanField(verbose_name="Аукцион в процессе", default=False)
    is_done = models.BooleanField(verbose_name="Аукцион завершен", default=False)

    winner_exist = models.BooleanField(verbose_name="Есть победитель", default=False)
    winner_name = models.CharField(verbose_name="Имя (наименование) победителя", max_length=225, blank=True, null=True)
    winner_contact = models.CharField(verbose_name="Контактные данные победителя", max_length=225, blank=True, null=True)

    def setup(self) -> NoReturn:
        self.total_price = self.min_price
        self.winner_name = None
        self.winner_contact = None
        self.winner_exist = False
        self.is_done = False
        self.is_underway = True
        self.save()

    def check_max_price_is_valid(self) -> NoReturn:
        return self.total_price + self.step <= self.max_price

    def auto_price_increase(self) -> NoReturn:
        if self.check_max_price_is_valid():
            lock = threading.Lock()

            with lock:
                self.total_price += self.step
                self.is_auto_price_increase = True
                self.save()

    @staticmethod
    def timer_off() -> NoReturn:
        for thread in threading.enumerate():
            if thread.name == 'timer':
                thread.cancel()

    def save_contacts(self, data: dict, commit=True) -> NoReturn:
        self.winner_name = data.get('name')
        self.winner_contact = data.get('contact_info')
        self.winner_exist = True

        if commit:
            self.save()

    def take_step(self, data: dict) -> NoReturn:
        self.timer_off()
        self.save_contacts(data, commit=False)
        self.is_step_taken = True
        self.is_underway = False
        self.is_done = True
        self.save()

    def stop(self) -> NoReturn:
        self.timer_off()
        self.is_underway = False
        self.is_done = True
        self.save()

    @staticmethod
    def check_start_timer_allowed() -> bool:
        return not any(['timer' in [thread.name for thread in threading.enumerate()]])

    def start_timer(self) -> NoReturn:
        if self.check_start_timer_allowed():
            threading.Thread(target=self.timer, name='start_timer_thread').start()

    def timer(self) -> NoReturn:
        self.setup()

        while not self.is_done and self.check_max_price_is_valid():
            """edit to hours"""
            timer = threading.Timer(interval=self.interval, function=self.auto_price_increase)
            timer.name = 'timer'
            timer.start()

            while True:
                if self.is_step_taken:
                    break
                if self.is_auto_price_increase:
                    self.is_auto_price_increase = False
                    break

        self.is_done = True
        self.is_underway = False
        self.save()
