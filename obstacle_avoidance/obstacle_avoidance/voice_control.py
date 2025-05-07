import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import speech_recognition as sr
import time

class VoiceControlNode(Node):
    def __init__(self):
        super().__init__('voice_control_node')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen_and_execute(self):
        with self.microphone as source:
            self.get_logger().info("Say a command...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio).lower()
            self.get_logger().info(f"You said: {text}")
            self.execute_command(text)
        except sr.UnknownValueError:
            self.get_logger().warn("Could not understand audio")
        except sr.RequestError:
            self.get_logger().warn("Speech Recognition service error")

    def execute_command(self, text):
        twist = Twist()
        duration = 0

        if "forward" in text:
            twist.linear.x = 1.0
        elif "backward" in text:
            twist.linear.x = -1.0
        elif "left" in text:
            twist.angular.z = 1.0
        elif "right" in text:
            twist.angular.z = -1.0
        else:
            self.get_logger().info("No valid direction found.")
            return

        for word in text.split():
            if word.isdigit():
                duration = int(word)

        self.get_logger().info(f"Executing for {duration} seconds")

        start = time.time()
        while time.time() - start < duration:
            self.publisher.publish(twist)
            time.sleep(0.1)

        self.publisher.publish(Twist())

def main(args=None):
    rclpy.init(args=args)
    node = VoiceControlNode()

    try:
        while rclpy.ok():
            node.listen_and_execute()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
