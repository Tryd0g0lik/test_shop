"""This a page tests the event from cart"""

import pytest

from __tests__.tests_inventory_page.test_views import (add_product_to_cart,
                                                       open_inventory_page)
from __tests__.tests_main_page.test_views import testdata

buy_testdata = [
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
    )
]


@pytest.mark.parametrize("login, password", buy_testdata)
async def test_buy_from_cart(browsers_inventory, login: str, password: str):
    page, context, locators = await open_inventory_page(
        browsers_inventory, login, password
    )
    await add_product_to_cart(page, locators)
    # Clean up context after test
    await context.close()
