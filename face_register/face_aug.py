from imgaug import augmenters as iaa

aug_pipe = iaa.Sequential([
    iaa.Sometimes(0.5, (iaa.PerspectiveTransform(scale=(0.01, 0.02)))),
    iaa.LinearContrast((0.9, 1.1)),
    iaa.AddToSaturation((-5, 10)),
    iaa.AddToBrightness((-20, 20)),
    iaa.SomeOf((0,2), [
        iaa.GaussianBlur((0, 0.1)),
        iaa.Sharpen(alpha=(0, 0.1), lightness=(0.9, 1.1))
    ]),
    iaa.Sometimes(0.5, iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.02*255), per_channel=0.5)),
    iaa.Sometimes(0.6, iaa.Affine(
        scale={"x": (0.95, 1.05), "y": (0.95, 1.05)},
        translate_percent={"x": (-0.05, 0.05), "y": (-0.05, 0.05)},
        rotate=(-3, 3),
        order=[0, 1]
    )),    
], random_order=True)