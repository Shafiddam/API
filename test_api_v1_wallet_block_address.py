import uuid

import pytest

from .endpoints.wallet_endpoint import WalletEndpoint


# 7 Заблокировать статический кошелек /v1/wallet/block-address
# Позитивный тест
@pytest.mark.parametrize('network', ['tron'])
@pytest.mark.parametrize('currency', ['BUSD','TRX', 'USDC', 'USDT'])
def test_api_v1_wallet_block_address_positive(network, currency):
    """ Документация: https://doc.cryptomus.com/payments/block-wallet
    Параметры запроса
    uuid* - Идентификатор кошелька
    order_id* - Идентификатор заказа в Вашей системе
    is_force_refund - Верните все входящие платежи на адрес отправителя

    * - обязательный параметр
    Надо передать один из обязательных параметров, если Вы передадите оба,
    аккаунт будет идентифицирован с помощью order_id

    Пример запроса
    curl https://api.cryptomus.com/v1/wallet/block-address \
    -X POST \
    -H 'merchant: 8b03432e-385b-4670-8d06-064591096795' \
    -H 'sign: fe99035f86fa436181717b302b95bacff1' \
    -H 'Content-Type: application/json' \
    -d '{
        "order_id": "1"
    }'    """

    try:
        # ------------  1 Создание статического кошелька /v1/wallet
        # Создание статического кошелька, документация: https://doc.cryptomus.com/payments/creating-static
        order_id = str(uuid.uuid4())  # генерация случайного уникального идентификатора типа UUID
        data = {
                'network': network,
                'currency': currency,
                'order_id': order_id
                }
        response, sign = WalletEndpoint.create_wallet(data)
        print('\nstatus_code = ', response.status_code)
        print('order_id = ', order_id)
        print('sign = ', sign)
        response_data = response.json()
        print('response_data = ', response_data)
        result_data = response_data.get('result')
        print('result_data = ', result_data)

        # Проверяем, что все поля присутствуют
        assert 'wallet_uuid' in result_data, "wallet_uuid is missing in the response"
        assert 'uuid' in result_data, "uuid is missing in the response"
        assert 'order_id' in result_data, "order_id is missing in the response"
        assert 'currency' in result_data, "currency is missing in the response"
        assert 'network' in result_data, "network is missing in the response"
        assert 'address' in result_data, "address is missing in the response"
        assert 'url' in result_data, "url is missing in the response"
        # Проверяем, что все поля не пустые
        assert result_data['wallet_uuid'], "wallet_uuid is empty in the response"
        assert result_data['uuid'], "uuid is empty in the response"
        assert result_data['order_id'], "order_id is empty in the response"
        assert result_data['currency'], "currency is empty in the response"
        assert result_data['network'], "network is empty in the response"
        assert result_data['address'], "address is empty in the response"
        assert result_data['url'], "url is empty in the response"
        # проверка что статус код = 200
        assert response.status_code == 200, "Ошибка: статус код не 200!"

        # -------------------   2 Заблокировать статический кошелек /v1/wallet/block-address
        uuid_my = response_data['result']['uuid']
        print('uuid_my = ', uuid_my)
        print('order_id = ', order_id)
        data = {
            'order_id': order_id,
        }

        response, sign = WalletEndpoint.block_address(data)

        print('\nstatus_code = ', response.status_code)
        print('sign = ', sign)
        response_data = response.json()
        print(response_data)
        # проверка что статус код = 200
        assert response.status_code == 200, "Ошибка: статус код не 200!"

    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")