from pyboleto.bank.caixa import BoletoCaixa as BaseBoletoCaixa
from django.conf import settings


class BoletoCaixa(BaseBoletoCaixa):
    """
    Configures the BoletoCaixa until it comes clean from the original repo.
    """
    def __init__(self, *args, **kwargs):
        super(BoletoCaixa, self).__init__(*args, **kwargs)
        # inicio_nosso_numero need 2 number or more to create nosso_numero
        if len(settings.BILLET_PREFIX) < 2:
            prefix = '{0}0'.format(settings.BILLET_PREFIX)
        else:
            prefix = settings.BILLET_PREFIX
        self.inicio_nosso_numero = prefix  # this is supposed to be part of pyboleto
