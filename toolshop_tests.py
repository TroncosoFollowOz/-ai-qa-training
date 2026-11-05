from playwright.sync_api import sync_playwright


BASE_URL = "https://practicesoftwaretesting.com/"


def test_browse_category(page):
    page.goto(BASE_URL)

    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()

    page_title = page.locator('[data-test="page-title"]').inner_text()

    assert page_title == "Category: Hand Tools", (
        "Expected the page title to be 'Category: Hand Tools'."
    )

    product_names = page.locator('[data-test="product-name"]')
    product_count = product_names.count()

    assert product_count > 0, (
        "Expected at least one product in the Hand Tools category."
    )

    for index in range(product_count):
        product_name = product_names.nth(index).inner_text().strip()

        assert product_name != "", (
            f"Expected product {index + 1} to have a non-empty name."
        )


def test_product_details(page):
    page.goto(BASE_URL)

    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()

    first_product = page.locator('[data-test="product-name"]').first
    expected_product_name = first_product.inner_text().strip()

    first_product.click()

    actual_product_name = (
        page.locator('[data-test="product-name"]').inner_text().strip()
    )

    assert actual_product_name == expected_product_name, (
        f"Expected the product name to be '{expected_product_name}', "
        f"but found '{actual_product_name}'."
    )

    product_price = page.locator('[data-test="unit-price"]').inner_text().strip()

    assert product_price != "", (
        "Expected the product detail page to show a price."
    )

    add_to_cart_button = page.locator('[data-test="add-to-cart"]')

    assert add_to_cart_button.is_visible(), (
        "Expected the Add to cart button to be visible."
    )


def test_add_to_cart(page):
    page.goto(BASE_URL)

    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()

    first_product = page.locator('[data-test="product-name"]').first
    expected_product_name = first_product.inner_text().strip()

    first_product.click()

    product_price = page.locator('[data-test="unit-price"]').inner_text().strip()

    page.locator('[data-test="add-to-cart"]').click()

    cart_quantity = page.locator('[data-test="cart-quantity"]')

    assert cart_quantity.inner_text().strip() == "1", (
        "Expected the cart icon to show a quantity of 1."
    )

    page.locator('[data-test="nav-cart"]').click()

    actual_product_name = (
        page.locator('[data-test="product-title"]').inner_text().strip()
    )

    assert actual_product_name == expected_product_name, (
        f"Expected the cart product name to be '{expected_product_name}', "
        f"but found '{actual_product_name}'."
    )

    quantity = page.locator('[data-test="product-quantity"]').input_value()

    assert quantity == "1", (
        "Expected the product quantity in the cart to be 1."
    )

    cart_total = page.locator('[data-test="cart-total"]').inner_text().strip()

    
    if cart_total.startswith("$"):
        cart_total = cart_total.replace("$", "", 1).strip()

    assert product_price in cart_total, (
        f"Expected the cart total to contain the product price "
        f"'{product_price}', but found '{cart_total}'."
    )


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000
        )

        tests = [
            test_browse_category,
            test_product_details,
            test_add_to_cart,
        ]

        for test in tests:
            page = browser.new_page()

            try:
                print(f"Running: {test.__name__}")
                test(page)
                print(f"PASS: {test.__name__}")
            except Exception as error:
                print(f"FAIL: {test.__name__}")
                print(f"Reason: {error}")
            finally:
                page.close()

        browser.close()


if __name__ == "__main__":
    main()