from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
from enhancer.Enhancer import Deblurrer, Denoiser, SuperResolver
from PIL import Image as _Image
from io import BytesIO
import sys
# Create your models here.


class Image(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True)
    name = models.TextField(default='')
    image = models.ImageField(upload_to="images")
    deblur = models.BooleanField(default=False)
    denoise = models.BooleanField(default=False)
    super_resolve = models.BooleanField(default=False)
    deblurrer = Deblurrer()
    denoiser = Denoiser()
    sr = SuperResolver()

    def __str__(self):
        return str(self.unique_id)

    def save(self):
        img = _Image.open(self.image).convert('RGB')

        img_enhanced = img

        if self.denoise:
            img_enhanced = self.denoiser.enhance(img_enhanced)
        if self.deblur:
            img_enhanced = self.deblurrer.enhance(img_enhanced)
        if self.super_resolve:
            img_enhanced = self.sr.enhance(img_enhanced)

        # transform image here
        output = BytesIO()
        im = _Image.fromarray(img_enhanced)

        # im = img.resize((400, 400))

        im.save(output, format='JPEG', quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(output, 'ImageField', str(
            self.unique_id) + ".jpg", 'image/jpeg', sys.getsizeof(output), None)
        self.name = "%s.jpg" % self.image.name.split(
            '.')[0]

        super(Image, self).save()
