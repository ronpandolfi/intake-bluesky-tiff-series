import tifffile
from intake_bluesky_files import FileHandlerPlugin


class TIFSeriesPlugin(FileHandlerPlugin):
    name = 'TIF Series'
    extensions = ['.tiff', '.tif']

    def __call__(self, *args, **kwargs):
        return tifffile.imread(self.path)

    def metadata(self):
        return {key: tag.value for key, tag in tifffile.TiffFile(self.path).pages[0].tags.items()}


