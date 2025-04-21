from ninja import Router

from app.application.api.customers.handlers import router as customer_router
from app.application.api.products.handlers import router as product_router
from app.application.api.products.categories.handlers import router as category_router

router = Router(tags=['v1'])

router.add_router('customers/', customer_router)
router.add_router('products/', product_router)
router.add_router('categories/', category_router)