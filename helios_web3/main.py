from web3 import Web3
from web3.eth import Eth
from web3.net import Net
from helios_web3.hls import Hls
from helios_web3.personal import Personal
from web3._utils.empty import empty
from helios_web3.pythonic_middleware import pythonic_middleware

class HeliosWeb3(Web3):
    def __init__(self, provider=empty, middlewares=None, modules=None, ens=empty):
        if modules is None:
            modules = {'hls': (Hls,),
                       'eth': (Eth,),
                       'personal': (Personal,),
                       "net": (Net,),}
        else:
            modules['hls'] = (Hls,)
            modules['eth'] = (Eth,)
            modules['personal'] = (Personal,)
            modules['net'] = (Net,)

        if middlewares is None:
            middlewares = [
                (pythonic_middleware, 'pythonic'),
            ]

        super().__init__(provider=provider, middlewares=middlewares, modules=modules, ens=ens)
