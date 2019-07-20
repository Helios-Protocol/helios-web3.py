from web3 import Web3
from web3.eth import Eth
from helios_web3.hls import Hls
from helios_web3.personal import Personal
from web3._utils.empty import empty

class HeliosWeb3(Web3):
    def __init__(self, provider=empty, middlewares=None, modules=None, ens=empty):
        if modules is None:
            modules = {'hls': (Hls,), 'eth': (Eth,), 'personal': (Personal,)}
        else:
            modules['hls'] = (Hls,)
            modules['eth'] = (Eth,)
            modules['personal'] = (Personal,)

        super().__init__(provider=provider, middlewares=middlewares, modules=modules, ens=ens)
