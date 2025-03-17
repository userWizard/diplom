from ninja import Router

from api.customers.handlers import router as customer_router

router = Router(tags=['v1'])

router.add_router('customers/', customer_router)