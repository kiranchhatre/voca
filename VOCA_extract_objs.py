

"""
Env yml: /ps/project/EmotionalFacialAnimation/data/mead/ensparc_audios/voca.yaml

USAGE:
python VOCA_extract_objs.py --audio_fname /ps/project/EmotionalFacialAnimation/data/mead/ensparc_audios --out_path /ps/project/EmotionalFacialAnimation/data/mead/ensparc_audios/VOCA
change:
    --condition_idx: Subject condition id in [1,8]
    
inputs: /is/cluster/fast/rdanecek/data/lrs3_enspark_testing/pretrain ... /dskjfdsbjf/0007.wav
outs: /is/cluster/fast/rdanecek/testing/enspark/results  ... /dskjfdsbjf/0007/1.obj and so on
"""


import os
import glob
import argparse
from utils.inference import inference

from pathlib import Path

def str2bool(val):
    if isinstance(val, bool):
        return val
    elif isinstance(val, str):
        if val.lower() in ['true', 't', 'yes', 'y']:
            return True
        elif val.lower() in ['false', 'f', 'no', 'n']:
            return False
    return False

parser = argparse.ArgumentParser(description='Voice operated character animation')
parser.add_argument('--tf_model_fname', default='/is/cluster/scratch/kchhatre/Work/ENSPARC/baselines/voca/model/gstep_52280.model', help='Path to trained VOCA model')
parser.add_argument('--ds_fname', default='/is/cluster/scratch/kchhatre/Work/ENSPARC/baselines/voca/ds_graph/output_graph.pb', help='Path to trained DeepSpeech model')
parser.add_argument('--audio_fname', default='/is/cluster/fast/scratch/rdanecek/testing/enspark/baselines/lrs3_audios_only', help='Path of input speech sequence')
parser.add_argument('--template_fname', default='/is/cluster/scratch/kchhatre/Work/ENSPARC/baselines/voca/template/FLAME_sample.ply', help='Path of "zero pose" template mesh in" FLAME topology to be animated')
parser.add_argument('--condition_idx', type=int, default=5, help='Subject condition id in [1,8]')
parser.add_argument('--uv_template_fname', default='', help='Path of a FLAME template with UV coordinates')
parser.add_argument('--texture_img_fname', default='', help='Path of the texture image')
parser.add_argument('--out_path', default='/is/cluster/fast/scratch/rdanecek/testing/enspark/baselines/VOCA_lrs3_test/sub3', help='Output path')
parser.add_argument('--visualize', default='False', help='Visualize animation')

args = parser.parse_args()
tf_model_fname = args.tf_model_fname
ds_fname = args.ds_fname
audio_fname = args.audio_fname
template_fname = args.template_fname
condition_idx = args.condition_idx
out_path = args.out_path

uv_template_fname = args.uv_template_fname
texture_img_fname = args.texture_img_fname

if not os.path.exists(out_path):
    os.makedirs(out_path)

for i, p in enumerate(Path(audio_fname).glob('*')):
    sample_dir = p.stem
    out_path = os.path.join(args.out_path, sample_dir)
    os.makedirs(out_path, exist_ok=True)
    print(f"Processing {sample_dir} ({i+1}/{len(list(Path(audio_fname).glob('*')))})")
    audio_fname = os.path.join(args.audio_fname, sample_dir)
    inference(tf_model_fname, ds_fname, audio_fname, template_fname, condition_idx, out_path, str2bool(args.visualize), uv_template_fname=uv_template_fname, texture_img_fname=texture_img_fname)

print("Changing permissions of the output files")
os.system("find /is/cluster/fast/scratch/rdanecek/testing/enspark/baselines -type d -exec chmod 755 {} +")
print("Done")

# sub1: 3
# sub2: 4
# sub3: 5