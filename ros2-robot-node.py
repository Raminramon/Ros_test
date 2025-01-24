import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class SimpleRobotNode(Node):
    def __init__(self):
        super().__init__('simple_robot_node')
        
        # Publisher for robot movement
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscriber for laser scan data
        self.laser_subscriber = self.create_subscription(
            LaserScan, 
            '/scan', 
            self.laser_callback, 
            10
        )
        
        # Timer for periodic movement
        self.timer = self.create_timer(0.5, self.move_robot)
        
        # Robot state
        self.obstacle_detected = False

    def laser_callback(self, msg):
        # Check for obstacles in front of the robot
        min_distance = min(msg.ranges)
        
        # Set obstacle flag if something is too close (less than 0.5m)
        self.obstacle_detected = min_distance < 0.5
        
        self.get_logger().info(f'Minimum obstacle distance: {min_distance:.2f}m')

    def move_robot(self):
        # Create a velocity message
        vel_msg = Twist()
        
        # If no obstacle, move forward
        if not self.obstacle_detected:
            vel_msg.linear.x = 0.5  # Move forward at 0.5 m/s
            self.get_logger().info('Moving forward')
        else:
            # Stop if obstacle detected
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.5  # Rotate to avoid obstacle
            self.get_logger().info('Obstacle detected! Rotating')
        
        # Publish the velocity command
        self.cmd_vel_publisher.publish(vel_msg)

def main(args=None):
    rclpy.init(args=args)
    robot_node = SimpleRobotNode()
    
    try:
        rclpy.spin(robot_node)
    except KeyboardInterrupt:
        robot_node.get_logger().info('Stopping robot node')
    finally:
        robot_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
