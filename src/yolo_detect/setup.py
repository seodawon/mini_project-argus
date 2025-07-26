from setuptools import find_packages, setup

package_name = 'yolo_detect'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rokey',
    maintainer_email='rokey@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imagePub = yolo_detect.imagePub:main',
            'imageSub = yolo_detect.imageSub:main',
            'yolopub = yolo_detect.yolo_publisher:main',
            'yolosub = yolo_detect.yolo_subscriber:main',
            'yolo8_obj = yolo_detect.yolov8_obj_det_wc:main',
        ],
    },
)
