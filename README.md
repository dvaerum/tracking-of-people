[TOC]

# Introduction

This is a small project made doing [SummerHack 2020](https://sommerhack.dk/) there would track you movement and make a DMX project light up your path. It is very hacky, but we got it to somewhat work.

## Re-create the `yolo-coco/yolov3.weights`
The `yolo-coco/yolov3.weights` files is too big so I had to split it up. So, in our to re-create it run
```
cat yolo-coco/yolov3.weights.* > yolo-coco/yolov3.weights

# Verify: 293c70e404ff0250d7c04ca1e5e053fc21a78547e69b5b329d34f25981613e59b982d93fff2c352915ef7531d6c3b02a9b0b38346d05c51d6636878d8883f2c1  yolo-coco/yolov3.weights
sha512sum yolo-coco/yolov3.weights
```

## Stuff to improve

- Use an AMD or Nvidia graficcard instead of the build-in intel grafic
- Learn advance math and apply it or maybe there exist a library for calculating posission
- Maybe find a better dataset for object reconission


