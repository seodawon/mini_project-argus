import rclpy as rp
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
from argus_msgs.srv import DangerClass
import random

class TopicTest(Node):
    def __init__(self):
        super().__init__('topic_test')
        self.subscribtion = self.create_subscription(
            BatteryState ,'/robot6/battery_state', self.callback,10
        )
        self.batteryPercent = 0
        

    def callback(self,msg): # 5 second hzㅁ
        self.batteryPercent = msg
        self.get_logger().info('battery'+ str(self.batteryPercent.percentage))
        self.destroy_subscription(self.subscribtion)
        if self.batteryPercent.percentage > 0.2:
            self.service_client = self.create_client(DangerClass,
                                                 'danger')
            while not self.service_client.wait_for_service(timeout_sec=1.0):
                self.get_logger().warning("service server service not available")
            self.send_request()

    def send_request(self):
        service_request = DangerClass.Request()
        service_request.danger = random.randint(0,1) # 여기서 어떤 것을 보낼지 결정
        self.get_logger().info('battery'+ str(self.batteryPercent.percentage))
        futures = self.service_client.call(service_request)
        self.get_logger().info('battery'+ str(self.batteryPercent.percentage))

        return futures
def main():
    rp.init(args=None)

    topic_test = TopicTest()
    rp.spin(topic_test)
    topic_test.destroy_node()
    rp.shutdown()
if __name__ == '__main__':
    main()