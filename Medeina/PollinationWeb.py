from .Web import Web
from .config import *


class PollinationWeb(Web):
    def __init__(self, path=BASEDIR, *args, **kwargs):
        super().__init__(path, args, kwargs)
        newWeb = self.filterByInteractionType(["pollination"])
        self.linkMetas = newWeb.linkMetas
        self.datasetMetas = newWeb.datasetMetas
        self.interactions = newWeb.interactions
        self.stringNames = newWeb.stringNames
        self.taxa = newWeb.taxa
