from scripts.helpful_scripts import get_account, encode_function_data
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def main():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    encoded_function_initializer = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_function_initializer,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, box.abi)
    # proxy_box.stores(1, {"from": account})
    print(proxy_box.retrieve())
