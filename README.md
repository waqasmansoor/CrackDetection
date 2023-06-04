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