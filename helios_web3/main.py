from web3 import Web3
from web3.eth import Eth
from web3.net import Net
from helios_web3.hls import Hls
from helios_web3.personal import Personal
from web3._utils.empty import empty
from helios_web3.pythonic_middleware import pythonic_middleware
from web3.middleware import (
    name_to_address_middleware,
    attrdict_middleware,
)
from helios_web3.abi import abi_middleware



class HeliosWeb3(Web3):
    def __init__(self, provider=empty, middlewares=None, modules=None, ens=empty):
        if modules is None:
            modules = {'hls': (Hls,),
                       'eth': (Hls,),
                       'personal': (Personal,),
                       "net": (Net,),}
        else:
            modules['hls'] = (Hls,)
            modules['eth'] = (Eth,)
            modules['personal'] = (Personal,)
            modules['net'] = (Net,)

        if middlewares is None:
            middlewares = [
                (name_to_address_middleware(self), 'name_to_address'),
                (attrdict_middleware, 'attrdict'),
                (pythonic_middleware, 'pythonic'),
                (abi_middleware, 'abi'),
            ]

        super().__init__(provider=provider, middlewares=middlewares, modules=modules, ens=ens)
