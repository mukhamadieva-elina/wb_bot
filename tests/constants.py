test_number = 21313123132
price_history_ex = [{'dt': 1693094400, 'price': {'RUB': 25582}}, {'dt': 1693699200, 'price': {'RUB': 25929}}, {'dt': 1694304000, 'price': {'RUB': 25566}}, {'dt': 1694908800, 'price': {'RUB': 25537}}, {'dt': 1695513600, 'price': {'RUB': 25864}}, {'dt': 1696118400, 'price': {'RUB': 28778}}, {'dt': 1696723200, 'price': {'RUB': 26285}}, {'dt': 1697328000, 'price': {'RUB': 24956}}, {'dt': 1697932800, 'price': {'RUB': 25214}}, {'dt': 1698537600, 'price': {'RUB': 25180}}, {'dt': 1699142400, 'price': {'RUB': 24834}}, {'dt': 1699747200, 'price': {'RUB': 23587}}, {'dt': 1700352000, 'price': {'RUB': 20862}}, {'dt': 1700956800, 'price': {'RUB': 17767}}, {'dt': 1701561600, 'price': {'RUB': 17595}}, {'dt': 1702166400, 'price': {'RUB': 19220}}, {'dt': 1702771200, 'price': {'RUB': 19441}}, {'dt': 1703376000, 'price': {'RUB': 19103}}, {'dt': 1703980800, 'price': {'RUB': 18914}}, {'dt': 1704585600, 'price': {'RUB': 18873}}, {'dt': 1705190400, 'price': {'RUB': 19167}}, {'dt': 1705795200, 'price': {'RUB': 19231}}, {'dt': 1706400000, 'price': {'RUB': 19193}}, {'dt': 1707004800, 'price': {'RUB': 19186}}, {'dt': 1707609600, 'price': {'RUB': 19177}}]
error_load_image_answer = {'status_code': 400, 'error': {'message': 'No file was uploaded (UPLOAD_ERR_NO_FILE)', 'code': 201},
            'status_txt': 'Bad Request'}
bad_status_load_image_answer = {'status_code': 400, 'status_txt': 'Bad Request'}

positive_load_image_answer = {'data': {'id': 'gWQn35j', 'title': 'image', 'url_viewer': 'https://ibb.co/gWQn35j',
                     'url': 'https://i.ibb.co/LgBG8Lk/image.webp', 'display_url': 'https://i.ibb.co/LgBG8Lk/image.webp',
                     'width': 640, 'height': 480, 'size': 7296, 'time': 1708020345, 'expiration': 0,
                     'image': {'filename': 'image.webp', 'name': 'image', 'mime': 'image/webp', 'extension': 'webp',
                               'url': 'https://i.ibb.co/LgBG8Lk/image.webp'},
                     'thumb': {'filename': 'image.webp', 'name': 'image', 'mime': 'image/webp', 'extension': 'webp',
                               'url': 'https://i.ibb.co/gWQn35j/image.webp'},
                     'delete_url': 'https://ibb.co/gWQn35j/27fe43f7d6bd4b32ea9ac0a56e5a1f33'}, 'success': True,
            'status': 200}