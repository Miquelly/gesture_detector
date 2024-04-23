from is_msgs.image_pb2 import HumanKeypoints as HKP

camera_id = "0"

array_color = ['b-', '#EEAD2D', 'r-', 'g-']

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

comparator =  HKP.Value("NOSE")
group = [
            (HKP.Value("LEFT_WRIST"), comparator),
            (HKP.Value("RIGHT_WRIST"), comparator),
            ]