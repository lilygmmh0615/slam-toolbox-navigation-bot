import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math


FORWARD_SPEED = 0.3
TURN_SPEED = 0.5
OBSTACLE_DISTANCE = 0.8  # meters — if anything closer than this, react


class Brain(Node):
    def __init__(self):
        super().__init__('brain')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.on_scan, 10)
        self.get_logger().info('Brain started')

    def stop(self):
        self.cmd_pub.publish(Twist())
        self.get_logger().info('Brain stopped — robot halted')

    def on_scan(self, msg):
        ranges = msg.ranges

        # Split scan into front, left, right sectors
        # index 0 = -180° (behind), index 180 = 0° (forward)
        # front: index 180 ± 30 degrees
        front_indices = list(range(150, 210))
        left_indices  = list(range(210, 270))
        right_indices = list(range(90, 150))

        front_min = self._min_range(ranges, front_indices)
        left_min = self._min_range(ranges, left_indices)
        right_min = self._min_range(ranges, right_indices)

        twist = Twist()

        if front_min < OBSTACLE_DISTANCE:
            # Obstacle ahead — turn away from the closer side
            if left_min > right_min:
                twist.angular.z = TURN_SPEED   # turn left
            else:
                twist.angular.z = -TURN_SPEED  # turn right
            self.get_logger().info(
                f'Obstacle ahead ({front_min:.2f}m) — turning {"left" if twist.angular.z > 0 else "right"}'
            )
        else:
            # Path clear — go forward
            twist.linear.x = FORWARD_SPEED

        self.cmd_pub.publish(twist)

    def _min_range(self, ranges, indices):
        values = [ranges[i] for i in indices if not math.isinf(ranges[i]) and not math.isnan(ranges[i])]
        return min(values) if values else float('inf')


def main():
    rclpy.init()
    node = Brain()
    try:
        rclpy.spin(node)
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
