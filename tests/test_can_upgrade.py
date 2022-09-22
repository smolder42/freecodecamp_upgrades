from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract
import pytest


def test_can_upgrade():
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

    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(AttributeError):
        proxy_box.increment({"from": account})

    tx = upgrade(account, proxy, box_v2, proxy_admin=proxy_admin)
    tx.wait(1)
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
