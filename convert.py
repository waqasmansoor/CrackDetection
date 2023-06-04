from models.common import DetectMultiBackend
import argparse
from pathlib import Path
from utils.general import print_args
import torch
from copy import deepcopy
from models.yolo import Model

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
from utils.torch_utils import select_device
from utils.torch_utils import de_parallel

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default="./best.pt", help='model path(s)')
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--save_path', type=str, default=ROOT / 'convert.pt')
    parser.add_argument('--do_copy', type=bool, default=True)
    opt = parser.parse_args()
    print_args(vars(opt))
    return opt


def convert(opt):
    device = select_device(opt.device, batch_size=1)
    models = torch.load(opt.weights, map_location=device)

    model = models['model']
    if opt.do_copy:
        model = deepcopy(model)
    for module in model.modules():
        if hasattr(module, 'switch_to_deploy'):
            module.switch_to_deploy()
    if opt.save_path is not None:
        ckpt = {'model': deepcopy(de_parallel(model)).half()}

        torch.save(ckpt, opt.save_path)


if __name__ == "__main__":
    opt = parse_opt()
    convert(opt)
