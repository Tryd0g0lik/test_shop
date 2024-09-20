"""This a page tests the event from cart"""

import pytest
from playwright.async_api import expect

from __tests__.tests_inventory_page.test_views import (add_product_to_cart,
                                                       browsers_inventory,
                                                       open_inventory_page)
from __tests__.tests_main_page.test_views import testdata

buy_testdata = [
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
    )
]


@pytest.fixture()
async def browsers_inventory_cart(browsers_inventory):
    # async with async_playwright() as playwright:
    # webkit = playwright.webkit
    # browser = await webkit.launch()

    # yield browser
    yield browsers_inventory


@pytest.mark.parametrize("login, password", buy_testdata)
async def test_buy_from_cart(browsers_inventory_cart, login: str, password: str):
    page, context, locators = await open_inventory_page(
        browsers_inventory_cart, login, password
    )
    await add_product_to_cart(page, locators)

    expect(page.locator("#checkout").filter(has_text="Checkout")).to_have_text(
        "Checkout"
    )
    page.locator("#checkout").click()

    # Clean up context after test
    await context.close()
