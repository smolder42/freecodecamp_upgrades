import eth_utils
from brownie import network, accounts, config
import eth_utils

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]


def get_account(number=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if number:
        return accounts[number]
    # if network.show_active() in config["networks"]:
    #    account = accounts.add(config["wallets"]["from_key"])
    #    return account
    # return None
    account = accounts.add(config["wallets"]["from_key"])
    return account


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy_contract_address,
    implementation_contract_address,
    proxy_admin=None,
    initializer=None,
    *args
):
    tx = None
    if proxy_admin:
        if initializer:
            tx = proxy_admin.upgradeAndCall(
                proxy_contract_address.address,
                implementation_contract_address,
                encode_function_data(initializer, *args),
                {"from": account, "gas_limit": 1000000},
            )
        else:
            tx = proxy_admin.upgrade(
                proxy_contract_address.address,
                implementation_contract_address,
                {"from": account, "gas_limit": 1000000},
            )
    else:
        if initializer:
            tx = proxy_contract_address.upgradeToAndCall(
                implementation_contract_address,
                encode_function_data(initializer, *args),
                {"from": account, "gas_limit": 1000000},
            )
        else:
            tx = proxy_contract_address.upgradeTo(
                implementation_contract_address,
                {"from": account, "gas_limit": 1000000},
            )
    return tx
