from scripts.helpful_scripts import get_account, encode_function_data
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_can_deploy():
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
    assert proxy_box.retrieve() == 0
    proxy_box.stores(1, {"from": account})
    assert proxy_box.retrieve() == 1
