# K-Means Color Quantization

Example of K-Means color quantization. It performs pixel-wise replacements on the image based on the number of clusters defined with K-Means.

It's a basic form of compression where it can reduce the storage space.

## Execution

The program can be run by simply using this command
```bash
python main.py -f sample/cliff.jpg
python main.py -f sample/house.jpg
```

Clicking the "Save" button will compress the image into the custom format (saved under the `sample` directory).

## Decompression

In order to visualize the compressed image you can run
```bash
python compress.py -f sample/PATH_TO_IMAGE
```