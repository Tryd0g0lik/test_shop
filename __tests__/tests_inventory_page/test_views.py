"""Position of the catalog."""

import re

import pytest
from playwright.async_api import Page, async_playwright, expect

from __tests__.dotenv_ import TEST_HOST
from __tests__.tests_main_page.test_views import fill_feields, testdata

# This is point for dependence after.
SECTION_TITLE: str = "Sauce Labs Backpack"


@pytest.fixture()
async def browsers_inventory():
    async with async_playwright() as playwright:
        webkit = playwright.webkit
        browser = await webkit.launch()

        yield browser


inventory_testdata = [
    (
        testdata[0][0],
        testdata[0][1],
        testdata[0][2],
        testdata[0][3],
        ".inventory_item",
        "text",
        SECTION_TITLE,
    ),
    (
        testdata[0][0],
        testdata[0][1],
        testdata[0][2],
        testdata[0][3],
        ".inventory_item",
        "role",
        "Add to cart",
    ),
    (
        testdata[0][0],
        testdata[0][1],
        testdata[0][2],
        testdata[0][3],
        ".inventory_item",
        "text",
        "carry.allTheThings() with the sleek, streamlined Sly Pack that melds \
        uncompromising style with unequaled laptop and tablet protection.",
    ),
    (
        testdata[0][0],
        testdata[0][1],
        testdata[0][2],
        testdata[0][3],
        ".inventory_item",
        "pattern",
        re.compile(r"\d{1,3}\.\d{1,2}"),
    ),
]


@pytest.mark.parametrize(
    "login, password, ind, excepted, select, view, text", inventory_testdata
)
async def test_combined_inventory(
    browsers_inventory: pytest.fixture,
    login: str,
    password: str,
    ind: str,
    select: str,
    view: str,
    text: str,
    excepted: [str, re.Pattern],
):

    context = await browsers_inventory.new_context()
    page: Page = await context.new_page()
    if_not_true = await fill_feields(page, login, password)

    assert if_not_true is not False
    await page.locator('input[type="submit"]').click()
    # Relocation after the login
    await page.goto(f"https://www.{TEST_HOST}/inventory.html")
    await if_not_true.wait_for_url("**/inventory.html", timeout=4000)
    assert "inventory.html" in page.url

    # Position 'Sauce Labs Backpack' look up and click
    await page.screenshot(
        path=f"./___tests__/tests_inventory_page/pic/screenshot_{ind}_page.png",
    )
    locators = page.locator(".inventory_item[data-test='inventory-item']")

    # title and descrip of position
    if isinstance(text, str) is str and view == "text":
        await expect(locators.filter(has_text=text)).to_contain_text(text)

    # price of position
    elif isinstance(text, re.Pattern) and view == "pattern":
        element = (
            locators.filter(has_text=SECTION_TITLE)
            .get_by_text("$")
            .filter(has_text=text)
        )

        assert await element.count() > 0

    # button
    elif view == "role":
        element = locators.filter(has_text=SECTION_TITLE).get_by_role(
            "button", name=text
        )
        assert await element.count() > 0

    # Check if it's a regex pattern
    await page.get_by_text("Sauce Labs Backpack").click()
    await expect(page).to_have_url(re.compile(r"/inventory-item\.html\?id=[0-9]+$"))

    # Single position adding into the cart
    await expect(
        page.locator("button[id='add-to-cart']").get_by_text("Add to cart")
    ).to_have_text("Add to cart")
    # Look on a cart 1/2
    locator = page.locator(".shopping_cart_link[data-test='shopping-cart-link']")
    await expect(locator).to_be_empty()
    await page.locator("button[id='add-to-cart']").click()
    # Look on a cart 2/2
    await expect(
        page.locator(".shopping_cart_link[data-test='shopping-cart-link']")
    ).not_to_be_empty()

    await context.close()
    await browsers_inventory.close()
