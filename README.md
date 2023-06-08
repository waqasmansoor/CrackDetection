# An Improved YOLOv5 Underwater Detector Based on an Attention Mechanism and Multi-Branch Reparameterization Module
This repository contains the code for the paper: [An Improved YOLOv5 Underwater Detector Based on an Attention Mechanism and Multi-Branch Reparameterization Module](https://www.mdpi.com/2079-9292/12/12/2597).
## Datasets 
**URPC2019**: [Google Drive](https://drive.google.com/file/d/1DV1I5NNy0xGD7V9uGeQoOMF2wivX_e-Z/view?usp=share_link)
## Model
**urpc_s model**: [Google Drive](https://drive.google.com/file/d/1Diwcqz69DrXO_ErxzzulsEeduPl45cD-/view?usp=sharing)
## Training
```angular2html
python train.py --cfg model/urpc_s.yaml --data data/URPC2019 --hyp data/hyps/hyp.urpc.yaml --batch-size 8 --name UWDetector
```

## Convert
To fuse fusion block
```angular2html
python --weights run/UWDetector/train/weight/best.pt --save_path ./convert.pt 
```
## Val
```angular2html
python val.py --data data/URPC2019.yaml --weights ./conver.pt --name UWDetector
```

## Citation

```
@Article{electronics12122597,
AUTHOR = {Zhang, Jian and Chen, Hongda and Yan, Xinyue and Zhou, Kexin and Zhang, Jinshuai and Zhang, Yonghui and Jiang, Hong and Shao, Bingqian},
TITLE = {An Improved YOLOv5 Underwater Detector Based on an Attention Mechanism and Multi-Branch Reparameterization Module},
JOURNAL = {Electronics},
VOLUME = {12},
YEAR = {2023},
NUMBER = {12},
ARTICLE-NUMBER = {2597},
URL = {https://www.mdpi.com/2079-9292/12/12/2597},
ISSN = {2079-9292},
DOI = {10.3390/electronics12122597}
}
```
