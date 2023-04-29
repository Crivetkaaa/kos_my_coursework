
class Reader:

    @staticmethod
    def read_file(check):
        file_name = 'Приходная' if check else 'Расходная'
        data = []
        with open(f'files/{file_name}_накладная.txt', 'r', encoding='utf-8') as file:
            rows = file.readlines()
            for row in rows:
                data.append(row)
        return data
    
    @staticmethod
    def clear(check):
        file_name = 'Приходная' if check else 'Расходная'
        with open(f'files/{file_name}_накладная.txt', 'w', encoding='utf-8') as file:
            file.close()
