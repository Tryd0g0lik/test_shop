"""This a page tests the event from cart"""

import pytest
from playwright.async_api import expect

from __tests__.tests_inventory_page.test_views import (add_product_to_cart,
                                                       browsers_inventory,
                                                       open_inventory_page)
from __tests__.tests_main_page.test_views import testdata

# This params for a test the form/ It's a decor for a order
buy_testdata = [
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
        "0",
        "Firstname",
        "Sacondname",
        "999999",
        True,
    ),
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
        "2",
        "FirstName",
        "Sacondname",
        "999999",
        False,
    ),
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
        "3",
        "Firstname",
        "SaconDname",
        "999999",
        False,
    ),
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
        "4",
        "First Name",
        "Sacondname",
        "999999",
        False,
    ),
    (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
        "5",
        "Firstname",
        "Sacon Dname",
        "999999",
        False,
    ),
     (
        testdata[0][0],  # Login
        testdata[0][1],  # Password
        "6",
        "Firstname",
        "Sacon%dname",
        "999999",
        False,
    ),
 
]  # Here params not all. Not be all verification conditions for fields.


@pytest.fixture()
async def browsers_inventory_cart(browsers_inventory):
    yield browsers_inventory


async def get_body_manual_test(
    browsers_inventory_cart,
    login: str,
    password: str,
    ind: str,
    firstname: str,
    secondname: str,
    postalcode: [str, int],
):
    # Receiving a page
    page, context, locators = await open_inventory_page(
        browsers_inventory_cart, login, password
    )
    # One product add to the cart
    await add_product_to_cart(page, locators)
    cart = page.locator("#shopping_cart_container a")
    await expect(cart).not_to_be_empty()
    await expect(cart).to_be_visible()
    await cart.click()

    checkout_locator = page.get_by_role("button", name="checkout")
    await page.screenshot(
        path=f"./__tests__/tests_cart_for_buy/pic/\
    screenshot_{ind}_page.png"
    )
    await expect(checkout_locator).to_be_visible()

    # Open a form for order
    await expect(checkout_locator).to_have_text("Checkout")

    await page.locator("#checkout").click()
    locator_form = page.locator("form .checkout_info")
    await expect(locator_form).to_be_visible()
    locator_form = page.locator("form")
    # Fill fields
    # Firstname
    field_first_name = locator_form.get_by_placeholder("First Name")
    await expect(field_first_name).to_have_count(1)
    await expect(field_first_name).to_be_visible()
    await field_first_name.fill(value=firstname)

    # Secondname
    field_second_name = locator_form.get_by_placeholder("Last Name")
    await expect(field_second_name).to_have_count(1)
    await expect(field_second_name).to_be_visible()
    await field_second_name.fill(value=secondname)

    # Postal Code
    field_postal_code = locator_form.get_by_placeholder("Zip/Postal Code")
    await expect(field_postal_code).to_have_count(1)
    await expect(field_postal_code).to_be_visible()
    await locator_form.get_by_placeholder("Zip/Postal Code").fill(value=postalcode)

    await page.screenshot(
        path=f"./__tests__/tests_cart_for_buy/pic/\
    screenshot_{ind}_fill_field.png"
    )

    return [page, context, locators, locator_form]


@pytest.mark.parametrize(
    "login, password, ind, firstname, secondname, postalcode, asserts", buy_testdata
)
async def test_buy_from_cart(
    browsers_inventory_cart: browsers_inventory_cart,
    login: str,
    password: str,
    ind: str,
    firstname: str,
    secondname: str,
    postalcode: [str, int],
    asserts: bool,
):
    """
    This test check to make an order from cart.
    There (in cart) be filling an all fields, then press by button 'Continue'.
    After a 'Continue' if we can to see a next button with name 'Finish'.
    It means that an all fields were do fill is True.

    This a test is completed whith display the text 'Thank you for your order!'
    :param browsers_inventory_cart: @pytest.fixture
    :param login: str
    :param password: str
    :param ind: str
    :param firstname: str
    :param secondname: str
    :param postalcode: str
    :param asserts: str
    :return:
    """
    page, context, locators, locator_form = await get_body_manual_test(
        browsers_inventory_cart, login, password, ind, firstname, secondname, postalcode
    )
    # Button "Continue"
    button_continue = locator_form.locator("#continue")
    await expect(button_continue).to_have_count(1)
    await expect(button_continue).to_be_visible()
    await button_continue.click()

    # Button finish
    button_finis = page.get_by_role("button", name="finish")
    await expect(button_finis).to_have_count(1)
    await expect(button_finis).to_be_visible()
    result = False
    try:
        await button_finis.is_visible()
        result = True
    except Exception as err:
        pass
    # Below variable 'asserts', It's expected an answer.
    # If variable 'result' is True, it's mean - we can see
    # the button 'Finished'. Means, That all fields field were correct
    assert result == asserts

    # Completing an order and the test 'Thank you for your order!' display
    await button_finis.click()
    text_is_thank = page.get_by_text("Thank you for your order!")
    await expect(text_is_thank).to_have_count(1)
    await expect(text_is_thank).to_be_visible()
    # assert not button_finis.is_visible()
    # Clean up context after test

    await context.close()
    await browsers_inventory_cart.close()
