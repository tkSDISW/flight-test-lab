import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String


class FlightTelemetryPublisher(Node):
	def __init__(self):
		super().__init__("flight_telemetry_publisher")

		self.altitude_pub = self.create_publisher(Float64, "/flight/altitude_ft", 10)
		self.airspeed_pub = self.create_publisher(Float64, "/flight/airspeed_kts", 10)
		self.roll_pub = self.create_publisher(Float64, "/flight/roll_deg", 10)
		self.pitch_pub = self.create_publisher(Float64, "/flight/pitch_deg", 10)
		self.yaw_pub = self.create_publisher(Float64, "/flight/yaw_deg", 10)
		self.rpm_pub = self.create_publisher(Float64, "/engine/rpm", 10)
		self.egt_pub = self.create_publisher(Float64, "/engine/egt_c", 10)
		self.phase_pub = self.create_publisher(String, "/flight/phase", 10)

		self.t = 0.0
		self.dt = 0.1
		self.timer = self.create_timer(self.dt, self.publish_telemetry)

	def publish_telemetry(self):
		# 6-minute repeating mission profile
		cycle_time = self.t % 360.0

		if cycle_time < 30:
			phase = "taxi"
			altitude = 0.0
			airspeed = 20.0 + cycle_time
			pitch = 0.0
			rpm = 1200.0
			egt = 420.0

		elif cycle_time < 80:
			phase = "takeoff"
			x = (cycle_time - 30) / 50.0
			altitude = 3000.0 * x
			airspeed = 80.0 + 170.0 * x
			pitch = 8.0
			rpm = 3200.0
			egt = 760.0

		elif cycle_time < 160:
			phase = "climb"
			x = (cycle_time - 80) / 80.0
			altitude = 3000.0 + 27000.0 * x
			airspeed = 250.0 + 80.0 * x
			pitch = 5.0
			rpm = 2900.0
			egt = 700.0

		elif cycle_time < 240:
			phase = "cruise"
			altitude = 30000.0
			airspeed = 430.0
			pitch = 1.5
			rpm = 2500.0
			egt = 640.0

		elif cycle_time < 320:
			phase = "descent"
			x = (cycle_time - 240) / 80.0
			altitude = 30000.0 * (1.0 - x)
			airspeed = 410.0 - 180.0 * x
			pitch = -3.0
			rpm = 1800.0
			egt = 520.0

		else:
			phase = "landing"
			x = (cycle_time - 320) / 40.0
			altitude = 500.0 * (1.0 - x)
			airspeed = 140.0 - 90.0 * x
			pitch = 3.0
			rpm = 1600.0
			egt = 500.0

		roll = 5.0 * math.sin(self.t / 8.0)
		yaw = (self.t * 0.5) % 360.0

		self.publish_float(self.altitude_pub, altitude)
		self.publish_float(self.airspeed_pub, airspeed)
		self.publish_float(self.roll_pub, roll)
		self.publish_float(self.pitch_pub, pitch)
		self.publish_float(self.yaw_pub, yaw)
		self.publish_float(self.rpm_pub, rpm)
		self.publish_float(self.egt_pub, egt)

		phase_msg = String()
		phase_msg.data = phase
		self.phase_pub.publish(phase_msg)

		self.t += self.dt

	def publish_float(self, publisher, value):
		msg = Float64()
		msg.data = float(value)
		publisher.publish(msg)


def main(args=None):
	rclpy.init(args=args)
	node = FlightTelemetryPublisher()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
