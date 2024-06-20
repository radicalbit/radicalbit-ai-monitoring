from fastapi import APIRouter


class HealthcheckRoute:
    @staticmethod
    def get_healthcheck_route() -> APIRouter:
        router = APIRouter(tags=['status_api'])

        @router.get('/healthcheck')
        def healthcheck():
            return {'status': 'alive'}

        return router
