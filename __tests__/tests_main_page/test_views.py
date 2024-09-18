"""This is a test for authorisation's form."""

import pytest
from playwright.async_api import Page, async_playwright

from __tests__.dotenv_ import TEST_HOST, TEST_LOGIN, TEST_PASSWORD

# This is a parametrize
testdata = [
    (TEST_LOGIN, TEST_PASSWORD, "0", True),
    (" ", TEST_PASSWORD, "1", False),
    (TEST_LOGIN, " ", "2", False),
    (" ", " ", "3", False),
    ("также отсортировало", "также отсортировало", "4", False),
    ("также_отсортировало", "также_отсортировало", "5", False),
    ("также-отсортировало", "также-отсортировало", "6", False),
    ("также-отсортировало", TEST_PASSWORD, "7", False),
    ("отсортировало", TEST_PASSWORD, "8", False),
    ("otsortirovalo", TEST_PASSWORD, "9", False),
    ("OTSORTI", TEST_PASSWORD, "10", False),
    (f" {TEST_LOGIN}", TEST_PASSWORD, "11", False),
    (f" {TEST_LOGIN} ", TEST_PASSWORD, "12", False),
    (f"{TEST_LOGIN}".replace("_", " "), TEST_PASSWORD, "13", False),
    (f"{TEST_LOGIN}".replace("_", "-"), TEST_PASSWORD, "14", False),
    (f"{TEST_LOGIN}".replace("-", "_"), TEST_PASSWORD, "15", False),
    (TEST_LOGIN.capitalize(), TEST_PASSWORD, "16", False),
    (TEST_LOGIN.lower(), TEST_PASSWORD, "17", False),
    (TEST_LOGIN.swapcase(), TEST_PASSWORD, "18", False),
    (f"{TEST_LOGIN[:3]} {TEST_LOGIN[5:]} ", TEST_PASSWORD, "19", False),
    (f" {TEST_LOGIN}", TEST_PASSWORD, "20", False),
    (f"{TEST_LOGIN}", f" {TEST_PASSWORD}", "21", False),
    (f"{TEST_LOGIN}", f"{TEST_PASSWORD} ", "22", False),
    (f"{TEST_LOGIN}", f" {TEST_PASSWORD} ", "23", False),
    (f"{TEST_LOGIN}", TEST_PASSWORD.replace("_", " "), "24", False),
    (f"{TEST_LOGIN}", TEST_PASSWORD.replace("_", "-"), "25", False),
    (f"{TEST_LOGIN}", TEST_PASSWORD.replace("_", " "), "26", False),
    (f"{TEST_LOGIN}", TEST_PASSWORD.replace("-", "_"), "27", False),
    (f"{TEST_LOGIN}", TEST_PASSWORD.replace("-", " "), "28", False),
    (TEST_LOGIN, TEST_PASSWORD.capitalize(), "29", False),
    (TEST_LOGIN, TEST_PASSWORD.lower(), "30", False),
    (TEST_LOGIN, TEST_PASSWORD.swapcase(), "31", False),
    (TEST_LOGIN, f"{TEST_PASSWORD[:3]} {TEST_PASSWORD[5:]}", "32", False),
]


async def fill_feields(one_page: Page, login, password) -> [bool, Page]:
    """Fill to the login form"""
    await one_page.goto(f"https://www.{TEST_HOST}/")
    result = await one_page.title()
    if result == "Swag Labs":
        await one_page.get_by_placeholder("Username").fill(login)
        await one_page.get_by_placeholder("Password").fill(password)
        return one_page
    return False


@pytest.fixture()
async def browsers():
    """Open the browser"""
    async with async_playwright() as playwright:
        webkit = playwright.webkit
        browser = await webkit.launch()
        context = await browser.new_context()
        yield context
        await context.close()
        await browser.close()


@pytest.mark.parametrize("login, password, ind, excepted", testdata)
async def test_autorization_form_group(browsers, login, password, ind, excepted):
    """
    This is a test for authorisation's form. Form from main page (first).
        Itself has a some parametrize and folder 'pic' (from a root project).
    0. Test's lines: 15, 17, 27, 28, 30 it's more
    1. Folder pic. In going cycle of test the folder 'pic' will receive
        screenshots. It has names (number from name is line's id):
        - `screenshot_0_page.png` on the start test.
        - 'screenshot_1error.png' if we have a not rue login or password.
        - 'screenshot_0_navigate.png' then we have aт authorisation.

    2. Below you can to see our params. This
    parametrize goes by the cycle. It has a 35 line by template:
    "(f"<your_login>", <your_password>, "<number_of_this_line>",
    <bool_result_will_expect>),". Exemple:
    "(TEST_LOGIN, TEST_PASSWORD, "24", False),"
    :param login: str
    :param password: str
    :param ind: str
    :param excepted: bool
    :return: void
    """
    # async with async_playwright() as playwright:
    # webkit = playwright.webkit
    # browser = await webkit.launch()
    # context = await browser.new_context()
    page = await browsers.new_page()
    await page.goto(f"https://www.{TEST_HOST}/")
    result_bool = await fill_feields(page, login, password)
    assert result_bool is not False

    # Make screen
    await page.screenshot(path=f"./pic/screenshot_{ind}_page.png")
    await page.locator('input[type="submit"]').click()
    res_true_false: bool = False

    # This is simple except/timeout
    page.get_by_text("Epic ")

    await page.wait_for_url("**/inventory.html")
    if "/inventory.html" in page.url:
        await page.screenshot(path=f"./pic/screenshot_{ind}_navigate.png")
        res_true_false = True
    else:
        await page.screenshot(path=f"./pic/screenshot_{ind}error.png")
    assert res_true_false == excepted
    # await page.close()
    await browsers.close()
