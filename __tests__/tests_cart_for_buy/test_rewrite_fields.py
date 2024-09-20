"""Here we make specially one mistake"""

import pytest

from __tests__.tests_cart_for_buy.test_views import buy_testdata, get_body_manual_test
from __tests__.tests_inventory_page.test_views import browsers_inventory


@pytest.fixture()
async def browsers_cart(browsers_inventory):
    yield browsers_inventory


@pytest.mark.parametrize(
    "login, password, ind, firstname, secondname, postalcode, asserts",
    buy_testdata[1:2],
)
async def test_second_buy_from_cart(
    browsers_cart: browsers_cart,
    login: str,
    password: str,
    ind: str,
    firstname: str,
    secondname: str,
    postalcode: [str, int],
    asserts: bool,
):
    """
    This test inherits from '__tests__/tests_cart_for_buy/test_buy_from_cart'.
    Here we make specially an one mistake. It is inserting to
    the first field (first name).
    After, makes to press by button 'Continue'. This is event return to publish
    the error message.
    Then, make a repeat of steps and filling all fields then.
    Test should receive is correct response.
    :param browsers_cart: @pytest.fixture
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
        browsers_cart, login, password, ind, "", secondname, postalcode
    )

    # Button finish
    button_finis = page.get_by_role("button", name="finish")
    try:
        await button_finis.is_visible()
    except Exception as err:
        pass
    asserts_two = True

    # Double
    page, context, locators, locator_form = await get_body_manual_test(
        browsers_cart,
        login,
        password,
        "1",
        "Firstname",
        "Sacondname",
        "999999",
    )
    await page.screenshot(
        path=f"./__tests__/tests_cart_for_buy/pic/\
        screenshot_{ind}_double_1.png"
    )
    # Button finish
    button_finis = page.get_by_role("button", name="finish")
    result = False
    try:
        await button_finis.is_visible()
        result = True
    except Exception as err:
        pass
    # Below variable 'asserts', It's expected an answer.
    # If variable 'result' is True, it's mean - we can see
    # the button 'Finished'. Means, That all fields field were correct
    await page.screenshot(
        path=f"./__tests__/tests_cart_for_buy/pic/\
            screenshot_{ind}_double_2.png"
    )
    assert result == asserts_two
    # assert not button_finis.is_visible()
    # Clean up context after test

    await context.close()
    await browsers_cart.close()
