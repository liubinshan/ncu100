from response import Error, Success, validData


class GetResponse:
    def __init__(self):
        pass

    @validData(Error(400, "错误信息"), Success(200, "成功"))
    def get(self):
        # raise Exception()
        return {
            'data': {1: "ssss", 2: 'dsf'},
            "page": int(),
            "count": int(),
        }


a = GetResponse()
print(a.get())
