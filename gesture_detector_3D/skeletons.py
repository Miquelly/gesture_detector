import socket
import colorsys
from itertools import permutations
from typing import List

import cv2
import sys
from google.protobuf.json_format import ParseDict


from is_msgs.image_pb2 import HumanKeypoints as HKP
from is_msgs.image_pb2 import ObjectAnnotations
from is_wire.core import Channel, Message, Subscription
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from gesture import gesture

matplotlib.use("Agg")


class CustomChannel(Channel):
    def __init__(
        self,
        uri: str = "amqp://guest:guest@localhost:5672",
        exchange: str = "is",
    ) -> None:
        super().__init__(uri=uri, exchange=exchange)

    def consume_all(self) -> List[Message]:
        messages = []
        message = super().consume()
        messages.append(message)
        while True:
            try:
                message = super().consume(timeout=0.0)
                messages.append(message)
            except socket.timeout:
                return messages


class App(object):
    def __init__(
        self,
        group_id: int = 0,
        broker_uri: str = "amqp://guest:guest@localhost:5672",
    ) -> None:
        self.channel = CustomChannel(uri=broker_uri, exchange="is")
        self.subscription = Subscription(channel=self.channel, name="app2")
        self.subscription.subscribe(f"SkeletonsGrouper.{group_id}.Localization")
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(projection="3d")

        self.colors = list(permutations([0, 255, 85, 170], 3))
        self.links = [
            # (HKP.Value("HEAD"), HKP.Value("NECK")),
            # (HKP.Value("NECK"), HKP.Value("CHEST")),
            # (HKP.Value("CHEST"), HKP.Value("RIGHT_HIP")),
            # (HKP.Value("CHEST"), HKP.Value("LEFT_HIP")),
            # (HKP.Value("NECK"), HKP.Value("LEFT_SHOULDER")),
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("RIGHT_SHOULDER")),
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("LEFT_HIP")),
            (HKP.Value("RIGHT_SHOULDER"), HKP.Value("RIGHT_HIP")),
            (HKP.Value("LEFT_HIP"), HKP.Value("RIGHT_HIP")),
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("LEFT_EAR")),
            (HKP.Value("RIGHT_SHOULDER"), HKP.Value("RIGHT_EAR")),
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("LEFT_ELBOW")),
            (HKP.Value("LEFT_ELBOW"), HKP.Value("LEFT_WRIST")),
            # (HKP.Value("NECK"), HKP.Value("LEFT_HIP")),
            (HKP.Value("LEFT_HIP"), HKP.Value("LEFT_KNEE")),
            (HKP.Value("LEFT_KNEE"), HKP.Value("LEFT_ANKLE")),
            # (HKP.Value("NECK"), HKP.Value("RIGHT_SHOULDER")),
            (HKP.Value("RIGHT_SHOULDER"), HKP.Value("RIGHT_ELBOW")),
            (HKP.Value("RIGHT_ELBOW"), HKP.Value("RIGHT_WRIST")),
            # (HKP.Value("NECK"), HKP.Value("RIGHT_HIP")),
            (HKP.Value("RIGHT_HIP"), HKP.Value("RIGHT_KNEE")),
            (HKP.Value("RIGHT_KNEE"), HKP.Value("RIGHT_ANKLE")),
            (HKP.Value("NOSE"), HKP.Value("LEFT_EYE")),
            (HKP.Value("LEFT_EYE"), HKP.Value("LEFT_EAR")),
            (HKP.Value("NOSE"), HKP.Value("RIGHT_EYE")),
            (HKP.Value("RIGHT_EYE"), HKP.Value("RIGHT_EAR")),
        ]

        comparator =  HKP.Value("NOSE")
        self.group = [
                    (HKP.Value("LEFT_WRIST"), comparator),
                    (HKP.Value("RIGHT_WRIST"), comparator),
                    ]
        
        self.list_id = {}

    def _id_to_rgb_color(self, id, id_color):
        # Calcula a matiz (cor) com base no ID usando o operador módulo
        hue = (id % id_color) / id_color
        # Define uma saturação e luminosidade fixas para cores vibrantes
        saturation = 0.8
        luminance = 0.6
        # Converte a cor de HSL para RGB
        r, g, b = [x for x in colorsys.hls_to_rgb(hue, luminance, saturation)]
        return r, g, b

    def render_skeletons_3d(self, skeletons):

        for skeleton in skeletons.objects:
            parts = {}
            for part in skeleton.keypoints:
                parts[part.id] = (part.position.x, part.position.y, part.position.z)

            id_color = gesture(self.group, parts)
            
            for link_parts in self.links:
                begin, end = link_parts
                if begin in parts and end in parts:
                    x_pair = [parts[begin][0], parts[end][0]]
                    y_pair = [parts[begin][1], parts[end][1]]
                    z_pair = [parts[begin][2], parts[end][2]]
                    color = self._id_to_rgb_color(id=skeleton.id, id_color=id_color)
                    self.ax.plot(
                        x_pair,
                        y_pair,
                        zs=z_pair,
                        linewidth=3,
                        color=color,
                    )

    def run(self) -> None:
        plt.ioff()
        while True:
        
            messages = self.channel.consume_all()
            for message in messages:
                objs = message.unpack(ObjectAnnotations)
                self.ax.clear()
                self.ax.view_init(azim=0, elev=20)
                self.ax.set_xlim(-4, 4)
                self.ax.set_xticks(np.arange(-4, 4, 1))
                self.ax.set_ylim(-4, 4)
                self.ax.set_yticks(np.arange(-4, 4, 1))
                self.ax.set_zlim(-0.25, 2)
                self.ax.set_zticks(np.arange(0, 2, 0.5))
                self.ax.set_xlabel("X", labelpad=20)
                self.ax.set_ylabel("Y", labelpad=10)
                self.ax.set_zlabel("Z", labelpad=5)
                self.render_skeletons_3d(objs)
                self.fig.canvas.draw()
                
                # generate a image from a matplotlib figure
                data = np.fromstring(
                    self.fig.canvas.tostring_rgb(), dtype=np.uint8, sep=""
                )
                view_3d = data.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
                cv2.imshow("", view_3d)
                key = cv2.waitKey(1)
                if key == ord("q"):
                    return
                # plt.show(block=False)
                # self.ax.clear()


if __name__ == "__main__":
    app = App(broker_uri="amqp://guest:guest@10.20.5.2:30000")
    app.run()
