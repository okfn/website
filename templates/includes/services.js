//  Check if Internet Explorer
var ua = window.navigator.userAgent;
var msie = ua.indexOf("MSIE ");

// Rotate banner text
var textAnimation = "flipUp"; // You can pick the way it animates when rotating through words. Options are dissolve (default), fade, flip, flipUp, flipCube, flipCubeUp and spin.

// If IE don't use flip rotation (because it breaks)
if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./)) {
  textAnimation = "fade";
}

//  Setup rotating text
$(".rotate").textrotator({
  animation: textAnimation,
  separator: ",", // If you don't want commas to be the separator, you can define a new separator (|, &, * etc.) by yourself using this field.
  speed: 2000 // How many milliseconds until the next word show.
});


// Services slider
if (window.innerWidth > 768) {
  $("#services .components").addClass( "owl-carousel" );
}

$('#services .owl-carousel').owlCarousel({
  loop: true,
  center: true,
  dots: false,
  responsive: {
    0: {
      items: 1,
    },
    768: {
      autoWidth: true,
    }
  }
});

$("#services .component-nav .next").on('click', function () {
  $('#services .owl-carousel').trigger('next.owl');
});
$("#services .component-nav .prev").on('click', function () {
  $('#services .owl-carousel').trigger('prev.owl');
});


// testimonial slider
$('.testimonials.owl-carousel').owlCarousel({
  loop: true,
  items: 1,
  autoplay: true
})
