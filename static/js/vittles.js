// Create a popup displayed when hovering over the given selector.
//
// `selector` must have an `id` attribute, as well as a child element with
// `class='popup'`. The content of the `popup` class is displayed when hovering
// over elements matching `selector`.
function add_popup(selector) {
  $(selector).mouseover(function(event) {
    $('#' + this.id + ' .popup').show();
  }).mouseout(function() {
    $('#' + this.id + ' .popup').hide();
  });
}

