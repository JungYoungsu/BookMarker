from PIL import Image


for i in range(1,103):
	img = Image.open('bookshelf_' + str(i) + '_1.png')
	img = img.convert("RGBA")
	datas = img.getdata()

	newData = []
	for item in datas:
		if item[0] == 255 and item[1] == 255 and item[2] == 255:
			newData.append((255, 255, 255, 0))
		else:
			newData.append(item)

	img.putdata(newData)
	img.save("temp/" + "bookshelf_" + str(i) + "_1.png", "PNG")