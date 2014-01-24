from compressor.filters.base import CompilerFilter
from compressor.filters.css_default import CssAbsoluteFilter

# Work around the fact that django-compressor doesn't succeed in running the
# CssAbsoluteFilter on less files due to broken path lookups.

class LessFilter(CompilerFilter):
    def __init__(self, content, attrs, **kwargs):
        super(LessFilter, self).__init__(content, command='lessc {infile} {outfile}', **kwargs)

    def input(self, **kwargs):
        content = super(LessFilter, self).input(**kwargs)
        return CssAbsoluteFilter(content).input(**kwargs)
