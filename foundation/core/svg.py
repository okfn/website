"""
Inspired with
https://github.com/artrey/django-svg-image-form-field
"""
import logging
from io import BytesIO

from xml.etree import ElementTree
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    get_available_image_extensions,
)
from django.forms import ImageField as DjangoImageField
from PIL import Image


logger = logging.getLogger(__name__)


def validate_image_and_svg_file_extension(extension):
    allowed_extensions = get_available_image_extensions() + ['svg']
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(extension)


class SvgAndImageFormField(DjangoImageField):
    default_validators = [validate_image_and_svg_file_extension]

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports).
        """
        logger.info(f'SvgAndImageFormField.to_py :: {data} :: {type(data)}')

        try:
            test_file = super().to_python(data)
        except ValidationError:
            # add a workaround to handle svg images
            if not self.is_svg(data):
                raise
            else:
                test_file = data

        if test_file is None:
            return None

        # We need to get a file object for Pillow. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            ifile = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                ifile = BytesIO(data.read())
            else:
                ifile = BytesIO(data['content'])

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            image = Image.open(ifile)
            # verify() must be called immediately after the constructor.
            image.verify()

            # Annotating so subclasses can reuse it for their own validation
            test_file.image = image
            test_file.content_type = Image.MIME[image.format]
        except Exception:
            # add a workaround to handle svg images
            is_svg_file = self.is_svg(data)
            logger.info(f'Error image is_svg: {is_svg_file}')
            if not is_svg_file:
                raise ValidationError(
                    self.error_messages['invalid_image'],
                    code='invalid_image',
                )
        if hasattr(test_file, 'seek') and callable(test_file.seek):
            test_file.seek(0)
        return test_file

    def is_svg(self, f):
        """
        Check if provided file is svg
        """

        # When is the temporary_file_path
        f_is_path = isinstance(f, str)

        if f_is_path:
            fio = open(f, 'rb')
        else:
            fio = f

        fio.seek(0)

        tag = None
        try:
            for event, el in ElementTree.iterparse(fio, ('start',)):
                tag = el.tag
                break
        except ElementTree.ParseError:
            pass

        if f_is_path:
            fio.close()

        return tag == '{http://www.w3.org/2000/svg}svg'
