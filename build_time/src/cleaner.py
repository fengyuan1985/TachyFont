"""
  Copyright 2014 Google Inc. All rights reserved.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

from fontTools.subset import Options, load_font, Subsetter, save_font
from common import reverse_cmap


class Cleaner(object):
  """A font cleaner which is initialized with
     fontfile : full path to font file
     hinting : True if you want to keep hinting
     whitespace_list : These code points are expected to hve 0 contours.

  def __init__(self, fontfile, hinting, whitespace_list):
    self.fontfile = fontfile
    self.options = Options()
    self.options.hinting = hinting
    self.font = load_font(fontfile, self.options, lazy=False)
    assert 'glyf' in self.font, 'only support TrueType (quadratic) fonts \
    (eg, not CFF) at this time'    
    self.whitespace_list = whitespace_list

  def _invalid_glyphs(self, names):
    invalid_glyphs = set()
    glyf_table = self.font['glyf']
    rcmap = reverse_cmap(self.font)
    for name in names:
      if name != '.notdef' and glyf_table[name] and \
          glyf_table[name].numberOfContours == 0 and \
          rcmap[name] not in self.whitespace_list:
        invalid_glyphs.add(name)
    return invalid_glyphs

  def clean(self):
    """
    Remove glyphs that should have outlines but do not.
    """
    names = set(self.font.getGlyphOrder())
    names.difference_update(self._invalid_glyphs(names))
    subsetter = Subsetter(options=self.options)
    subsetter.populate(glyphs=names)
    subsetter.subset(self.font)

  def save(self, outputfile):
    save_font(self.font, outputfile, self.options)

  def close(self):
    self.font.close()
