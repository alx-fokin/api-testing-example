# INPUTS SECTION
test_number = 'DELETED FOR REPO VERSION'
valid_numbers = ('DELETED FOR REPO VERSION', )

invalid_numbers = ('DELETED FOR REPO VERSION', )

invalid_creds = ('%25s', '%25d', '$$$$$$$$', '????????', '********', '........', '""', "''",
                 'SELECT * FROM TABLE OR 1=1;', 'api_key', 'api_secret', '((()))', '{{{}}}',
                 '[[[]]]', '^^^^^^', '00000000', '11111111', '12345678', '12abcdef', 'admin', 'root')

valid_brands = ('A', '888ABC', 'XYZ999', 'ABCDEFABCDEFABCDEF', ':):):)', '$$$%25%25%25@@@')

invalid_brands = ('ABCDEFABCDEFABCDEFA', '12345678901234567890')

valid_country = ('RU',)

invalid_country = ('R', 'RUS')

valid_code_length = ('4', '6', '00004', '06', '0000000000000000000004')

invalid_numeric_code_length = ('0', '-1', '999999', '3', '5', '7')

invalid_nonnumeric_code_length = ('4.0', '6.0', '%25s', '%25d', '8/2', '9%255', '%2B4', '6%2B', '=4')

valid_sender_id = ('VERIFY', 'Check', '123Check', 'Проверка', 'Тестxyz', 'ABCDEFABCDE')

invalid_sender_id = ('VERIFYVERIFY', 'ПРОВЕРКАПРОВЕРКА')

invalid_language = ('%25s%25d', '%25%25^^//??!!', '----------', '>>>>>>>', '??????', 'rururu', 'enenen',
                    'en_us', 'ru_ru', 'ruru' 'dede')

invalid_code = ('%25s', '%25d', '????', '1-34', '!!%25%25')

invalid_cmd = ('delete', 'resend', 'destroy', '0123456789', '%25%25$$^^**@@')

valid_request_ids = ('cd962ff5575e4dffb864bf26726d05db', '3e75e2e9dd9d465e88d8698a0fb490c3',
                     '361f300fc976490bb27383c993f042f7', '7cc7d1e655fc434884667185d41be20f')

invalid_request_ids = ('f58598c41da948fca0e9a9480a3821834', )

verified_request_id = ('f58598c41da948fca0e9a9480a382183', )
