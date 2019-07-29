from tesserocr import PyTessBaseAPI

images = ['sample1.jpg', 'sample2.jpg', 'sample3.jpg']

with PyTessBaseAPI() as api:
    for img in images:
        print ('x')
        #api.SetImageFile(img)
        #print (api.GetUTF8Text())
        #print (api.AllWordConfidences())
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.

from PIL import Image
from tesserocr import PyTessBaseAPI, RIL

image = Image.open('./data/cdn.differencebetween_crawler.net/wp-content/uploads/2019/02/Acetone-vs-Bleach.jpg.png')
with PyTessBaseAPI() as api:
    api.SetImage(image)
    box = {'x': 23, 'y': 516, 'w': 704, 'h': 216}
    api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
    ocrResult = api.GetUTF8Text()
    print (ocrResult)

    print ('hallo')

    boxes = api.GetComponentImages(RIL.WORD, True)
    print ('Found {} textline image components.'.format(len(boxes)))
    for i, (im, box, _, _) in enumerate(boxes):
        # im is a PIL image object
        # box is a dict with x, y, w and h keys
        api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
        ocrResult = api.GetUTF8Text()
        conf = api.MeanTextConf()
        print ((u"Box[{0}]: x={x}, y={y}, w={w}, h={h},  confidence: {1}, text_tokenized: {2}").format(i, conf, ocrResult, **box))