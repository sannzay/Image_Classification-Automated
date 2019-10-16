# Image Classification

## Requirements:

1. This project is supposed to be run in a docker with tensorflow-serving setup in it.
   (To save the trouble, you can pull my docker container with all requirements installed: sannzay/tf_serve:version4)
2. tensorflow (both in docker and local)
3. utils (both in docker and local)
4. grpcio (only in local)
5. grpcio-tools (only in local)
6. matplotlib (both in docker and local)
7. pillow (both in docker and local)
8. scipy (only in local)
9. tensorflow-serving-api (only in local)
10. protobuf-complier (both in docker and local)
11. numpy (both in docker and local)
12. pandas (both in docker and local)
13. python3 (both in docker and local)

## Instructions to run:

Run the following comand in the docker terminal:
```
*python3 objectclassification.py --dataset=dataset*
```
Change the datset path to your dataset path which you want to train.

Dataset folder should contain your image classes in seperate folders with their label names as folder names with a minimum of two folders (eg. Here dataset folder contains two folders namely, "dog" and "cat").

For setting up the tensorflow-serving on the docker refer the section 4 of the object_Detection_repot document present in this repository.

**NOTE:** This project can also be executed without docker, but the hosting part of the model won't be achieved. (In that case comment the last line (os.system command) in the objectclassification.py file) 

## Tensorflow serving

### Generating model files and structuring them as per the tf_serving needs

Present version of Tensorflow serving doesn’t accept the direct accessing of the model and its weights. We need to get the saved model to be served in the session which contains both the weights and graph structure and also freeze (used for the inference) the model before we export it to the serving engine. That is, create the saved model (.pb file) from the available weight and structure files (.ckpt files). Note that saved model is not a serializable one and can be used for retraining whereas once its frozen it becomes serializable and cannot be used for training.

Go to the models/research/object_detection folder, where you will find export_inference_graph.py file which helps to create the desired models. Mention the path to the config file and checkpoints used for training the model while running it.
```
python3 -u export_inference_graph.py \
  --input_type=image_tensor \
  --pipeline_config_path=/home/convo/Downloads/faster_rcnn_inception_v2_pets.config \
  --trained_checkpoint_prefix=tensorflow-obj/cfast100/model.ckpt-100 \
  --output_directory=model_output/cfast100
```
Once the command is executed you will find the saved model, frozen model and checkpoints files at the mentioned output location. 

Grab the contents in the saved_model folder and put inside a new folder named “1” outside the working directory. Create a new folder with the name of your own neural network, lets say “fastcarmodel” and put the folder “1” inside it. 

### Installing the docker

Open the terminal and execute the following commands in the sequence provided:
```
sudo apt update
sudo apt upgrade

sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt update
sudo apt install docker-ce
```
By now you should be able to see the running updates of the docker by executing the following command:
```
sudo systemctl status docker 
```


### Building the tensorflow_serving docker image

First we have to clone the tensorflow serving github repository before proceeding to the building of the docker image.
```
git clone --recursive https://github.com/tensorflow/serving
```
Enter into the tensorflow serving project folder through terminal
```
cd serving
```
Inside /tools/docker/ you will find the Dockerfile.devel which lists all the dependencies required for us to build the tensorflow_serving service. Through docker we can create a specific container which is unaffected by other system files and loaded with all the dependencies mentioned.

This can be achieved by executing the following command from serving/:
```
sudo docker build --pull -t $USER/tensorflow-serving-devel -f tensorflow_serving/tools/docker/Dockerfile.devel .
```
Once it is build, run it by the following command:
```
docker run --name=tensorflow_container -it $USER/tensorflow-serving-devel
```
Check for the contents inside the container. Some versions come with tensorflow_serving already configured inside it. If it is the case, proceed to the next step. Orelse manually clone the tensorflow_serving repo and configure it using the following command:
```
git clone --recursive https://github.com/tensorflow/serving 
```
Now we need to build the tensorflow_serving project using Google’s bazel from inside the container. It downloads and manages all the dependencies required for the serving.
```
bazel build -c opt tensorflow_serving/...
```

### Exporting and Running the model

Once the building is finished completely, get back to the directory where we saved our ready-made final graph folder, “fastcarmodel” through terminal.

Now we have to copy that folder into the container we built by executing the following command:
```
sudo docker cp ./fastcarmodel x:/serving  (x is the contained id {eg: root@x})
```
Now get back to the container and check whether the model is exported. Once it is done, we are all set to host our model on the server.

Use the following command from inside the container to host the model using using tensorflow-serving (Mention the port number, model name, log file and desired path for the model ):
```
bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=9000 --model_name=inception --model_base_path=/serving/fastcarmodel &> fastcarmodel_log & 
```
You can check the updates of the server in the fastcarmodel_log as mentioned in the above command.

### Accessing the service using the client file

Before leaving the container, install the required grpc tools by the following command:
```
pip3 install grpcio grpcio-tools
```
Now, get back to the directory where the client.py is saved and again install the grpc tools here.
```
pip3 install grpcio grpcio-tools
```
Get the IP address of our container by using the following command: 
```
sudo docker network inspect bridge | grep Ipv4Address
```
Once it is executed, you will see the address where our service is hosted. Note it.

Now get the inference by executing the client.py file, mentioning the address and the image path that we want to analyze, as follows:
```
python3 client.py --server=172.17.0.2:9000 –image=./test.jpg
```
