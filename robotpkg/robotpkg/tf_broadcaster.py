import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from gazebo_msgs.msg import LinkStates
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class GazeboTFBroadcaster(Node):
    def __init__(self):
        super().__init__('gazebo_tf_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.subscription = self.create_subscription(
            LinkStates,
            '/link_states',
            self.link_states_callback,
            qos)

    def link_states_callback(self, msg):
        if 'my_robot::base_link' not in msg.name:
            return

        idx = msg.name.index('my_robot::base_link')
        pose = msg.pose[idx]

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = pose.position.x
        t.transform.translation.y = pose.position.y
        t.transform.translation.z = pose.position.z
        t.transform.rotation = pose.orientation

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = GazeboTFBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
