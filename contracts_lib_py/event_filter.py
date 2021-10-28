import logging
import time

from contracts_lib_py.web3_provider import Web3Provider

logger = logging.getLogger(__name__)


class EventFilter:
    def __init__(self, event_name, event, argument_filters, from_block, to_block,
                 poll_interval=None):
        self.event_name = event_name
        self.event = event
        self.argument_filters = argument_filters
        self.block_range = (from_block, to_block)
        self._filter = None
        self._poll_interval = poll_interval if poll_interval else 0.5
        self._create_filter()

    @property
    def filter_id(self):
        return self._filter.filter_id if self._filter else None

    def uninstall(self):
        Web3Provider.get_web3().eth.uninstallFilter(self._filter.filter_id)

    def set_poll_interval(self, interval):
        self._poll_interval = interval

    def recreate_filter(self):
        self._create_filter()

    def _create_filter(self):
        chain_id = Web3Provider.get_web3().net.version
        from_block = 0

        # temporary workaround to work with mumbai
        # Infura has a 1000 block range limit in their api
        if chain_id == '80001':
            latest_block = Web3Provider.get_web3().eth.get_block_number()
            from_block = latest_block - 990


        self._filter = {
            'fromBlock': from_block,
            'toBlock': self.block_range[1],
            'argument_filters': self.argument_filters
        }

    def get_new_entries(self, max_tries=1):
        # This api is not provided by polygon
        try:
            return self._get_entries(max_tries=max_tries)
        except ValueError as e:
            # method does not exist or is not available
            if e.args[0]['code'] == -32601:
                return []
            else:
                raise

    def get_all_entries(self, max_tries=1):
         # This api is not provided by polygon
        try:
            return self._get_entries(max_tries=max_tries)
        except ValueError as e:
            # method does not exist or is not available
            if e.args[0]['code'] == -32601:
                return []
            else:
                raise

    def _get_entries(self, max_tries=1):
        i = 0
        while i < max_tries:
            try:
                logs = self.event.getLogs(**self._filter)
                if logs:
                    logger.debug(
                        f'found event logs: event-name={self.event_name}, '
                        f'range={self.block_range}, '
                        f'logs={logs}')
                    return logs
            except ValueError as e:
                if 'Filter not found' in str(e):
                    logger.debug(f'recreating filter (Filter not found): event={self.event_name}, '
                                 f'arg-filter={self.argument_filters}, from/to={self.block_range}')
                    time.sleep(1)
                    self._create_filter()
                else:
                    raise

            i += 1
            if max_tries > 1 and i < max_tries:
                time.sleep(0.5)

        return []
