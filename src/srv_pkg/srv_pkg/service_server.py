from argus_msgs.srv import DangerClass
from rclpy.node import Node
import rclpy

class Service_server(Node):
    def __init__(self):
        super().__init__('service_server') 
        self.get_logger().info("service server ready!")
        self.service_server = self.create_service(DangerClass,
                                                  'danger',
                                                  self.get_danger
                                                  )
        
    def get_danger(self,request,response):
        if request.danger == 0:
            self.argument_result = "claymor"
        else:
            self.argument_result = "enemy"
        response.response_result = self.argument_result
        self.get_logger().info("response complete!")
        return response

def main(args=None):
    rclpy.init(args=args)
    executor = Service_server()
    rclpy.spin(executor)
    executor.service_server.destroy() # closed
    executor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
