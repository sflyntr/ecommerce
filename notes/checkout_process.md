# Checkout Process

- Cart
    - 먼저 쇼핑몰에 접속을 하는 순간 세션 하나가 생긴다.
    - 로그인을 하지 않더라도 쇼핑을 하고 장바구니에 담는다.
    - 이 장바구니에 담긴 정보는 로그인을 안해도 계속 남아있다.
    - 강제로 로그아웃을 하거나(로그아웃 메뉴가 있다.) 시간이 지나면 expire된다.
    - 로그인이 안된 상태에서 로그인을 하면 그 장바구니 담긴 정보는 그대로 살아있다.
    - 하지만 로그인후 로그아웃 하면 그 장바구니 정보는 모두 없어진다.
    - 또한 게스트 상태에서 장바구니에 담고 모든 창을 다 닫은 후 1분뒤에 다시 크롬을 열어 들어가면 그대로 장바구니에 있다.
    - 시간이 많이 지나면 없어지리라.
    - 단 시크릿창을 열면 장바구니에 아무것도 없다.
    - 이것이 Cart이다.   

# Checkout Process

1. Cart -> Checkout View
    ?
    - Login/Register or Enter an Email (as Guest)
    - Shipping Address
    - Billing Info
        - Billing Address
        - Credit Card / Payment

2. Billing App/Component
    - Billing Profile
        - User or Email (Guest Email)
        - generate payment processor token(Strip or Braintree)

3. Orders / Invoices Component
    - Connecting the Billing Address
    - Shipping / Billing Address
    - Cart
    - Status -- Shipped? Cancelled?