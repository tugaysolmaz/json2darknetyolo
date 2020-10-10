# json2darknetyolo

Convert Supervisely annotation type to darknet-yolo style. Creates:
* <Annotation .txt> files under new created <annotations_darknet> folder
* <coco_classes.names> file

Requirements:

* Python 3
* opencv or PIL (and numpy)
* (havent tried on linux, but it should work)

Versions of opencv or PIL should not matter, they are only needed for image dimensions, since darknet labeling depends on it.

You also should have a folder structure if you have Supervisely annotated data:

__Dataset Folder\\
....|__meta.json
....|__annotations\\
........|__01.json
........|__02.json
........|__...
....|
....|__images\\
........|__01.jpg
........|__02.png
........|__...

## Tutorial

* Clone repository
* Just copy paste json2darknet.py right next to meta.json file

You can also use command line tool:

```
python json2darknet -p database/my_dataset
```

## Author
Tugay Solmaz - [Deahran](https://github.com/Deahran)
Feel free to make suggestions or contact me.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Keywords
darknet, yolo, json, json2darknet, json2yolo, json 2 yolo, json 2 darknet, json to darknet conversion, json to yolo conversion.