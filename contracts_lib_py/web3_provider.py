from web3 import Web3

from contracts_lib_py.web3.http_provider import CustomHTTPProvider


class Web3Provider(object):
    """Provides the Web3 instance."""
    _web3 = None

    @staticmethod
    def get_web3(keeper_url=None, provider=None):
        """Return the web3 instance to interact with the ethereum client."""
        if Web3Provider._web3 is None:
            if not provider:
                assert keeper_url, 'keeper_url or a provider instance is required.'
                provider = CustomHTTPProvider(keeper_url)

            Web3Provider._web3 = Web3(provider)
            # Reset attributes to avoid lint issue about no attribute
            Web3Provider._web3.EthereumTesterProvider = getattr(Web3Provider._web3, 'EthereumTesterProvider')
            Web3Provider._web3.HTTPProvider = getattr(Web3Provider._web3, 'HTTPProvider')
            Web3Provider._web3.IPCProvider = getattr(Web3Provider._web3, 'IPCProvider')
            Web3Provider._web3.Iban = getattr(Web3Provider._web3, 'Iban')
            Web3Provider._web3.RequestManager = getattr(Web3Provider._web3, 'RequestManager')
            Web3Provider._web3.WebsocketProvider = getattr(Web3Provider._web3, 'WebsocketProvider')
            Web3Provider._web3.codec = getattr(Web3Provider._web3, 'codec')
            Web3Provider._web3.eth = getattr(Web3Provider._web3, 'eth')
            Web3Provider._web3.geth = getattr(Web3Provider._web3, 'geth')
            Web3Provider._web3.manager = getattr(Web3Provider._web3, 'manager')
            Web3Provider._web3.net = getattr(Web3Provider._web3, 'net')
            Web3Provider._web3.parity = getattr(Web3Provider._web3, 'parity')
            Web3Provider._web3.provider = getattr(Web3Provider._web3, 'provider')
            Web3Provider._web3.testing = getattr(Web3Provider._web3, 'testing')
            Web3Provider._web3.version = getattr(Web3Provider._web3, 'version')

        return Web3Provider._web3

    @staticmethod
    def set_web3(web3):
        Web3Provider._web3 = web3
