# def parameters. args, argv
# *args : sequence arguments, '*': just sign not pointer or something.
# **kwargs : keyword arguments, '**': just sign, this is keyword argument and key, value pair(dictionary)


def param_test(*args, **kwargs):
    for i in args:
        print(i)

    for k, v in kwargs.items():
        print('key: ' + k + ' value:' + v)


param_test('hello', 'world', 'Yo')
print('-------------------------')
param_test('hello', 'world', 'Yo', name='dosjung', age='30')

class Test:
    pass

test_a = Test()
test_b = Test()
test_c = Test()

test_d = [test_a, test_b, test_c]
type(test_d)
# <class 'list'>

test_d
# [<Test object at 0x10665d668>, <Test object at 0x105dfa780>, <Test object at 0x1072dab38>]

# [] : 리스트를 의미한다. <>: object를 의미한다. <Test>는 type,즉 클래스를 의미한다.
# 따라서 위는 Test object at 주소들의 리스트를 의미한다는 뜻이다.

# qs = Product.objects.all()
# type(qs)
# <class 'django.db.models.query.QuerySet'>
# 즉 QuerySet 클래스를 의미한다.

# qs
# <QuerySet [<Product: T-shirts>, <Product: Hat>]>
# <> 이게 먼저 나오니, QuerySet 클래스의 오브젝트를 의미한다. 근데 주소가 안나온다. 이유는?
# 이거 아무래도 lazy(generator) 라서 당장 주소값이 없나? 여튼 나중에 다시 생각해보자.


# QueyrSet Class : 참조 : https://github.com/django/django/blob/master/django/db/models/query.py
# Represent a lazy database lookup for a set of objects
# 쿼리셋에 대해서는 점차 익숙해지면서 공부하자.