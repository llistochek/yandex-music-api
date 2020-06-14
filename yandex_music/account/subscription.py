from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, AutoRenewable, RenewableRemainder, NonAutoRenewable, Operator


class Subscription(YandexMusicObject):
    """Класс, представляющий информацию о подписках пользователя.

    Attributes:
        non_auto_renewable_remainder (:obj:`yandex_music.RenewableRemainder`): Напоминание о продлении.
        auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`): Автопродление подписки.
        family_auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`): Автопродление семейной подписки.
        operator (:obj:`list` из :obj:`yandex_music.Operator`): Услуги сотового оператора.
        non_auto_renewable (:obj:`yandex_music.NonAutoRenewable`): Отключённое автопродление.
        can_start_trial (:obj:`bool`): Есть ли возможность начать пробный период.
        mcdonalds (:obj:`bool`): mcdonalds TODO.
        end (:obj:`str`): Дата окончания.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        non_auto_renewable_remainder (:obj:`yandex_music.RenewableRemainder`): Напоминание о продлении.
        auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`, optional): Автопродление.
        family_auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`): Автопродление семейной подписки.
        operator (:obj:`list` из :obj:`yandex_music.Operator`, optional): Услуги сотового оператора.
        non_auto_renewable (:obj:`yandex_music.NonAutoRenewable`, optional): Отключённое автопродление.
        can_start_trial (:obj:`bool`, optional): Есть ли возможность начать пробный период.
        mcdonalds (:obj:`bool`, optional): mcdonalds TODO.
        end (:obj:`str`, optional): Дата окончания.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 non_auto_renewable_remainder: 'RenewableRemainder',
                 auto_renewable: List['AutoRenewable'],
                 family_auto_renewable: List['AutoRenewable'],
                 operator: List['Operator'] = None,
                 non_auto_renewable: Optional['NonAutoRenewable'] = None,
                 can_start_trial: Optional[bool] = None,
                 mcdonalds: Optional[bool] = None,
                 end: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.non_auto_renewable_remainder = non_auto_renewable_remainder
        self.auto_renewable = auto_renewable
        self.family_auto_renewable = family_auto_renewable

        self.operator = operator
        self.non_auto_renewable = non_auto_renewable
        self.can_start_trial = can_start_trial
        self.mcdonalds = mcdonalds
        self.end = end

        self.client = client
        self._id_attrs = (self.non_auto_renewable_remainder, self.auto_renewable, self.family_auto_renewable)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Subscription']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Subscription`: Информация о подписках пользователя.
        """
        if not data:
            return None

        data = super(Subscription, cls).de_json(data, client)
        from yandex_music import AutoRenewable, RenewableRemainder, NonAutoRenewable, Operator
        data['auto_renewable'] = AutoRenewable.de_list(data.get('auto_renewable'), client)
        data['family_auto_renewable'] = AutoRenewable.de_list(data.get('family_auto_renewable'), client)
        data['non_auto_renewable_remainder'] = RenewableRemainder.de_json(
            data.get('non_auto_renewable_remainder'), client)
        data['non_auto_renewable'] = NonAutoRenewable.de_json(data.get('non_auto_renewable'), client)
        data['operator'] = Operator.de_list(data.get('operator'), client)

        return cls(client=client, **data)
