import asyncio
from dynamic_measurement import apply_measurement_to_async_methods
from measure_action import measure_action

# IMPORT FROM LOCAL FOLDER
from reviews.analysis_with_cache import process_models_with_cache
from reviews.analysis_without_cache import process_models_without_cache

class FunctionActions:
    def __init__(self, locust_user):
        self.locust_user = locust_user

    async def analyze_reviews_with_cache(self, models_list):
        # DIRECT AWAIT (No to_thread needed anymore)
        result = await process_models_with_cache(models_list)
        return result
    async def analyze_reviews_without_cache(self, models_list):
        # DIRECT AWAIT (No to_thread needed anymore)
        result = await process_models_without_cache(models_list)
        return result

apply_measurement_to_async_methods(FunctionActions, measure_action)