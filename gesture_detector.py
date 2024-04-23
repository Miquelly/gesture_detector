import socket
import config
from typing import Tuple
import matplotlib.pyplot as plt


from utils import colors, corresponding_points
from is_wire.core import Channel, Subscription, Message
from is_msgs.image_pb2 import ObjectAnnotations
from is_msgs.image_pb2 import HumanKeypoints as HKP

class StreamChannel(Channel):
    def __init__(
        self, uri: str = "amqp://guest:guest@localhost:5672", exchange: str = "is"
    ) -> None:
        super().__init__(uri=uri, exchange=exchange)

    def consume_last(self) -> Tuple[Message, int]:
        dropped = 0
        msg = super().consume()
        while True:
            try:
                # will raise an exception when no message remained
                msg = super().consume(timeout=0.0)
                dropped += 1
            except socket.timeout:
                return (msg, dropped)

def plot_lines(ax, lines, x_list, y_list, c_lists):
    # Limpa as linhas anteriores
    
    for line in lines:
        line.set_xdata([])
        line.set_ydata([])

    # Cria novas linhas e as adiciona à lista de linhas
    new_lines = []
    for x, y, c in zip(x_list, y_list, c_lists):
        
        line, = ax.plot(x, y, c)

        new_lines.append(line)

    return new_lines

def main():

    camera_id = config.camera_id
    service_name = "test"
    channel = StreamChannel(f"amqp://10.20.5.2:30000")
    # channel = Channel(f"amqp://10.20.5.2:30000")  ## "broker_uri": "amqp://10.20.5.2:30000"
    assinatura = Subscription(channel, name=service_name)
    assinatura.subscribe(topic=f"SkeletonsDetector.{camera_id}.Detection")

    # Configurações Plot
    plt.ion()
    plt.show(block=False)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1288)
    ax.set_ylim(728, 0)
    plt.title("skeletons_detector")

    lines = []

    while True:
 
        messagem, _ = channel.consume_last()
        # messagem = channel.consume()
        results = messagem.unpack(ObjectAnnotations)

        list_position = {}

        # Listas com as coordenadas das linhas para cada frame
        lists_x_links = []
        lists_y_links = []
        lists_cor_links = []

        for x in results.objects:

            for o in x.keypoints:
                list_position[o.id] =  (o.position.x, o.position.y)

            color_list = colors(config.group, list_position)
            list_links = corresponding_points(config.links, list_position, color_list)

            lists_x_links.append(list_links[0])
            lists_y_links.append(list_links[1])
            lists_cor_links.append(list_links[2])

        # Informações dos n esqueletos detectados
        lx = [item for sublist in lists_x_links for item in sublist]
        ly = [item for sublist in lists_y_links for item in sublist]
        lc = [item for sublist in lists_cor_links for item in sublist]

        # Plot
        lines = plot_lines(ax, lines, lx, ly, lc)
        fig.canvas.draw()
        fig.canvas.flush_events()

        plt.ioff()

if __name__ == "__main__": 
    main()
