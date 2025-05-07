import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener, LookupException, ExtrapolationException
import tf2_geometry_msgs
import numpy as np
import cv2
from cv_bridge import CvBridge
import tkinter as tk
from tkinter import messagebox


class ImageClickTo3DNode(Node):
    def __init__(self):
        super().__init__('image_click_to_3d_node')
        self.bridge = CvBridge()

        # Camera intrinsics
        self.fx = None
        self.fy = None
        self.cx = None
        self.cy = None

        # TF
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.camera_frame = 'camera_link_optical'
        self.base_frame = 'base_link'

        # Subscribers
        self.create_subscription(CameraInfo, '/camera/depth/camera_info', self.camera_info_callback, 10)
        self.create_subscription(Image, '/camera/depth/image_rect_raw', self.depth_image_callback, 10)

        self.latest_depth = None

        # Tkinter setup
        self.window = tk.Tk()
        self.window.title("Camera Depth to Base Link")
        self.label = tk.Label(self.window, text="Click on the image to get 3D coordinates:")
        self.label.pack()

        self.result_label = tk.Label(self.window, text="3D Position: x=0, y=0, z=0")
        self.result_label.pack()

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        # Initialize the image
        self.img = None
        self.tk_img = None

        self.canvas.bind("<Button-1>", self.mouse_callback)

        self.window.after(10, self.update_image)

    def camera_info_callback(self, msg):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]

    def depth_image_callback(self, msg):
        self.latest_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    def update_image(self):
        if self.latest_depth is not None:
            depth_colored = cv2.normalize(self.latest_depth, None, 0, 255, cv2.NORM_MINMAX)
            depth_colored = np.uint8(depth_colored)
            depth_colored = cv2.applyColorMap(depth_colored, cv2.COLORMAP_JET)

            # Convert OpenCV image to Tkinter format
            self.tk_img = cv2.cvtColor(depth_colored, cv2.COLOR_BGR2RGB)
            self.tk_img = cv2.flip(self.tk_img, 0)  # Flip vertically (for Tkinter canvas)
            self.tk_img = Image.fromarray(self.tk_img)
            self.tk_img = ImageTk.PhotoImage(self.tk_img)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

        self.window.after(10, self.update_image)

    def mouse_callback(self, event):
        u, v = event.x, event.y
        if self.fx is None:
            messagebox.showwarning("Warning", "Camera intrinsics not yet received.")
            return

        if self.latest_depth is None:
            messagebox.showwarning("Warning", "No depth image received.")
            return

        depth = self.latest_depth[v, u] / 1000.0  # Convert mm to meters if needed

        if np.isnan(depth) or depth <= 0.0:
            messagebox.showwarning("Warning", "Invalid depth at clicked pixel.")
            return

        # Convert pixel (u, v) to 3D point in camera frame
        x = (u - self.cx) * depth / self.fx
        y = (v - self.cy) * depth / self.fy
        z = depth

        # Build PointStamped message
        point_camera = PointStamped()
        point_camera.header.frame_id = self.camera_frame
        point_camera.header.stamp = self.get_clock().now().to_msg()
        point_camera.point.x = x
        point_camera.point.y = y
        point_camera.point.z = z

        try:
            transform = self.tf_buffer.lookup_transform(
                self.base_frame,
                self.camera_frame,
                rclpy.time.Time()
            )
            point_base = tf2_geometry_msgs.do_transform_point(point_camera, transform)

            # Update the result label
            result_text = f"3D Position in {self.base_frame}: x={point_base.point.x:.3f}, " \
                          f"y={point_base.point.y:.3f}, z={point_base.point.z:.3f}"
            self.result_label.config(text=result_text)

        except (LookupException, ExtrapolationException):
            messagebox.showwarning("Error", "TF transform failed.")


def main():
    rclpy.init()
    node = ImageClickTo3DNode()

    # Run the Tkinter event loop
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            node.window.update()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
