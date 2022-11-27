"""
DSC 20 Mid-Quarter Project
Name: Wenyuan Chen and Yu Huang
PID:  A15516589/A154556000
"""

# Part 1: RGB Image #
class RGBImage:
    """
    A class to create image objects in RGB color spaces
    """
    def __init__(self, pixels):
        """
        A constructor that initializes a RGBImage instance and necessary 
        instance variables.
        """
        self.pixels = pixels

    def size(self):
        """
        A getter method that returns the size of the image in a tuple
        (# of rows,# of columns)
        """
        return (len(self.pixels[0]), len(self.pixels[0][0]))

    def get_pixels(self):
        """
        A getter method to return a copy of the pixel matrix of the image
        """
        # using list to create a deep copy of the matrix
        copy_matrix = [[[intensity for intensity in row] for row in channel] \
        for channel in self.pixels]
        return copy_matrix 

    def copy(self):
        """
        A getter method that returns copy of the RGBImage instance
        """
        copy_instance = RGBImage(self.get_pixels())
        return copy_instance

    def get_pixel(self, row, col):
        """
        A getter method that returns the color of the pixel at
        position(row, col) in a 3-element tuple
        """
        blue_channel = 2
        assert all([isinstance(row, int), isinstance(col, int)])
        assert all([0 <= col <= self.size()[1]-1, 0 <= row <= self.size()[0]-1])
        return (self.pixels[0][row][col], self.pixels[1][row][col], \
            self.pixels[blue_channel][row][col])

    def set_pixel(self, row, col, new_color):
        """
       A setter method that updates the color of the pixel at position
       (row, col) to the new_color inplace.
       """
       # using enumerate to loop over the index and color of the matrix, 
       # and then update the pixel in place
        assert all([isinstance(row, int), isinstance(col, int)])
        assert all([0 <= col <= self.size()[1]-1, 0 <= row <= self.size()[0]-1])
        for index, color in enumerate(new_color):
            if color != -1:
                self.pixels[index][row][col] = color


# Part 2: Image Processing Methods #
class ImageProcessing:
    """
    A class that have methods for the class only return a proceesed image after
    the methods applied to the image
    """
    @staticmethod
    def negate(image):
        """
        A method that returns the negative image instance of the given image, 
        that is all piexel values are inverted for that image. 
        """
        max_intensity = 255
        # loop over each channel, and then loop over each row of each channel,
        # finally loop over and update each intensity of each row. 
        negated_pixels = list(map(lambda channel: list(map(lambda row: \
            list(map(lambda intensity: max_intensity - intensity, row)), \
            channel)), image.get_pixels()))
        return RGBImage(negated_pixels)


    @staticmethod
    def grayscale(image):
        """
        A method that converts the given image to grayscale by replacing
        the pixel with the average intensity of that position
        """
        length_3d_matrix = 3
        blue_channel = 2
        matrix_gray = image.get_pixels()
        # obtain a 1d matrix with the average of intensities at each position
        gray_scale_pixels = list(map(lambda x, y, z: list(map\
            (lambda u, v, w: (u+v+w)// length_3d_matrix, x,y,z)), \
        matrix_gray[0], matrix_gray[1], matrix_gray[blue_channel]))

        # the final matrix will have three of the same 1d matrix.
        return \
        RGBImage([gray_scale_pixels, gray_scale_pixels, gray_scale_pixels])


    @staticmethod
    def scale_channel(image, channel, scale):
        """
        A method that scales the given channel of the image by the given scale
        """
        max_intensity = 255
        new_image = image.get_pixels()
        new_image[channel] = list(map(lambda row: list(map(lambda intensity: \
            min(intensity*scale, max_intensity), row)), new_image[channel]))
        return RGBImage(new_image)

    @staticmethod
    def clear_channel(image, channel):
        """
        A method that clears the given channel of the image by updateing every
        intensity value in the given chennel to 0
        """
        max_intensity = 255
        new_image = image.get_pixels()
        new_image[channel] = list(map(lambda row: list(map(lambda intensity: \
            0, row)), new_image[channel]))
        return RGBImage(new_image)

    @staticmethod
    def rotate_90(image, clockwise):
        """
        A method that rotates the image for 90 degrees,clockwise or 
        counter clockwise. 
        """
        blue_channel = 2
        new_image = image.get_pixels()
        if clockwise:
            new_pixel = list(map(lambda channel: list(map(lambda row: \
                row[::-1], list(map(list, zip(*channel))))), new_image))
            return RGBImage(new_pixel)
        if not clockwise:
            transpose_pixel = list(map(lambda channel: list(map(list, \
                zip(*channel))), new_image))
            red_channel = [transpose_pixel[0][-index] \
            for index in range(1, len(transpose_pixel[0])+1)]
            
            green_channel = [transpose_pixel[1][-index] \
            for index in range(1, len(transpose_pixel[1])+1)]
           
            blue_channel = [transpose_pixel[blue_channel][-index] \
            for index in range(1, len(transpose_pixel[blue_channel])+1)]
            return RGBImage([red_channel, green_channel, blue_channel])

    @staticmethod
    def crop(image, tl_row, tl_col, target_size):
        """
        A method that crops the image to target size starting at tl_row and
        tl_col.
        If col and row overflow after cropping, stop at the boarders.
        """
        blue_channel = 2
        new_image = image.get_pixels()
        actual_row = min(image.size()[0], tl_row + target_size[0])
        actual_col = min(image.size()[1], tl_col + target_size[1])
        red_row = [row for index, row in enumerate(new_image[0]) \
        if tl_row <= index <= actual_row]
        red_intensity = [[col for index, col in enumerate(row) \
        if tl_col <= index <= actual_col] for row in red_row]
        
        green_row = [row for index, row in enumerate(new_image[1]) \
        if tl_row <= index <= actual_row]
        green_intensity = [[col for index, col in enumerate(row) \
        if tl_col <= index <= actual_col] for row in green_row]
        
        blue_row = [row for index, row in enumerate(new_image[blue_channel]) \
        if tl_row <= index <= actual_row]
        blue_intensity = [[col for index, col in enumerate(row) \
        if tl_col <= index <= actual_col] for row in blue_row]

        return RGBImage([red_intensity, green_intensity, blue_intensity])

    @staticmethod
    def chroma_key(chroma_image, background_image, color):
        """
        An algorithm that replaces th pixels with the specified color in the
        chroma_image
        """
        assert type(chroma_image) == RGBImage
        assert type(background_image) == RGBImage
        assert chroma_image.size() == background_image.size()
        new_image = chroma_image.copy()
        for index_row in range(new_image.size()[0]):
            for index_col in range(new_image.size()[1]):
                if new_image.get_pixel(index_row, index_col) == color:
                    new_image.set_pixel(index_row, index_col, \
                        background_image.get_pixel(index_row, index_col))
        return new_image


# Part 3: Image KNN Classifier #
class ImageKNNClassifier:
    """
    A RGBImage clissifier that predicts the label of a piece of unkwnown image
    """

    def __init__(self, n_neighbors):
        """
        A constructor that initializes a ImageKNNClassifier instance and the
        size of the nearest neighborhood
        """
        self.n_neighbors = n_neighbors
        self.data = []

    def fit(self, data):
        """
        Fit the classifier by storing all training data in the classifier 
        instance
        """
        assert len(data) > self.n_neighbors
        assert len(self.data) == 0
        for image in data:
            self.data.append(image)
    @staticmethod
    def distance(image1, image2):
        """
        Compute the Euclidean distance between RGBimage image 1 and image 2
        """
        num_of_channel = 3
        image1_matrix = image1.pixels
        image2_matrix = image2.pixels
        assert isinstance(image1, RGBImage)
        assert isinstance(image2, RGBImage)
        assert image1.size() == image2.size()
        
        return (sum([(image1_matrix[channel][row][col]-\
            image2_matrix[channel][row][col])**2 \
            for channel in range(num_of_channel) for row in \
            range(image1.size()[0]) for col in range(image1.size()[1])]))**(1/2)
        
        
    @staticmethod
    def vote(candidates):
        """
        find out the most popular label from the n_neighbors nearest candidates
        labels
        """
        dit = {}
        for label in candidates:
            if label not in dit:
                dit[label] = 1
            else:
                dit[label] += 1
        for label, value in dit.items():
            if value == max(dit.values()):
                return label
        
    def predict(self, image):
        """
        Predict the label of the given image using the KNN classification 
        algorithm.
        """
        assert len(self.data) > 0
        sorted_n_neighbor_dis = \
        sorted([ImageKNNClassifier.distance(image, tup[0]) for tup \
            in self.data])[:self.n_neighbors]
        label_candidates = [tup[1] for tup in self.data if \
        ImageKNNClassifier.distance(image, tup[0]) \
        in sorted_n_neighbor_dis]
        return ImageKNNClassifier.vote(label_candidates)

