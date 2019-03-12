from web3 import Web3
from helios_web3.hls import Hls
from web3.utils.empty import empty

class HeliosWeb3(Web3):
    def __init__(self, providers=empty, middlewares=None, modules=None, ens=empty):
        if modules is None:
            modules = {'hls': Hls}
        else:
            modules['hls'] = Hls

        super().__init__(providers=providers, middlewares=middlewares, modules=modules, ens=ens)
