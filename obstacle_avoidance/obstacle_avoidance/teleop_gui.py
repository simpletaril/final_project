#advance gui:

import rclpy
from rclpy.node import Node
import tkinter as tk
from geometry_msgs.msg import Twist
import time


class TeleopGui(Node):
    def __init__(self):
        super().__init__('teleop_gui')

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.velocity_msg = Twist()

        self.linear_speed = 0.5
        self.angular_speed = 0.5

        self.window = tk.Tk()
        self.window.title("Teleop GUI")

        self.running = True
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        frame = tk.Frame(self.window)
        frame.pack()

        # Arrow buttons
        tk.Button(frame, text="↑", width=5, height=2, command=self.button_up).grid(row=0, column=1)
        tk.Button(frame, text="←", width=5, height=2, command=self.button_left).grid(row=1, column=0)
        tk.Button(frame, text="⏹", width=5, height=2, command=self.stop_robot).grid(row=1, column=1)
        tk.Button(frame, text="→", width=5, height=2, command=self.button_right).grid(row=1, column=2)
        tk.Button(frame, text="↓", width=5, height=2, command=self.button_down).grid(row=2, column=1)

        # Speed sliders
        tk.Label(self.window, text="Linear Speed").pack()
        self.linear_slider = tk.Scale(self.window, from_=0.0, to=4.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.linear_slider.set(self.linear_speed)
        self.linear_slider.pack()

        tk.Label(self.window, text="Angular Speed").pack()
        self.angular_slider = tk.Scale(self.window, from_=0.0, to=4.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.angular_slider.set(self.angular_speed)
        self.angular_slider.pack()

    def bind_keys(self):
        self.window.bind('<w>', lambda event: self.button_up())
        self.window.bind('<s>', lambda event: self.button_down())
        self.window.bind('<a>', lambda event: self.button_left())
        self.window.bind('<d>', lambda event: self.button_right())
        self.window.bind('<q>', lambda event: self.stop_robot())

    def button_up(self):
        self.update_speeds()
        self.velocity_msg.linear.x = self.linear_speed
        self.velocity_msg.angular.z = 0.0
        self.publish_velocity()

    def button_down(self):
        self.update_speeds()
        self.velocity_msg.linear.x = -self.linear_speed
        self.velocity_msg.angular.z = 0.0
        self.publish_velocity()

    def button_left(self):
        self.update_speeds()
        self.velocity_msg.linear.x = 0.0
        self.velocity_msg.angular.z = self.angular_speed
        self.publish_velocity()

    def button_right(self):
        self.update_speeds()
        self.velocity_msg.linear.x = 0.0
        self.velocity_msg.angular.z = -self.angular_speed
        self.publish_velocity()

    def stop_robot(self):
        self.velocity_msg.linear.x = 0.0
        self.velocity_msg.angular.z = 0.0
        self.publish_velocity()

    def update_speeds(self):
        self.linear_speed = self.linear_slider.get()
        self.angular_speed = self.angular_slider.get()

    def publish_velocity(self):
        self.cmd_vel_pub.publish(self.velocity_msg)

    def on_closing(self):
        self.stop_robot()
        self.running = False
        self.window.quit()


def main(args=None):
    rclpy.init(args=args)
    node = TeleopGui()

    while node.running:
        rclpy.spin_once(node, timeout_sec=0.1)
        node.window.update_idletasks()
        node.window.update()
        time.sleep(0.01)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()






















# regular gui:
# import rclpy
# from rclpy.node import Node
# import tkinter as tk
# from geometry_msgs.msg import Twist
# import time


# class TeleopGui(Node):
#     def __init__(self):
#         super().__init__('teleop_gui')

#         self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
#         self.velocity_msg = Twist()

#         self.window = tk.Tk()
#         self.window.title("Teleop GUI")
#         self.create_buttons()

#         self.running = True
#         self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def create_buttons(self):
#         frame = tk.Frame(self.window)
#         frame.pack()

#         tk.Button(frame, text="↑", width=5, height=2, command=self.button_up).grid(row=0, column=1)
#         tk.Button(frame, text="←", width=5, height=2, command=self.button_left).grid(row=1, column=0)
#         tk.Button(frame, text="⏹", width=5, height=2, command=self.stop_robot).grid(row=1, column=1)
#         tk.Button(frame, text="→", width=5, height=2, command=self.button_right).grid(row=1, column=2)
#         tk.Button(frame, text="↓", width=5, height=2, command=self.button_down).grid(row=2, column=1)

#     def button_up(self):
#         self.velocity_msg.linear.x = 0.5
#         self.velocity_msg.angular.z = 0.0
#         self.publish_velocity()

#     def button_down(self):
#         self.velocity_msg.linear.x = -0.5
#         self.velocity_msg.angular.z = 0.0
#         self.publish_velocity()

#     def button_left(self):
#         self.velocity_msg.linear.x = 0.0
#         self.velocity_msg.angular.z = 1.0
#         self.publish_velocity()

#     def button_right(self):
#         self.velocity_msg.linear.x = 0.0
#         self.velocity_msg.angular.z = -1.0
#         self.publish_velocity()

#     def stop_robot(self):
#         self.velocity_msg.linear.x = 0.0
#         self.velocity_msg.angular.z = 0.0
#         self.publish_velocity()

#     def publish_velocity(self):
#         self.cmd_vel_pub.publish(self.velocity_msg)

#     def on_closing(self):
#         self.stop_robot()
#         self.running = False
#         self.window.quit()


# def main(args=None):
#     rclpy.init(args=args)
#     node = TeleopGui()

#     # Main loop: handle GUI + ROS spinning
#     while node.running:
#         rclpy.spin_once(node, timeout_sec=0.1)
#         node.window.update_idletasks()
#         node.window.update()
#         time.sleep(0.01)

#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

