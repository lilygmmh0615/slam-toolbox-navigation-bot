import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class Mover(Node):
    def __init__(self):
        super().__init__('mover_node')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(0.05, self.timer_callback) # 20Hz
        self.angle = 0.0

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['arm_joint']
        # Create a swinging motion using a sine wave
        self.angle += 0.05
        msg.position = [math.sin(self.angle)] 
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = Mover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()