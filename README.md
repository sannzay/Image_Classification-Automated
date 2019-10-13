# image-recogntion

## Requirements:

1. This project is supposed to be run in a docker with tensorflow-serving setup in it.
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

*python3 objectclassification.py --dataset=dataset*

Change the datset path to your dataset path which you want to train.

Dataset folder should contain your image classes in seperate folders with their label names as folder names with a minimum of two folders (eg. Here dataset folder contains two folders namely, "dog" and "cat").

For setting up the tensorflow-serving on the docker refer the section 4 of the object_Detection_repot document present in this repository.

**NOTE:** This project can also be executed without docker, but the hosting part of the model won't be achieved. (In that case comment the last line (os.system command) in the objectclassification.py file) 
