import argparse
import json
import os
try:
	import cv2
	def get_image_dims(im_file):
		im = cv2.imread(im_file,0)
		im_h, im_w = im.shape
		return im_h, im_w
		Exception.Modu
except ModuleNotFoundError as e:
	from PIL import Image
	def get_image_dims(im_file):
		im = Image.open(im_file)
		im_w, im_h = im.size
		return im_h, im_w
except ModuleNotFoundError as e:
	raise Exception("Either install opencv-python or PIL")


def main(data_path=""):
	meta_json_path = os.path.join(data_path,"meta.json")
	if not os.path.isfile(meta_json_path):
		raise Exception(meta_json_path + " not found.")
	# Create .data file
	with open(meta_json_path) as f:
		classes = json.loads(f.read())
		titles = [lis["title"] for lis in classes["classes"]]
		dic_titles = dict(zip(titles, range(len(titles))))

		names =  "\n".join(dic_titles.keys())
		meta_names_path = os.path.join(data_path,"meta.names")
		with open(meta_names_path, "w") as text_file:
			text_file.write(names)

	# Convert all spaces
	images_path = os.path.join(data_path,"images")
	anno_path = os.path.join(data_path,"annotations")
	darknet_path = os.path.join(data_path,"annotations_darknet")
	if not os.path.isdir(darknet_path): os.mkdir(darknet_path)

	anno_paths = os.listdir(anno_path)
	anno_paths = [path for path in anno_paths if path.endswith(".json")]

	for ap in anno_paths:
		with open(os.path.join(anno_path,ap)) as f:
			tmp_dict = json.loads(f.read())

			im_file = tmp_dict["FileName"]
			rel_path = os.path.join(images_path,im_file)
			if not os.path.isfile(rel_path): 
				print("Image file not found for " + rel_path)
				continue
			im_h, im_w = get_image_dims(rel_path)

			num_anno = tmp_dict["NumOfAnno"]
			if num_anno < 1: continue
			annotations = tmp_dict["Annotations"]
			anno_str = ""
			for json_anno in annotations:
				classname = json_anno["classname"]
				classnum = str(dic_titles[classname])
				xmin, ymin, xmax, ymax = json_anno["BoundingBox"]

				x_cen = ((xmax + xmin)/2) / im_w
				y_cen = ((ymax + ymin)/2) / im_h
				w = (xmax - xmin) / im_w
				h = (ymax - ymin) / im_h
				anno_str += classnum + " {:.4f} {:.4f} {:.4f} {:.4f}\n".format(x_cen, y_cen, w, h)

		darknet_anno = ap.split(".")[0]+".txt"
		with open(os.path.join(darknet_path, darknet_anno),"w") as f:
			f.write(anno_str)
			print(f"Converting: {ap} -> {darknet_anno}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert Supervisely format to Darknet-Yolo format')
	parser.add_argument('-p','--path', dest="data_path", default="", metavar="path", type=str,
	                    help='full or relative path to folder containing meta.json')

	args = parser.parse_args()
	main(data_path=args.data_path)