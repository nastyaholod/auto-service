import grpc
import catalog_pb2
import catalog_pb2_grpc

class CatalogGrpcClient:
    def __init__(self, host: str, port: int):
        self._channel = grpc.aio.insecure_channel(f"{host}:{port}")
        self._stub = catalog_pb2_grpc.CatalogServiceStub(self._channel)

    async def check_stock(self, part_id: str, quantity: int) -> tuple[bool, str]:
        try:
            request = catalog_pb2.CheckStockRequest(part_id=part_id, quantity=quantity)
            response = await self._stub.CheckStock(request)
            return response.is_available, response.message
        except grpc.RpcError as e:
            return False, f"gRPC ошибка: {e.details()}"

    async def close(self):
        await self._channel.close()