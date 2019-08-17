
from web3.module import (
    Module,
)

class Admin(Module):


    def stopRPC(self, password):
        return self.web3.manager.request_blocking("admin_stopRPC", [password])

    def startRPC(self, password):
        return self.web3.manager.request_blocking("admin_startRPC", [password])