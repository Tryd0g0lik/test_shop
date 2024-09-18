"""Position of the catalog."""

import pytest
from playwright.async_api import Page, async_playwright, expect

from __tests__.dotenv_ import TEST_HOST
from __tests__.tests_main_page.test_views import fill_feields, testdata


@pytest.fixture()
async def browsers_inventory():
    async with async_playwright() as playwright:
        webkit = playwright.webkit
        browser = await webkit.launch()

        yield browser


@pytest.mark.parametrize("login, password, ind, excepted", testdata[:1])
async def test_combined_inventory(browsers_inventory, login, password, ind, excepted):

    context = await browsers_inventory.new_context()
    page: Page = await context.new_page()
    if_not_true = await fill_feields(page, login, password)
    await page.locator('input[type="submit"]').click()

    assert if_not_true is False

    await page.goto(f"https://www.{TEST_HOST}/inventory.html")
    await if_not_true.wait_for_url("**/inventory.html", timeout=4000)
    assert "inventory.html" in page.url

    await expect(page.get_by_text("Sauce Labs Backpack")).to_have_text(
        "Sauce Labs Backpack"
    )
    await page.get_by_text("Sauce Labs Backpack").click()
    await page.screenshot(
        path=f"./___tests__/tests_inventory_page/pic/screenshot_{ind}_page.png"
    )
    await expect(
        page.locator("button[id='add-to-cart']").get_by_text("Add to cart")
    ).to_have_text("Add to cart")

    await context.close()
    await browsers_inventory.close()
