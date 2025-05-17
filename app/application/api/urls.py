from ninja import Router

from app.application.api.customers.handlers import router as customer_router
from app.application.api.products.handlers import router as product_router
from app.application.api.products.categories.handlers import router as category_router
from app.application.api.carts.handlers import router as cart_router
from app.application.api.reviews.handlers import router as review_router
from app.application.api.orders.handlers import router as order_router

router = Router(tags=['v1'])

router.add_router('customers/', customer_router)
router.add_router('products/', product_router)
router.add_router('categories/', category_router)
router.add_router('carts/', cart_router)
router.add_router('reviews/', review_router)
router.add_router('orders/', order_router)