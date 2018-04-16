from concurrent import futures
import time
import grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GRPCServer:
    """Base gRPC server manager"""

    def __init__(self, max_workers=10):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

    def register_service(self, add_handler, service_class):
        add_handler(service_class(), self.server)

    def serve_insecure(self, address='[::]', port=50051):
        self.server.add_insecure_port('{}:{}'.format(address, port))
        self.server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            self.server.stop(0)