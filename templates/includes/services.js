// Rotate banner text
$(".rotate").textrotator({
  animation: "flipUp", // You can pick the way it animates when rotating through words. Options are dissolve (default), fade, flip, flipUp, flipCube, flipCubeUp and spin.
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
  //autoplay: true
})
