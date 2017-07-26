function CheckEmail($Email = "") {
  if (ereg("[[:alnum:]]+@[[:alnum:]]+\.[[:alnum:]]+", $Email)) {
    return true;
  } else {
    return false;
  }
}
