import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from builtin_interfaces.msg import Duration


class WorldMarkers(Node):
    def __init__(self):
        super().__init__('world_markers')
        self.publisher = self.create_publisher(MarkerArray, '/world_markers', 10)
        self.timer = self.create_timer(1.0, self.publish_markers)

    def publish_markers(self):
        array = MarkerArray()

        box = Marker()
        box.header.stamp = self.get_clock().now().to_msg()
        box.header.frame_id = 'odom'
        box.ns = 'world'
        box.id = 0
        box.type = Marker.CUBE
        box.action = Marker.ADD
        box.pose.position.x = 2.0
        box.pose.position.y = 0.0
        box.pose.position.z = 0.5
        box.pose.orientation.w = 1.0
        box.scale.x = 1.0
        box.scale.y = 1.0
        box.scale.z = 1.0
        box.color.r = 0.8
        box.color.g = 0.4
        box.color.b = 0.0
        box.color.a = 1.0
        box.lifetime = Duration(sec=2)

        array.markers.append(box)
        self.publisher.publish(array)


def main():
    rclpy.init()
    node = WorldMarkers()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
