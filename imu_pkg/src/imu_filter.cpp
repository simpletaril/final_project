
/*
The gyroscopes tend to have a low-frequency drift, while the accelerometers and magnetometers tend to have a high-frequency noise.
The complementary filter simple “combines” these two signals,
yielding the benefit of eliminating the drift from the gyroscope and noise from the accelerometer.
*/

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include <cmath>

class ComplementaryFilterNode : public rclcpp::Node
{
public:
    ComplementaryFilterNode()
        : Node("complementary_filter_node"), alpha_(0.98), dt_(0.01)
    {
        // Subscribe to the raw IMU topic
        imu_subscriber_ = this->create_subscription<sensor_msgs::msg::Imu>(
            "/data/imu", 10, std::bind(&ComplementaryFilterNode::imuCallback, this, std::placeholders::_1));

        // Publisher for the filtered IMU data
        filtered_imu_publisher_ = this->create_publisher<sensor_msgs::msg::Imu>("/imu/filtered", 10);

        RCLCPP_INFO(this->get_logger(), "Complementary Filter Node Initialized");
    }

private:
    void imuCallback(const sensor_msgs::msg::Imu::SharedPtr msg)
    {
        // Extract raw accelerometer and gyroscope data
        double ax = msg->linear_acceleration.x;
        double ay = msg->linear_acceleration.y;
        double az = msg->linear_acceleration.z;
        double gx = msg->angular_velocity.x;
        double gy = msg->angular_velocity.y;
        double gz = msg->angular_velocity.z;

        // Compute accelerometer-based pitch and roll
        double accel_pitch = atan2(ax, sqrt(ay * ay + az * az)) * 180.0 / M_PI;
        double accel_roll = atan2(ay, sqrt(ax * ax + az * az)) * 180.0 / M_PI;

        // Integrate gyroscope data for pitch, roll, and yaw
        pitch_ += gx * dt_;
        roll_ += gy * dt_;
        yaw_ += gz * dt_; // Yaw estimation (gyro-only)

        // Apply complementary filter for pitch and roll
        pitch_ = alpha_ * pitch_ + (1 - alpha_) * accel_pitch;
        roll_ = alpha_ * roll_ + (1 - alpha_) * accel_roll;

        // Filter accelerometer data (simple moving average for noise reduction)
        filtered_ax_ = alpha_ * filtered_ax_ + (1 - alpha_) * ax;
        filtered_ay_ = alpha_ * filtered_ay_ + (1 - alpha_) * ay;
        filtered_az_ = alpha_ * filtered_az_ + (1 - alpha_) * az;

        // Filter gyroscope data
        filtered_gx_ = alpha_ * filtered_gx_ + (1 - alpha_) * gx;
        filtered_gy_ = alpha_ * filtered_gy_ + (1 - alpha_) * gy;
        filtered_gz_ = alpha_ * filtered_gz_ + (1 - alpha_) * gz;

        // Create and publish the filtered IMU message
        auto filtered_msg = sensor_msgs::msg::Imu(*msg);
        filtered_msg.orientation.x = pitch_;
        filtered_msg.orientation.y = roll_;
        filtered_msg.orientation.z = yaw_;
        filtered_msg.linear_acceleration.x = filtered_ax_;
        filtered_msg.linear_acceleration.y = filtered_ay_;
        filtered_msg.linear_acceleration.z = filtered_az_;
        filtered_msg.angular_velocity.x = filtered_gx_;
        filtered_msg.angular_velocity.y = filtered_gy_;
        filtered_msg.angular_velocity.z = filtered_gz_;
        filtered_imu_publisher_->publish(filtered_msg);

        RCLCPP_INFO(this->get_logger(), "Filtered data - Pitch: %.2f, Roll: %.2f, Yaw: %.2f", pitch_, roll_, yaw_);
    }

    rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_subscriber_;
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr filtered_imu_publisher_;

    double alpha_; // Complementary filter coefficient
    double dt_;    // Time step

    // Orientation (pitch, roll, yaw)
    double pitch_ = 0.0;
    double roll_ = 0.0;
    double yaw_ = 0.0;

    // Filtered accelerometer and gyroscope data
    double filtered_ax_ = 0.0;
    double filtered_ay_ = 0.0;
    double filtered_az_ = 0.0;
    double filtered_gx_ = 0.0;
    double filtered_gy_ = 0.0;
    double filtered_gz_ = 0.0;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ComplementaryFilterNode>());
    rclcpp::shutdown();
    return 0;
}
