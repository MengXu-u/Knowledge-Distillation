# Knowledge-Distillation
Code for: Optimized Computation Combining Classification and Detection Networks with Distillation in Traffic Scenarios


### Step1: Data Preprocessing 

```console
mx@bar:~$ python DataProcessing/change_hsv.py
mx@bar:~$ python DataProcessing/cut_round.py
mx@bar:~$ python DataProcessing/cut_round2.py
```

### Step2: Classification experiment (vgg16, caffe implement)

##### TBD, given the caffe prototxt as the network.

### Step3: Object Detection experiment (Faster-RCNN based, caffe implement)

```console
mx@bar:~$ python Models/model_show.py 
```

### Step4: Results comparison

