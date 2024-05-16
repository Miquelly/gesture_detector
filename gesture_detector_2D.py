import socket
from typing import Tuple
import matplotlib.pyplot as plt


from is_msgs.image_pb2 import ObjectAnnotations
from is_msgs.image_pb2 import HumanKeypoints as HKP
from is_wire.core import Channel, Subscription, Message

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

def plot_lines(ax, lines, coordenadas_x, coordenadas_y, colors):
    # Limpa as linhas anteriores
    for line in lines:
        line.set_xdata([])
        line.set_ydata([])

    # Cria novas linhas e as adiciona à lista de linhas
    new_lines = []
    for x, y, color in zip(coordenadas_x, coordenadas_y, colors):
        
        line, = ax.plot(x, y, color)

        new_lines.append(line)

    return new_lines

def main():

    camera_id = 1
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

    links = {
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("RIGHT_SHOULDER")),
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("LEFT_HIP")),
            (HKP.Value("RIGHT_SHOULDER"), HKP.Value("RIGHT_HIP")),
            (HKP.Value("LEFT_HIP"), HKP.Value("RIGHT_HIP")),
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("LEFT_EAR")),
            (HKP.Value("RIGHT_SHOULDER"), HKP.Value("RIGHT_EAR")),
            (HKP.Value("LEFT_SHOULDER"), HKP.Value("LEFT_ELBOW")),
            (HKP.Value("LEFT_ELBOW"), HKP.Value("LEFT_WRIST")),
            (HKP.Value("LEFT_HIP"), HKP.Value("LEFT_KNEE")),
            (HKP.Value("LEFT_KNEE"), HKP.Value("LEFT_ANKLE")),
            (HKP.Value("RIGHT_SHOULDER"), HKP.Value("RIGHT_ELBOW")),
            (HKP.Value("RIGHT_ELBOW"), HKP.Value("RIGHT_WRIST")),
            (HKP.Value("RIGHT_HIP"), HKP.Value("RIGHT_KNEE")),
            (HKP.Value("RIGHT_KNEE"), HKP.Value("RIGHT_ANKLE")),
            (HKP.Value("NOSE"), HKP.Value("LEFT_EYE")),
            (HKP.Value("LEFT_EYE"), HKP.Value("LEFT_EAR")),
            (HKP.Value("NOSE"), HKP.Value("RIGHT_EYE")),
            (HKP.Value("RIGHT_EYE"), HKP.Value("RIGHT_EAR")),
    }

    while True:
 
        messagem, _ = channel.consume_last()
        results = messagem.unpack(ObjectAnnotations)

        list_position = {} 

        coordenadas_x = []
        coordenadas_y = []
        colors = []

        for x in results.objects:

            for o in x.keypoints:
                list_position[o.id] =  (o.position.x, o.position.y)

            if list_position[HKP.Value("RIGHT_WRIST")][1] < list_position[HKP.Value("NOSE")][1]:    

                if list_position[HKP.Value("LEFT_WRIST")][1] < list_position[HKP.Value("NOSE")][1]:
                    color = 'g-'
                else: 
                    color = 'r-'

            else:

                if list_position[HKP.Value("LEFT_WRIST")][1] < list_position[HKP.Value("NOSE")][1]:
                    color = '#EEAD2D'
                else: 
                    color = 'b-'

            for link in links:
                if link[0] in list_position and link[1] in list_position:

                    coordenadas_x.append([list_position[link[0]][0], list_position[link[1]][0]])
                    coordenadas_y.append([list_position[link[0]][1], list_position[link[1]][1]])
                    colors.append(color)

        lines = plot_lines(ax, lines, coordenadas_x, coordenadas_y, colors)
        fig.canvas.draw()
        fig.canvas.flush_events()

        plt.ioff()

if __name__ == "__main__": 
    main()