#  python3 objectclassification.py --dataset=dataset

import os
import argparse
import tensorflow as tf 

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--dataset', required=True, help='path to the dataset')
# ap.add_argument('-s', '--steps', required=True, help='number of training steps')
args=vars(ap.parse_args())
# os.system('git clone https://github.com/googlecodelabs/tensorflow-for-poets-2')
# os.system('mv tensorflow-for-poets-2 classify')
os.system('mkdir classify classify/tf_files classify/scripts')
os.system(f'cp -rf {args["dataset"]} classify/tf_files/')	
os.system('cp retrain1.py classify/scripts/')
os.chdir('classify')
os.system('mkdir servablemodelc servablemodelc/1')
os.system('ls')
os.system(f'''python3 -m scripts.retrain1 \
  --bottleneck_dir=tf_files/bottlenecks \
  --validation_batch_size=-1 \
  --model_dir=tf_files/models/ \
  --summaries_dir=tf_files/training_summaries/"inception_v3" \
  --saved_model_dir=model/1 \
  --output_graph=tf_files/retrained_graph.pb \
  --output_labels=tf_files/retrained_labels.txt \
  --image_dir=tf_files/dataset''')

 # --how_many_training_steps={args["steps"]} \

# os.system('cp tf_files/models/mobilenet_v1_0.50_224/quantized_graph.pb servablemodelc/1/saved_model.pb')
os.chdir('../')

os.system('/tensorflow-serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=8080 --model_name=inception_v3 --model_base_path=/tensorflow-serving/objectclassification/classify/model &> model_log &')
