import os, string, random, itertools
from optparse import OptionParser
import albumentations as A
from skimage import io

parser = OptionParser()
parser.add_option(
    "-p", "--path", 
    dest="images_path", 
    help="Applies data augmentation to the images inside the given path", 
    metavar="<images path>"
)

(options, args) = parser.parse_args()

if not options.images_path:
    parser.error('Images path is required, use --help')

path = options.images_path

transformations_list = [
    A.Rotate(90, p=1),
    A.Rotate(180, p=1),
    A.Rotate(270, p=1),
]

for filename in os.listdir(path):
    if 'augmented' in filename:
        continue
    
    img = io.imread(path+'/'+filename)

    for i in range(len(transformations_list)): 
        transformation_elements = transformations_list[i]

        if not hasattr(transformation_elements, '__iter__'):
            transformation_elements = [transformation_elements]

        transform = A.Compose(transformation_elements)      

        transformed = transform(image=img)
        transformed_image = transformed["image"]

        augmented_path = path+'/augmented/'
        if not os.path.exists(augmented_path):
            os.makedirs(augmented_path)

        filedst = augmented_path+str(id(transformed_image))+''.join(random.sample(string.ascii_lowercase, 10))+filename
        io.imsave(filedst, transformed_image)


