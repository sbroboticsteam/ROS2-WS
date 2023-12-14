import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped
import numpy as np


class SimpleController(Node):
    def __init__(self):
        super.__init__('simple_controller')
        self.declare_parameter("wheel_radius",0.033)
        self.declare_parameter("wheel_saperation",0.17)

        self.wheel_radius_ = self.get_parameter("wheel_radius").get_parameter_value().double_value
        self.wheel_saperation_ = self.get_parameter("wheel_saperation").get_parameter_value().double_value

        self.get_logger().info("Using wheel_radius %f" % self.wheel_radius_)
        self.get_logger().info("Using wheel_saperation %f" % self.wheel_saperation_)

        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray,'/simple_velocotiy_controller/commands',10)
        self.vel_sub_ = self.create_subscription(TwistStamped,'tetra_cotroller/cmd_vel',self.velCallback,10)
        self.get_logger().info(self.sped_conversioin_)
        self.sped_conversioin_ = np.array([self.wheel_radius_/2,self.wheel_radius_/2],
                                          [self.wheel_radius_/self.wheel_saperation_,self.wheel_radius_/self.wheel_saperation_])
        self.get_logger().info(self.sped_conversioin_)
        
        
    
    def velCallback(self,msg):
        robot_speed = np.array([msg.twist.linear.x],[msg.twist.angular.z])
        wheel_speed = np.matmul(np.linalg.inv(self.sped_conversioin_),robot_speed) 
        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [wheel_speed[1,0],wheel_speed[0,0]]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

def main():
    rclpy.init()
    simple_contoller = SimpleController()
    rclpy.spin(simple_contoller)
    simple_contoller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()