from argus_msgs.srv import DangerClass
import rclpy
from rclpy.node import Node
import random

class Service_client(Node):
    def __init__(self):
        super().__init__('service_client')

        self.service_client = self.create_client(DangerClass,
                                                 'danger')
        while not self.service_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning("service server service not available")

    def send_request(self):
        service_request = DangerClass.Request()
        service_request.danger = random.randint(0,1) # 여기서 어떤 것을 보낼지 결정
        futures = self.service_client.call_async(service_request)
        return futures


def main(args=None):
    rclpy.init(args=args)
    service_client = Service_client() # service client
    futures = service_client.send_request()
    while rclpy.ok():
        rclpy.spin_once(service_client)
        if futures.done():
            try:
                service_response = futures.result().response_result
            except Exception as e :
                service_client.get_logger().warn('service call failed %r' %(e, ))
            else:
                service_client.get_logger().info(f'{service_response}') # display
            break
    service_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()