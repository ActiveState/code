_slugify_strip_re = /[^\w\s-]/g;
_slugify_hyphenate_re = /[-\s]+/g;
function slugify(s) {
  s = s.replace(_slugify_strip_re, '').trim().toLowerCase();
  s = s.replace(_slugify_hyphenate_re, '-');
  return s;
}
