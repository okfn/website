/** Helper Functions */
function str2Object (str) {
    if (!str || typeof str === 'undefined') {
      return {};
    }

    const jsonStr = str.replaceAll("'", '"').replace(/(\w+:)|(\w+ :)/g, function(matchedStr) {
      return '"' + matchedStr.substring(0, matchedStr.length - 1) + '":';
    });

    return JSON.parse(jsonStr); //converts to a regular object
  };

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }


/** Main Javascript function */
const okfnMain = {
    init () {
      okfnMain.applyPlayVideo();
      okfnMain.applyOpenVideo();
      okfnMain.applySlider();
    },

    /**
     * Apply slick to all sliders blocks identified
     * @returns {void}
     */
    applySlider () {
      const slider = $('.slider');

      if (!slider.length) {
        return;
      }

      const self = this;
      let sliderAttribute = 'data-slider';
      if (this.isMobile()) {
        sliderAttribute = 'data-slider-mobile';
      }

      const sliderEl = $('['+ sliderAttribute +']');
      if (sliderEl.length) {
        sliderEl.each(function () {
          const sliderOptions = str2Object($(this).attr(sliderAttribute));
          let sliderId = $(this).attr('id');
          if (!sliderId) {
            sliderId = 'slider-' + Math.floor(Math.random() * 1000);
            $(this).attr('id', sliderId);
          }

          self.doSlider('#' + sliderId, sliderOptions);
        })
      }
    },

    /**
     * Apply the slick carousel
     * @param {string} sliderId
     * @param {object} slidesOptions
     */
    doSlider (sliderId, sliderOptions) {
      sliderId = sliderId || '.slider';
      const defaultOptions = {
        dots: false,
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
      };

      sliderOptions = { ...defaultOptions, ...sliderOptions };

      const slider = $(sliderId);

      if (slider.length) {
        slider.each(function () {
          const sliderWrapper = $(this).closest('.slider-wrapper');

          $(this).on('init', function(event, slick) {
            $(window).on('load', function () {
              sliderWrapper.find('.slider__pager-total').text(slick.slideCount);
              $('.slick-arrow').css('top', ($(this).find('.slick-list').height() / 2) + 'px');
            });
          });

          $(this).on('beforeChange', function(event, slick, currentSlide, nextSlide) {
            sliderWrapper.find('.slider__pager-num').text((nextSlide + 1));
            sliderWrapper.find('.slider__pager-total').text(slick.slideCount);
          });

          $(this).slick(sliderOptions);
        });
      }
    },

    applyPlayVideo () {
      const videoPlayTrigger = $('[data-play-video]');
      if (!videoPlayTrigger.length) {
        return
      }

      videoPlayTrigger.on('click', function () {
        const el = $(this);
        el.addClass('-active');
        el.find('iframe').attr('src', 'https://www.youtube.com/embed/' + $(this).attr('data-play-video') + '?autoplay=1');
      });
    },

    applyOpenVideo () {
      const videoOpener = $('[data-open-video]');
      if (!videoOpener.length) {
        return
      }

      videoOpener.on('click', function () {
        okfnMain.openVideo($(this).attr('data-open-video') + '?autoplay=1');
      });
    },

    openVideo (youtubeId) {
      // if (okfnMain.isMobile()) {
      //   window.open('https://www.youtube.com/watch?v=' + youtubeId, '_blank');
      //   return;
      // }

      if (!$('#alert-video').length) {
        $('body').append($('<div id="alert-video" class="hidden w-full md:max-w-xl lg:max-w-5xl"><div class="iframe-video md:max-w-xl lg:max-w-5xl !mb-0"><div class="iframe-video__wrapper"><iframe width="560" height="315" src="" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen /></div></div></div>'));
        sleep(500);
      }
      $('#alert-video').find('iframe').attr('src', 'https://www.youtube.com/embed/' + youtubeId);
      $('#alert-video').modal();

      $('#alert-video').on($.modal.BEFORE_CLOSE, function() {
        $('#alert-video').find('iframe').attr('src', '');
      });
    },

    /**
     * Check if device is mobile
     * @returns {boolean}
     */
    isMobile () {
      let check = false;
      (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|android|playbook|silk|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw-(n|u)|c55\/|capi|ccwa|cdm-|cell|chtm|cldc|cmd-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc-s|devi|dica|dmob|do(c|p)o|ds(12|-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(-|_)|g1 u|g560|gene|gf-5|g-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd-(m|p|t)|hei-|hi(pt|ta)|hp( i|ip)|hs-c|ht(c(-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i-(20|go|ma)|i230|iac( |-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|-[a-w])|libw|lynx|m1-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|-([1-8]|c))|phil|pire|pl(ay|uc)|pn-2|po(ck|rt|se)|prox|psio|pt-g|qa-a|qc(07|12|21|32|60|-[2-7]|i-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h-|oo|p-)|sdk\/|se(c(-|0|1)|47|mc|nd|ri)|sgh-|shar|sie(-|m)|sk-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h-|v-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl-|tdg-|tel(i|m)|tim-|t-mo|to(pl|sh)|ts(70|m-|m3|m5)|tx-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas-|your|zeto|zte-/i.test(a.substr(0,4))) check = true; })(navigator.userAgent||navigator.vendor||window.opera);
      return check;
    },

    parseQueryVars () {
      return new Promise((resolve) => {
        const queryDict = {};
        location.search.slice(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
        return resolve(queryDict);
      });
    },
  }

  $(function () {
    okfnMain.parseQueryVars().then(function (queryVars) {
      okfnMain.queryVars = queryVars;
      okfnMain.init();
    });
    window.okfnMain = okfnMain;
  });