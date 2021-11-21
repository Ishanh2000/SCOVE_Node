# AUM SHREEGANESHAAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
import requests
from base64 import b64encode

SERVER_URI = "http://ec2-18-222-200-30.us-east-2.compute.amazonaws.com:5000"

if __name__ == "__main__":
  i0 = b64encode(open("test/imisra_0.png", "rb").read())
  i1 = b64encode(open("test/imisra_1.png", "rb").read())
  i2 = b64encode(open("test/imisra_2.png", "rb").read())
  i3 = b64encode(open("test/imisra_3.png", "rb").read())
  i4 = b64encode(open("test/imisra_4.png", "rb").read())

  t0 = b64encode(open("test/tulika_0.png", "rb").read())
  t1 = b64encode(open("test/tulika_1.png", "rb").read())
  t2 = b64encode(open("test/tulika_2.png", "rb").read())
  t3 = b64encode(open("test/tulika_3.png", "rb").read())
  t4 = b64encode(open("test/tulika_4.png", "rb").read())

  req = requests.post(SERVER_URI + "/register", json={ "train" : [
    { "name" : "imisra", "files" : [(b"data:image/png;base64," + x) for x in [ i0, i1, i2, i3, i4 ]] },
    { "name" : "tulika", "files" : [(b"data:image/png;base64," + x) for x in [ t0, t1, t2, t3, t4 ]] },
  ] })
  print(req.content.decode("UTF-8"))
