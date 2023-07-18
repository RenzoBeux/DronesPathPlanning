from os import listdir
from classes import coordObject, Obstacle
from torch import device, cuda, tensor


class Constants_Class(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Constants_Class, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.set_uav_amount_and_time()
        self.set_device()

    def set_uav_amount_and_time(self):
        input_files = listdir("./input")
        single_file = listdir(f"./input/{input_files[0]}")
        file = open(f"./input/{input_files[0]}/{single_file[0]}", "r")
        file_lines = file.readlines()
        file.close()
        file_routes = list(map(lambda x: [list(map(int, x.split(" ")))], file_lines))
        files_tensor_routes = tensor(file_routes, dtype=int)
        self.uav_amount = files_tensor_routes.shape[0]
        self.time_lenght = files_tensor_routes.shape[2]

    def set_device(self):
        self.device = device("cuda" if cuda.is_available() else "cpu")

    def set_flat_obstacles(self, areaDims: coordObject):
        """
        Returns a list of all of the coordinates which are considered occupied by obstacles
        """
        obstaclesBySections: list[list[coordObject]] = list(
            map(lambda obs: obs.toSections(self.DIM), self.OBSTACLES)
        )
        flat_obs: list[coordObject] = []
        # Suboptimal as all hell
        for sectionList in obstaclesBySections:
            for section in sectionList:
                isAccounted = False
                for alreadyAccounted in flat_obs:
                    if (
                        alreadyAccounted.x == section.x
                        and alreadyAccounted.y == section.y
                    ):
                        isAccounted = True
                        break
                if not isAccounted:
                    flat_obs.append(section)
        self.FLAT_OBSTACLES = flat_obs

    BATCH_SIZE = 16
    EPOCHS = 2000
    NOISE_DIM = 64  # latent vector size
    K = 3  # number of steps to apply to the discriminator
    sample_size = 3  # fixed sample size
    device
    uav_amount: int = -1
    time_lenght: int = -1
    g_learn_rate: float = 0.0002
    d_learn_rate: float = 0.0002

    # SCENARIO
    ORIGIN = coordObject(0, 0)
    POIS = [coordObject(0.031, 0.909), coordObject(0.56, 0.09)]
    POIS_TIMES = [10, 18, 18, 18]
    DIM = coordObject(15, 15)
    metrics = ["Coverage", "Collision", "Obstacles", "POIS", "Uptime"]
    OBSTACLES = [Obstacle(coordObject(0.94, 0.4), coordObject(0.95, 0.5), 1)]
    FLAT_OBSTACLES: list[coordObject] = []


constants = Constants_Class()
