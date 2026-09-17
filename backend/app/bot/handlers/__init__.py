from app.bot import router

def setup_handlers(dp):
    dp.include_router(router)
