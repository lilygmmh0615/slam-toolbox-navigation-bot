import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ListenerNode(Node):
    def __init__(self):
        super().__init__('listener_node')
        # Create a subscription to the same topic used by the publisher
        self.subscription = self.create_subscription(
            String,
            'chatter',  # The topic name must match the publisher
            self.listener_callback,
            10)
        self.get_logger().info('Listener Node has started!')

    def listener_callback(self, msg):
        # This function runs every time a message is received
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = ListenerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()