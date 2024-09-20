"""This a test that where we can to make a click and  navigate to
    the product page."""

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


# This is parametrize
inventory_testdata = [
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
        "1",  # This id of params, symply
        testdata[0][3],  # bool. This is no need.
        ".inventory_item",  # selector for a total/general contain
        "text",  # This is data type for "inventory_testdata[0][-1]"
        SECTION_TITLE,  # What expect we for search
    ),
    (
        testdata[0][0],
        testdata[0][1],
        "2",
        testdata[0][3],
        ".inventory_item",
        "role",
        "Add to cart",
    ),
    (
        testdata[0][0],
        testdata[0][1],
        "3",
        testdata[0][3],
        ".inventory_item",
        "text",
        "carry.allTheThings() with the sleek, streamlined Sly Pack that melds \
        uncompromising style with unequaled laptop and tablet protection.",
    ),
    (
        testdata[0][0],
        testdata[0][1],
        "4",
        testdata[0][3],
        ".inventory_item",
        "pattern",
        re.compile(r"\d{1,3}\.\d{1,2}"),
    ),
]


async def open_inventory_page(browsers, login, password):
    """
    Open the page
    :param browsers:
    :param login:
    :param password:
    :return: [page, context, locators] where a "page" is \
        the page contain the DOM of "inventory.html". \
        "context" for a close when to the test completing \
        "locators" - this attribute use to def "add_product_to_cart" and end.
    """
    context = await browsers.new_context()
    page: Page = await context.new_page()
    if_not_true = await fill_feields(page, login, password)

    assert if_not_true is not False
    await page.locator('input[type="submit"]').click()
    # Relocation after the login
    await page.goto(f"https://www.{TEST_HOST}/inventory.html")
    await if_not_true.wait_for_url("**/inventory.html", timeout=4000)
    assert "inventory.html" in page.url
    # Position 'Sauce Labs Backpack' look up and click
    locators = page.locator(".inventory_item[data-test='inventory-item']")
    return [page, context, locators]


async def add_product_to_cart(page, locators):
    """

    :param page:
    :param locators:
    :return:
    """
    await expect(locators.filter(has_text=SECTION_TITLE)).to_contain_text(SECTION_TITLE)
    ree = locators.get_by_text(text=SECTION_TITLE)
    await ree.click()
    await expect(page).to_have_url(
        re.compile(r"/inventory-item\.html\?id=[0-9]+$"), timeout=7000
    )
    await expect(
        page.locator("button[id='add-to-cart']").get_by_text("Add to cart")
    ).to_have_text("Add to cart")
    await page.locator("button[id='add-to-cart']").click()


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
    text: [str, re.Pattern],
    excepted: bool,
):
    """
    This a test that where we can to make a click and then do navigate to
    the product page.
    :param browsers_inventory: browser is a fixture
    :param login: str
    :param password: str
    :param ind: # This an id param, simple. We can to see the error if \
        will been. Which the param from id do receive an error.
    :param select: str. This selector of the total/general contain for \
        after the work all
    :param view: str This is data type for "inventory_testdata[0][-1]"
    :param text: [str, re.Pattern]  What expect we for search
    :param excepted: bool. inheritance from the first test. It is no need.
    :return:
    """
    page, context, locators = await open_inventory_page(
        browsers_inventory, login, password
    )

    # title and descrip of position, Param inventory_testdata[0] and [0:4:3]
    if isinstance(text, str) and view == "text":
        await add_product_to_cart(page, locators)

    # price of position.  inventory_testdata[3]
    elif isinstance(text, re.Pattern) and view == "pattern":
        element = (
            locators.filter(has_text=SECTION_TITLE)
            .get_by_text("$")
            .filter(has_text=text)
        )

        assert await element.count() > 0
        await page.screenshot(
            path=f"./___tests__/tests_inventory_page/\
                pic/screenshot_{ind}_page.png"
        )

        await locators.filter(has_text=SECTION_TITLE).locator(
            "button", has_text="Add to cart"
        ).click()

    # button  Param inventory_testdata[1]
    elif view == "role":
        # Here one section chose and look up to the button
        element = locators.filter(has_text=SECTION_TITLE).get_by_role(
            "button", name=text
        )
        assert await element.count() > 0
        await element.click()
        # change the button. If it has selector "#add-to-cart" this means
        # not True
        await expect(
            page.locator("button[id='add-to-cart']").get_by_text(text)
        ).to_have_count(0)

    # Check if it's a regex pattern
    try:
        await expect(page.locator("button[id='add-to-cart']")).to_have_text(
            "Add to cart"
        ).not_to_have_count(1)
        # Look on a cart 1/2
        locator = page.locator(".shopping_cart_link[data-test='shopping-cart-link']")
        await expect(locator).to_be_empty()

    except Exception as err:
        print(err)
    finally:

        # Look on a cart 2/2
        await expect(
            page.locator(".shopping_cart_link[data-test='shopping-cart-link']")
        ).not_to_be_empty()

        await context.close()
        await browsers_inventory.close()
