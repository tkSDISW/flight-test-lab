from setuptools import setup

package_name = "flight_telemetry"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        (
            "share/" + package_name,
            ["package.xml"],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Tony Komar",
    maintainer_email="tony.komar@opensunpower.com",
    description="Synthetic flight telemetry generator",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "telemetry_publisher = flight_telemetry.telemetry_publisher:main",
        ],
    },
)