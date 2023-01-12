torch-model-archiver --model-name cnn --version 1.0 --model-file model-store/models/cnn.py --serialized-file model-store/models/parameters.pt --handler model-store/models/handler.py
mv cnn.mar model-store/models
torchserve --start --model-store model-store/models --models cnn=cnn.mar --ts-config config.properties