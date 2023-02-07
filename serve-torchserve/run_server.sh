#!/bin/bash

models=""
for model in "model-store/$MODEL_STORE"/*
do
  models=$models,"${model##*/}"
done
models="${models:1}"
echo $models

echo $MODEL_STORE
echo $MODELS

torchserve --start --model-store model-store/$MODEL_STORE --models $models
