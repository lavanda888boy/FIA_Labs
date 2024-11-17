import cv2


def is_valid_for_passport(image_path, annotations):
    image = cv2.imread(image_path)
    if image is None:
        return False

    height, width, _ = image.shape

    image_is_valid_for_passport = is_color(image) and is_portrait_or_square(width, height) and \
        has_correctly_aligned_eyes(height, annotations) and \
        contains_single_person(annotations) and \
        has_valid_head_area(width, height, annotations)

    if image_is_valid_for_passport:
        return True

    return False


def is_color(image):
    if (image[..., 0] == image[..., 1]).all() and (image[..., 1] == image[..., 2]).all():
        return False

    return True


def is_portrait_or_square(width, height):
    if width > height:
        return False

    return True


def has_correctly_aligned_eyes(height, annotations, eye_distance_threshold=5):
    eyes = [ann for ann in annotations if ann[0] == 1]

    if len(eyes) == 2:
        eye_y_coords = [int(eye[2] * height) for eye in eyes]

        if abs(eye_y_coords[0] - eye_y_coords[1]) > eye_distance_threshold:
            return False

        return True
    else:
        return False


def contains_single_person(annotations):
    faces = [ann for ann in annotations if ann[0] == 0]

    if len(faces) != 1:
        return False

    return True


def has_valid_head_area(width, height, annotations, head_area_lower_threshold=0.2,
                        head_area_upper_threshold=0.5):
    faces = [ann for ann in annotations if ann[0] == 0]

    face = faces[0]
    face_area = (face[3] * height) * (face[4] * width)
    image_area = height * width
    face_area_ratio = face_area / image_area

    if not (head_area_lower_threshold <= face_area_ratio <= head_area_upper_threshold):
        return False

    return True