from compressor.filters.base import CompilerFilter
from compressor.filters.css_default import CssAbsoluteFilter
from compressor.utils import staticfiles


class CustomCssAbsoluteFilter(CssAbsoluteFilter):
    def find(self, basename):
        # This is the same as the inherited implementation except for the
        # removal of a check on settings.DEBUG. See
        #
        #   https://stackoverflow.com/questions/15532464
        #
        # for details.
        if basename and staticfiles.finders:
            return staticfiles.finders.find(basename)


# Work around the fact that django-compressor doesn't succeed in running the
# CssAbsoluteFilter on less files due to broken path lookups.
class LessFilter(CompilerFilter):
    def __init__(self, content, attrs, **kwargs):
        super(LessFilter, self).__init__(
            content,
            command='lessc --no-color {infile} {outfile}',
            **kwargs)

    def input(self, **kwargs):
        content = super(LessFilter, self).input(**kwargs)
        return CustomCssAbsoluteFilter(content).input(**kwargs)
