import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(-1) is True
        assert product.check_quantity(0) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_check_quantity_zero(self,product):
        zero_product = Product("Notebook", 100, "This is a notebook", 0)
        assert zero_product.check_quantity(0) is True
        assert zero_product.check_quantity(1) is False


    def test_product_buy_positive(self, product):
        product.buy(1)
        assert product.quantity == 999

    def test_product_buy_all_items(self, product):
        product.buy(1000)
        assert product.quantity == 0


    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            assert product.buy(1001), 'Expecting ValueError here'


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product(self, cart, product):
        assert len(cart.products) == 0
        cart.add_product(product)
        assert len(cart.products) == 1
        assert cart.products[product] == 1
        cart.add_product(product, 100)
        assert cart.products[product] == 101

    def test_remove_product(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, 1)
        assert cart.products[product] == 9
        cart.remove_product(product)
        assert len(cart.products) == 0
        cart.add_product(product, 100)
        cart.remove_product(product, 100)
        assert cart.products[product] == 0
        cart.add_product(product, 500)
        cart.remove_product(product, 501)
        assert len(cart.products) == 0

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 100)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product):
        assert cart.get_total_price() == 0
        cart.add_product(product)
        assert cart.get_total_price() == 100
        cart.add_product(product, 50)
        assert cart.get_total_price() == 5100

    def test_buy_product(self, cart, product):
        cart.add_product(product)
        cart.buy()
        assert len(cart.products) == 0

    def test_product_buy_more_than_available(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            assert cart.buy()