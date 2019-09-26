from concurrent import futures
import logging
import os
import signal
import time

import grpc


logger = logging.getLogger(__name__)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GRPCServer:
    """Base gRPC server manager"""

    def __init__(self,
                 max_workers=10,
                 handlers=None,
                 interceptors=None,
                 options=None,
                 maximum_concurrent_rpcs=None,
                 grace=None):
        """
        Args:
            max_workers:  The maximum number of threads that can be used to execute the given calls.
            handlers: An optional list of GenericRpcHandlers used for executing RPCs.
                More handlers may be added by calling add_generic_rpc_handlers any time
                before the server is started
            interceptors: An optional list of ServerInterceptor objects that observe
                and optionally manipulate the incoming RPCs before handing them over to
                handlers. The interceptors are given control in the order they are
                specified. This is an EXPERIMENTAL API.
            options: An optional list of key-value pairs (channel args in gRPC runtime)
              to configure the channel.
            maximum_concurrent_rpcs: The maximum number of concurrent RPCs this server
                will service before returning RESOURCE_EXHAUSTED status, or None to
                indicate no limit.
            grace: An optional number of seconds to wait before cancelling all calls
                during the handling the server instance shutdown
        """
        self.instance = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            handlers=handlers,
            interceptors=interceptors,
            options=options,
            maximum_concurrent_rpcs=maximum_concurrent_rpcs
        )
        self.grace = grace

    def schedule_graceful_shutdown(self):
        if self.grace is None:
            return

        def _sigterm_handler(signum, frame):
            logging.info('Shutting down gRPC server with grace. Giving it %s seconds to complete calls', self.grace)
            stop_event = self.instance.stop(self.grace)
            stop_event.wait()
            logging.info('Server is now stopped. Exiting the application.')
            os._exit(0)

        signal.signal(signal.SIGTERM, _sigterm_handler)

    def register_service(self, add_handler, service_class):
        add_handler(service_class(), self.instance)

    def serve_insecure(self, address='[::]', port=50051):
        port_number = self.instance.add_insecure_port('{}:{}'.format(address, port))
        logging.info('Serving gRPC application on port %s...', port_number)
        self.instance.start()
        self.schedule_graceful_shutdown()

        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            self.instance.stop(0)
