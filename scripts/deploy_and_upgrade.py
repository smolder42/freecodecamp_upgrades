from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract


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
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    box_v2 = BoxV2.deploy({"from": account})
    tx = upgrade(account, proxy, box_v2, proxy_admin=proxy_admin)
    tx.wait(1)
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print(proxy_box.retrieve())
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
